#!/bin/bash

# --- CONFIGURACIÓN DE COLORES ---
VERDE="\033[1;32m"
CIAN="\033[1;36m"
AMARILLO="\033[1;33m"
ROJO="\033[1;31m"
RESET="\033[0m"

clear
echo -e "${CIAN}=========================================${RESET}"
echo -e "${VERDE}    ASISTENTE DE SUBIDA AUTO-GITHUB      ${RESET}"
echo -e "${CIAN}=========================================${RESET}"

# 1. Solicitar credenciales si no están configuradas globalmente
echo -e "\n${AMARILLO}🔑 Configurando tus datos de GitHub...${RESET}"
read -p "Introduce tu nombre de usuario de GitHub: " USUARIO
read -p "Introduce tu correo de GitHub: " CORREO
read -sp "Pega tu Token de GitHub (no se verá en pantalla): " TOKEN
echo ""

git config --global user.name "$USUARIO"
git config --global user.email "$CORREO"

# 2. Solicitar datos del repositorio
echo -e "\n${AMARILLO}📦 Configurando el repositorio...${RESET}"
read -p "Introduce el nombre del repositorio (ej. friz-downloader): " REPO

# 3. Inicializar Git y preparar archivos
echo -e "\n${CIAN}🚀 Inicializando repositorio local...${RESET}"
if [ ! -d ".git" ]; then
    git init
    git branch -M main
fi

git add .
read -p "Introduce el mensaje del commit [Por defecto: Actualización Friz]: " REPO_MSG
if [ -z "$REPO_MSG" ]; then
    REPO_MSG="Actualización Friz"
fi

git commit -m "$REPO_MSG"

# 4. Vincular el repositorio remoto de forma segura con el Token incrustado
echo -e "\n${CIAN}🔗 Vinculando con GitHub remoto...${RESET}"
# Eliminamos el origin viejo por si ya existía para evitar errores
git remote remove origin 2>/dev/null

# Esta URL mágica auto-autentica tu sesión sin pedirte contraseña en el push
URL_REMOTA="https://$USUARIO:$TOKEN@github.com/$USUARIO/$REPO.git"
git remote add origin "$URL_REMOTA"

# 5. Subir los archivos
echo -e "\n${VERDE}📤 Subiendo archivos a GitHub... ¡Espera un momento!${RESET}"
if git push -u origin main; then
    echo -e "\n${VERDE}✔ ¡ÉXITO ROTUNDO! Tus archivos ya están en GitHub. 🎉${RESET}"
else
    echo -e "\n${ROJO}✕ Vaya, algo salió mal. Revisa que el repositorio web esté creado y que tu Token tenga permisos de 'repo'.${RESET}"
fi
echo -e "${CIAN}=========================================${RESET}\n"
