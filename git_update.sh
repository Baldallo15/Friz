#!/bin/bash

# ==============================================================================
#  G I T   U P D A T E   P R O
#  Script elegante para la gestión y sincronización de repositorios en GitHub
# ==============================================================================

# Definición de Colores y Estilos (ANSI)
COLOR_RESET="\033[0m"
COLOR_PRIMARY="\033[38;5;39m"     # Azul brillante
COLOR_SECONDARY="\033[38;5;141m" # Púrpura suave
COLOR_ACCENT="\033[38;5;214m"    # Naranja cálido
COLOR_SUCCESS="\033[38;5;82m"     # Verde brillante
COLOR_MUTED="\033[38;5;244m"     # Gris elegante
COLOR_DANGER="\033[38;5;196m"    # Rojo
BOLD="\033[1m"
DIM="\033[2m"

# Archivo de configuración local para persistencia
CONFIG_FILE="$HOME/.github_uploader.cfg"

# Función para mostrar la marquesina / banner ASCII
show_banner() {
    clear
    echo -e "${COLOR_PRIMARY}${BOLD}"
    cat << "EOF"
   ____ ___ _____   _   _ ____  ____    _ _____ _____ 
  / ___|_ |_   _| | | | |  _ \|  _ \  / | |_   _| ____|
 | |  _ | |  | |   | | | | |_) | | | | | |   | | |  _|  
 | |_| || |  | |   | |_| |  __/| |_| | | |   | | | |___ 
  \____|___| |_|    \___/|_|   |____/  |_|   |_| |_____|
EOF
    echo -e "${COLOR_SECONDARY} ⚡ Git Sync & Deploy Tool • Termux / Linux Edition${COLOR_RESET}"
    echo -e "${COLOR_MUTED}──────────────────────────────────────────────────────────${COLOR_RESET}\n"
}

# Función para animación de carga (Spinner)
run_with_spinner() {
    local pid=$1
    local message=$2
    local spin=('⠋' '⠙' '⠹' '⠸' '⠼' '⠴' '⠦' '⠧' '⠇' '⠏')
    local i=0

    # Ocultar el cursor
    tput civis 2>/dev/null || true

    while kill -0 $pid 2>/dev/null; do
        i=$(( (i + 1) % 10 ))
        echo -ne "\r${COLOR_ACCENT}${spin[$i]}${COLOR_RESET} ${message}..."
        sleep 0.1
    done

    # Restaurar el cursor
    tput cnorm 2>/dev/null || true
    wait $pid
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo -e "\r${COLOR_SUCCESS}✔${COLOR_RESET} ${message} ${COLOR_SUCCESS}completado.${COLOR_RESET}"
    else
        echo -e "\r${COLOR_DANGER}✖${COLOR_RESET} ${message} ${COLOR_DANGER}falló.${COLOR_RESET}"
        return $exit_code
    fi
}

show_banner

# ------------------------------------------------------------------------------
# 1. Cargar o Configurar Usuario
# ------------------------------------------------------------------------------
SAVED_USER=""
if [ -f "$CONFIG_FILE" ]; then
    SAVED_USER=$(grep "^USERNAME=" "$CONFIG_FILE" | cut -d'=' -f2)
fi

if [ -n "$SAVED_USER" ]; then
    echo -e "${COLOR_PRIMARY}[👤 Usuario Detectado]${COLOR_RESET} Actual: ${BOLD}${SAVED_USER}${COLOR_RESET}"
    read -p "$(echo -e ${COLOR_MUTED}"¿Usar este usuario? [S/n]: "${COLOR_RESET})" USE_SAVED
    USE_SAVED=${USE_SAVED:-S}
    if [[ "$USE_SAVED" =~ ^[Ss]$ ]]; then
        USERNAME="$SAVED_USER"
    else
        read -p "$(echo -e ${COLOR_ACCENT}"👤 Nuevo usuario de GitHub: "${COLOR_RESET})" USERNAME
    fi
else
    read -p "$(echo -e ${COLOR_ACCENT}"👤 Usuario de GitHub: "${COLOR_RESET})" USERNAME
fi

# Guardar usuario actualizado en la configuración
echo "USERNAME=$USERNAME" > "$CONFIG_FILE"

# ------------------------------------------------------------------------------
# 2. Selección / Nombre del Repositorio (con Historial)
# ------------------------------------------------------------------------------
CURRENT_DIR=$(basename "$PWD")
echo -e "\n${COLOR_PRIMARY}[📦 Repositorio]${COLOR_RESET}"

SAVED_REPOS=$(grep "^REPO_NAME=" "$CONFIG_FILE" | cut -d'=' -f2 | sort -u)

if [ -n "$SAVED_REPOS" ]; then
    echo -e "${COLOR_MUTED}Historial de repositorios recientes:${COLOR_RESET}"
    select REPO_OPT in $SAVED_REPOS "Otro (Escribir nombre)"; do
        if [ "$REPO_OPT" == "Otro (Escribir nombre)" ]; then
            read -p "$(echo -e ${COLOR_ACCENT}"Ingresa el nombre del repositorio: "${COLOR_RESET})" REPO_NAME
            break
        elif [ -n "$REPO_OPT" ]; then
            REPO_NAME="$REPO_OPT"
            break
        fi
    done
else
    read -p "$(echo -e ${COLOR_ACCENT}"Nombre del repositorio [Por defecto: ${CURRENT_DIR}]: "${COLOR_RESET})" REPO_NAME
    REPO_NAME=${REPO_NAME:-$CURRENT_DIR}
fi

# Guardar repositorio en el historial de configuración si no existe
if ! grep -q "REPO_NAME=$REPO_NAME" "$CONFIG_FILE" 2>/dev/null; then
    echo "REPO_NAME=$REPO_NAME" >> "$CONFIG_FILE"
fi

# ------------------------------------------------------------------------------
# 3. Mensaje del Commit y Autenticación por Token
# ------------------------------------------------------------------------------
echo -e "\n${COLOR_PRIMARY}[💬 Configuración de Cambios]${COLOR_RESET}"
read -p "$(echo -e ${COLOR_MUTED}"Mensaje del commit [Por defecto: 'update']: "${COLOR_RESET})" COMMIT_MSG
COMMIT_MSG=${COMMIT_MSG:-"update"}

echo -e "\n${COLOR_PRIMARY}[🔑 Autenticación]${COLOR_RESET}"
read -sp "$(echo -e ${COLOR_ACCENT}"Ingresa tu Personal Access Token (PAT): "${COLOR_RESET})" TOKEN
echo ""

if [ -z "$TOKEN" ]; then
    echo -e "\n${COLOR_DANGER}Error: El token no puede estar vacío.${COLOR_RESET}"
    exit 1
fi

echo -e "\n${COLOR_MUTED}──────────────────────────────────────────────────────────${COLOR_RESET}"

# ------------------------------------------------------------------------------
# 4. Operaciones de Git con Animaciones
# ------------------------------------------------------------------------------

# Inicialización
if [ ! -d ".git" ]; then
    git init > /dev/null 2>&1
    echo -e "${COLOR_SUCCESS}✔${COLOR_RESET} Repositorio local inicializado."
fi

# Staging y Commit
(git add . && (git status --porcelain | grep -q . && git commit -m "$COMMIT_MSG" || true)) > /dev/null 2>&1 &
run_with_spinner $! "Procesando y commiteando archivos locales"

# Obtener nombre de la rama actual
CURRENT_BRANCH=$(git branch --show-current)
if [ -z "$CURRENT_BRANCH" ]; then
    git branch -M main > /dev/null 2>&1
    CURRENT_BRANCH="main"
fi

# Configuración remota con TOKEN temporal
REMOTE_AUTH_URL="https://${USERNAME}:${TOKEN}@github.com/${USERNAME}/${REPO_NAME}.git"
REMOTE_CLEAN_URL="https://github.com/${USERNAME}/${REPO_NAME}.git"

if git remote | grep -q "^origin$"; then
    git remote set-url origin "$REMOTE_AUTH_URL" > /dev/null 2>&1
else
    git remote add origin "$REMOTE_AUTH_URL" > /dev/null 2>&1
fi

# Pull remoto
(git pull origin "$CURRENT_BRANCH" --allow-unrelated-histories --no-rebase > /dev/null 2>&1) &
run_with_spinner $! "Sincronizando con repositorio remoto ($CURRENT_BRANCH)" || true

# Push remoto
(git push -u origin "$CURRENT_BRANCH" > /dev/null 2>&1) &
run_with_spinner $! "Desplegando cambios a GitHub"

# Limpieza del Token en local por seguridad
git remote set-url origin "$REMOTE_CLEAN_URL" > /dev/null 2>&1

# ------------------------------------------------------------------------------
# 5. Finalización y Resumen
# ------------------------------------------------------------------------------
echo -e "\n${COLOR_MUTED}──────────────────────────────────────────────────────────${COLOR_RESET}"
echo -e "${COLOR_SUCCESS}${BOLD}🎉 ¡OPERACIÓN COMPLETADA CON ÉXITO!${COLOR_RESET}"
echo -e "${COLOR_PRIMARY}👤 Usuario:${COLOR_RESET} $USERNAME"
echo -e "${COLOR_PRIMARY}📦 Repositorio:${COLOR_RESET} $REPO_NAME"
echo -e "${COLOR_PRIMARY}🌿 Rama:${COLOR_RESET} $CURRENT_BRANCH"
echo -e "${COLOR_PRIMARY}🔗 Enlace:${COLOR_RESET} ${COLOR_ACCENT}https://github.com/${USERNAME}/${REPO_NAME}${COLOR_RESET}\n"
