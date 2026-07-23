#!/bin/bash

# ==============================================================================
#  G I T   D E L E T E   P R O
#  Script para eliminar archivos/carpetas de repositorios locales y remotos
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

# Archivo de configuración local compartido
CONFIG_FILE="$HOME/.github_uploader.cfg"

# Banner ASCII para la herramienta de eliminación
show_banner() {
    clear
    echo -e "${COLOR_DANGER}${BOLD}"
    cat << "EOF"
   ____ ___ _____   ____  _____ _     _____ _____ _____ 
  / ___|_ |_   _| |  _ \| ____| |   | ____|_   _| ____|
 | |  _ | |  | |   | | | |  _| | |   |  _|   | | |  _|  
 | |_| || |  | |   | |_| | |___| |___| |___  | | | |___ 
  \____|___| |_|   |____/|_____|_____|_____| |_| |_____|
EOF
    echo -e "${COLOR_SECONDARY} 🗑️  Repository Cleaner & Purge Tool • Termux / Linux${COLOR_RESET}"
    echo -e "${COLOR_MUTED}──────────────────────────────────────────────────────────${COLOR_RESET}\n"
}

# Animación Spinner
run_with_spinner() {
    local pid=$1
    local message=$2
    local spin=('⠋' '⠙' '⠹' '⠸' '⠼' '⠴' '⠦' '⠧' '⠇' '⠏')
    local i=0

    tput civis 2>/dev/null || true

    while kill -0 $pid 2>/dev/null; do
        i=$(( (i + 1) % 10 ))
        echo -ne "\r${COLOR_ACCENT}${spin[$i]}${COLOR_RESET} ${message}..."
        sleep 0.1
    done

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
# 1. Cargar o Configurar Usuario (Persistencia compartida)
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

# Actualizar usuario en configuración
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

if ! grep -q "REPO_NAME=$REPO_NAME" "$CONFIG_FILE" 2>/dev/null; then
    echo "REPO_NAME=$REPO_NAME" >> "$CONFIG_FILE"
fi

# ------------------------------------------------------------------------------
# 3. Selección de Elementos a Eliminar
# ------------------------------------------------------------------------------
echo -e "\n${COLOR_DANGER}[🗑️ Selección de Archivo / Carpeta]${COLOR_RESET}"
read -p "$(echo -e ${COLOR_ACCENT}"Ruta del archivo o carpeta a eliminar: "${COLOR_RESET})" TARGET_PATH

if [ -z "$TARGET_PATH" ]; then
    echo -e "\n${COLOR_DANGER}Error: Debes especificar un archivo o carpeta a eliminar.${COLOR_RESET}"
    exit 1
fi

echo -e "\n${COLOR_PRIMARY}[💬 Mensaje del Commit]${COLOR_RESET}"
read -p "$(echo -e ${COLOR_MUTED}"Mensaje del commit [Por defecto: 'Delete ${TARGET_PATH}']: "${COLOR_RESET})" COMMIT_MSG
COMMIT_MSG=${COMMIT_MSG:-"Delete ${TARGET_PATH}"}

echo -e "\n${COLOR_PRIMARY}[🔑 Autenticación]${COLOR_RESET}"
read -sp "$(echo -e ${COLOR_ACCENT}"Ingresa tu Personal Access Token (PAT): "${COLOR_RESET})" TOKEN
echo ""

if [ -z "$TOKEN" ]; then
    echo -e "\n${COLOR_DANGER}Error: El token no puede estar vacío.${COLOR_RESET}"
    exit 1
fi

echo -e "\n${COLOR_MUTED}──────────────────────────────────────────────────────────${COLOR_RESET}"

# ------------------------------------------------------------------------------
# 4. Procesamiento de Eliminación con Git
# ------------------------------------------------------------------------------

# Verificar si es un repositorio válido
if [ ! -d ".git" ]; then
    echo -e "${COLOR_DANGER}Error: El directorio actual no es un repositorio Git local.${COLOR_RESET}"
    exit 1
fi

# Ejecutar git rm (local e índice)
(git rm -rf "$TARGET_PATH" && git commit -m "$COMMIT_MSG") > /dev/null 2>&1 &
run_with_spinner $! "Removiendo '$TARGET_PATH' e indexando el cambio"

# Obtener rama activa
CURRENT_BRANCH=$(git branch --show-current)
CURRENT_BRANCH=${CURRENT_BRANCH:-"main"}

# Configurar URLs
REMOTE_AUTH_URL="https://${USERNAME}:${TOKEN}@github.com/${USERNAME}/${REPO_NAME}.git"
REMOTE_CLEAN_URL="https://github.com/${USERNAME}/${REPO_NAME}.git"

if git remote | grep -q "^origin$"; then
    git remote set-url origin "$REMOTE_AUTH_URL" > /dev/null 2>&1
else
    git remote add origin "$REMOTE_AUTH_URL" > /dev/null 2>&1
fi

# Sincronizar y Subir cambio de eliminación
(git push origin "$CURRENT_BRANCH" > /dev/null 2>&1) &
run_with_spinner $! "Sincronizando eliminación con GitHub"

# Limpieza de credenciales
git remote set-url origin "$REMOTE_CLEAN_URL" > /dev/null 2>&1

# ------------------------------------------------------------------------------
# 5. Resumen Final
# ------------------------------------------------------------------------------
echo -e "\n${COLOR_MUTED}──────────────────────────────────────────────────────────${COLOR_RESET}"
echo -e "${COLOR_SUCCESS}${BOLD}🎉 ¡ELIMINACIÓN COMPLETADA Y SINCRONIZADA!${COLOR_RESET}"
echo -e "${COLOR_DANGER}❌ Elemento eliminado:${COLOR_RESET} $TARGET_PATH"
echo -e "${COLOR_PRIMARY}📦 Repositorio:${COLOR_RESET} $REPO_NAME"
echo -e "${COLOR_PRIMARY}🌿 Rama:${COLOR_RESET} $CURRENT_BRANCH"
echo -e "${COLOR_PRIMARY}🔗 Enlace:${COLOR_RESET} ${COLOR_ACCENT}https://github.com/${USERNAME}/${REPO_NAME}${COLOR_RESET}\n"
