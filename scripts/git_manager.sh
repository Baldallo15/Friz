#!/bin/bash

# ==============================================================================
#  G I T   M A N A G E R   P R O  •  Ultra Fast & Versatile CLI (Main Branch)
# ==============================================================================

# Limpiar posibles saltos de línea incompatibles (CRLF de Windows)
if [ -f "$0" ]; then
    sed -i -e 's/\r$//' "$0" 2>/dev/null || true
fi

COLOR_RESET="\033[0m"
COLOR_PRIMARY="\033[38;5;39m"
COLOR_SECONDARY="\033[38;5;141m"
COLOR_ACCENT="\033[38;5;214m"
COLOR_SUCCESS="\033[38;5;82m"
COLOR_MUTED="\033[38;5;244m"
COLOR_DANGER="\033[38;5;196m"
BOLD="\033[1m"

CONFIG_FILE="$HOME/.github_uploader.cfg"
CURRENT_DIR=$(basename "$PWD")

show_banner() {
    clear
    echo -e "${COLOR_PRIMARY}${BOLD}   ____ ___ _____   __  __                             "
    echo -e "  / ___|_ |_   _| |  \/  | __ _ _ __   __ _  __ _  ___ _ __ "
    echo -e " | |  _ | |  | |   | |\/| |/ _\` | '_ \ / _\` |/ _\` |/ _ \ '__|"
    echo -e " | |_| || |  | |   | |  | | (_| | | | | (_| | (_| |  __/ |   "
    echo -e "  \____|___| |_|   |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|   "
    echo -e "                                             |___/           ${COLOR_RESET}"
    echo -e "${COLOR_SECONDARY} ⚡ Git Turbo Manager • Termux / Linux${COLOR_RESET}"
    echo -e "${COLOR_MUTED}──────────────────────────────────────────────────────────${COLOR_RESET}\n"
}

run_with_spinner() {
    local pid=$1
    local message=$2
    local spin=('⠋' '⠙' '⠹' '⠸' '⠼' '⠴' '⠦' '⠧' '⠇' '⠏')
    local i=0
    tput civis 2>/dev/null || true
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i + 1) % 10 ))
        echo -ne "\r${COLOR_ACCENT}${spin[$i]}${COLOR_RESET} ${message}..."
        sleep 0.08
    done
    tput cnorm 2>/dev/null || true
    wait $pid
    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo -e "\r${COLOR_SUCCESS}✔${COLOR_RESET} ${message} ${COLOR_SUCCESS}OK.${COLOR_RESET}"
    else
        echo -e "\r${COLOR_DANGER}✖${COLOR_RESET} ${message} ${COLOR_DANGER}Error.${COLOR_RESET}"
        return $exit_code
    fi
}

show_banner

# ------------------------------------------------------------------------------
# 1. Menú de Acción Principal
# ------------------------------------------------------------------------------
echo -e "${COLOR_PRIMARY}[🎯 ¿Qué deseas hacer hoy?]${COLOR_RESET}"
echo -e "  ${COLOR_ACCENT}1)${COLOR_RESET} Subir / Actualizar cambios (Push a main)"
echo -e "  ${COLOR_ACCENT}2)${COLOR_RESET} Eliminar archivo o carpeta del repositorio"
read -p "$(echo -e ${COLOR_MUTED}"Selecciona una opción [1/2, Por defecto: 1]: "${COLOR_RESET})" ACTION_OPT
ACTION_OPT=${ACTION_OPT:-1}

# ------------------------------------------------------------------------------
# 2. Cargar Usuario (Caché)
# ------------------------------------------------------------------------------
SAVED_USER=""
[ -f "$CONFIG_FILE" ] && SAVED_USER=$(grep "^USERNAME=" "$CONFIG_FILE" | cut -d'=' -f2)

if [ -n "$SAVED_USER" ]; then
    read -p "$(echo -e ${COLOR_ACCENT}"👤 Usuario [${SAVED_USER}] (Enter para usar / Escribe otro): "${COLOR_RESET})" USERNAME
    USERNAME=${USERNAME:-$SAVED_USER}
else
    read -p "$(echo -e ${COLOR_ACCENT}"👤 Usuario de GitHub: "${COLOR_RESET})" USERNAME
fi
echo "USERNAME=$USERNAME" > "$CONFIG_FILE"

# ------------------------------------------------------------------------------
# 3. Nombre del Repositorio o URL Completa
# ------------------------------------------------------------------------------
echo -e "\n${COLOR_PRIMARY}[📦 Repositorio]${COLOR_RESET}"
read -p "$(echo -e ${COLOR_ACCENT}"Pega la URL del repo o escribe el nombre [Por defecto: ${CURRENT_DIR}]: "${COLOR_RESET})" REPO_INPUT

if [ -z "$REPO_INPUT" ]; then
    REPO_NAME="$CURRENT_DIR"
elif [[ "$REPO_INPUT" == *"github.com"* ]]; then
    REPO_NAME=$(basename "$REPO_INPUT" .git)
else
    REPO_NAME="$REPO_INPUT"
fi

# ------------------------------------------------------------------------------
# 4. Acciones Específicas
# ------------------------------------------------------------------------------
if [ "$ACTION_OPT" == "2" ]; then
    echo -e "\n${COLOR_DANGER}[🗑️ Eliminación]${COLOR_RESET}"
    read -p "$(echo -e ${COLOR_ACCENT}"Ruta del archivo/carpeta a borrar: "${COLOR_RESET})" TARGET_PATH
    [ -z "$TARGET_PATH" ] && { echo -e "${COLOR_DANGER}Ruta vacía. Saliendo.${COLOR_RESET}"; exit 1; }
    
    read -p "$(echo -e ${COLOR_MUTED}"Mensaje de commit [Por defecto: 'Delete ${TARGET_PATH}']: "${COLOR_RESET})" COMMIT_MSG
    COMMIT_MSG=${COMMIT_MSG:-"Delete ${TARGET_PATH}"}
else
    echo -e "\n${COLOR_PRIMARY}[💬 Sincronización]${COLOR_RESET}"
    read -p "$(echo -e ${COLOR_MUTED}"Mensaje de commit [Por defecto: 'update']: "${COLOR_RESET})" COMMIT_MSG
    COMMIT_MSG=${COMMIT_MSG:-"update"}
fi

# ------------------------------------------------------------------------------
# 5. Token Rápido
# ------------------------------------------------------------------------------
echo -e "\n${COLOR_PRIMARY}[🔑 Autenticación]${COLOR_RESET}"
read -sp "$(echo -e ${COLOR_ACCENT}"Personal Access Token (PAT): "${COLOR_RESET})" TOKEN
echo ""
[ -z "$TOKEN" ] && { echo -e "${COLOR_DANGER}Token requerido.${COLOR_RESET}"; exit 1; }

echo -e "\n${COLOR_MUTED}──────────────────────────────────────────────────────────${COLOR_RESET}"

# ------------------------------------------------------------------------------
# 6. Ejecución Optimizada de Git
# ------------------------------------------------------------------------------
[ ! -d ".git" ] && { git init > /dev/null 2>&1; echo -e "${COLOR_SUCCESS}✔${COLOR_RESET} Repo local inicializado."; }

git branch -M main > /dev/null 2>&1
TARGET_BRANCH="main"

REMOTE_AUTH_URL="https://${USERNAME}:${TOKEN}@github.com/${USERNAME}/${REPO_NAME}.git"
REMOTE_CLEAN_URL="https://github.com/${USERNAME}/${REPO_NAME}.git"

if git remote | grep -q "^origin$"; then
    git remote set-url origin "$REMOTE_AUTH_URL" > /dev/null 2>&1
else
    git remote add origin "$REMOTE_AUTH_URL" > /dev/null 2>&1
fi

LOG_FILE=$(mktemp)

if [ "$ACTION_OPT" == "2" ]; then
    (git rm -rf "$TARGET_PATH" && git commit -m "$COMMIT_MSG") > "$LOG_FILE" 2>&1 &
    run_with_spinner $! "Eliminando e indexando archivos"
else
    (git add . && (git status --porcelain | grep -q . && git commit -m "$COMMIT_MSG" || true)) > "$LOG_FILE" 2>&1 &
    run_with_spinner $! "Empaquetando y commiteando cambios"

    (git pull origin "$TARGET_BRANCH" --allow-unrelated-histories --no-rebase > "$LOG_FILE" 2>&1) &
    run_with_spinner $! "Sincronizando con remoto ($TARGET_BRANCH)" || true
fi

# Intentar PUSH
(git push -u origin "$TARGET_BRANCH" > "$LOG_FILE" 2>&1) &
run_with_spinner $! "Desplegando en GitHub ($TARGET_BRANCH)"
PUSH_STATUS=$?

git remote set-url origin "$REMOTE_CLEAN_URL" > /dev/null 2>&1

# ------------------------------------------------------------------------------
# 7. Resumen y Depuración
# ------------------------------------------------------------------------------
echo -e "\n${COLOR_MUTED}──────────────────────────────────────────────────────────${COLOR_RESET}"

if [ $PUSH_STATUS -eq 0 ]; then
    echo -e "${COLOR_SUCCESS}${BOLD}🎉 ¡OPERACIÓN EXITOSA!${COLOR_RESET}"
    echo -e "${COLOR_PRIMARY}📦 Repo:${COLOR_RESET} $REPO_NAME (${COLOR_MUTED}$TARGET_BRANCH${COLOR_RESET})"
    echo -e "${COLOR_PRIMARY}🔗 Enlace:${COLOR_RESET} ${COLOR_ACCENT}https://github.com/${USERNAME}/${REPO_NAME}${COLOR_RESET}\n"
else
    echo -e "${COLOR_DANGER}${BOLD}❌ FALLÓ LA OPERACIÓN CON GITHUB${COLOR_RESET}"
    echo -e "${COLOR_MUTED}Detalle técnico del error registrado por Git:${COLOR_RESET}\n"
    echo -e "${COLOR_DANGER}"
    cat "$LOG_FILE"
    echo -e "${COLOR_RESET}\n"
fi

rm -f "$LOG_FILE"
