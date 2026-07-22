#!/bin/bash

# --- CONFIGURACIÓN DE COLORES ---
VERDE="\033[1;32m"
CIAN="\033[1;36m"
AMARILLO="\033[1;33m"
ROJO="\033[1;31m"
RESET="\033[0m"

clear
echo -e "${CIAN}=========================================${RESET}"
echo -e "${VERDE}    ⚡ SUBIDA RÁPIDA CON TOKEN GITHUB ⚡  ${RESET}"
echo -e "${CIAN}=========================================${RESET}"

# 1. Pedir tus datos de acceso en tiempo real
echo -e "\n${AMARILLO}🔑 Introduce tus credenciales de GitHub:${RESET}"
read -p "👤 Usuario: " USUARIO
read -p "📦 Nombre del repositorio: " REPO

# Pedir el token ocultando la entrada (no se verá nada mientras escribes)
read -sp "🔑 Pega tu Token de GitHub: " TOKEN
echo -e "\n"

# 2. Inicializar o asegurar la rama main
if [ ! -d ".git" ]; then
    echo -e "${CIAN}🚀 Inicializando repositorio Git local...${RESET}"
    git init
fi
git branch -M main 2>/dev/null

# 3. Añadir archivos y hacer el commit
git add -A
read -p "💬 Mensaje para el commit [Enter para usar por defecto]: " MSG
if [ -z "$MSG" ]; then
    MSG="Actualización desde Termux"
fi
git commit -m "$MSG" --allow-empty

# 4. Configurar la URL remota usando el Token que acabas de escribir
git remote remove origin 2>/dev/null
URL_REMOTA="https://$USUARIO:$TOKEN@github.com/$USUARIO/$REPO.git"
git remote add origin "$URL_REMOTA"

# 5. Subir de golpe
echo -e "\n${VERDE}📤 Subiendo código a GitHub... ¡Espera!${RESET}"
if git push -u origin main; then
    echo -e "\n${VERDE}✔ ¡ÉXITO! Tu script ya está en GitHub sin usar contraseñas viejas. 🎉${RESET}"
else
    echo -e "\n${ROJO}✕ Algo falló. Verifica que el repositorio exista en la web y que tu Token sea el correcto.${RESET}"
fi
echo -e "${CIAN}=========================================${RESET}\n"
