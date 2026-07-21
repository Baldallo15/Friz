#!/bin/bash

# --- CONFIGURACIÓN DE COLORES ---
VERDE="\033[1;32m"
CIAN="\033[1;36m"
AMARILLO="\033[1;33m"
ROJO="\033[1;31m"
RESET="\033[0m"

clear
echo -e "${CIAN}=========================================${RESET}"
echo -e "${ROJO}    ELIMINAR ARCHIVO SELECCIONADO        ${RESET}"
echo -e "${CIAN}=========================================${RESET}"

# 1. Pedir datos de GitHub y el archivo
read -p "👤 Usuario de GitHub: " USUARIO
read -p "📦 Nombre del repositorio: " REPO
read -p "📄 Nombre exacto del archivo o carpeta a borrar: " TARGET

if [ -z "$TARGET" ]; then
    echo -e "\n${ROJO}✕ No especificaste ningún archivo. Cancelando...${RESET}\n"
    exit 1
fi

# Pedir el token ocultando la entrada por seguridad
read -sp "🔑 Pega tu Token de GitHub: " TOKEN
echo -e "\n"

# 2. Detectar si es archivo o carpeta para aplicar el parámetro correcto
PARAM_R=""
if [ -d "$TARGET" ]; then
    PARAM_R="-r"
fi

# 3. Preguntar el método (¡Aquí eliges tú!)
echo -e "${CIAN}¿Cómo deseas eliminar '$TARGET'?${RESET}"
echo -e "  ${ROJO}[1]${RESET} Borrar de GitHub Y TAMBIÉN de mi celular"
echo -e "  ${VERDE}[2]${RESET} Borrar SÓLO de GitHub (Conservarlo en mi celular)"
read -p "Selecciona una opción (1-2): " OPCION

case $OPCION in
    1)
        echo -e "\n${ROJO}🗑️ Eliminando de raíz...${RESET}"
        git rm -rf "$TARGET" 2>/dev/null
        rm -rf "$TARGET"
        MSG="Eliminado objeto: $TARGET"
        ;;
    2)
        echo -e "\n${AMARILLO}🛡️ Quitando de GitHub (se queda en tu celular)...${RESET}"
        git rm -rf --cached "$TARGET" 2>/dev/null
        MSG="Removido de GitHub remoto: $TARGET"
        ;;
    *)
        echo -e "\n${ROJO}✕ Opción inválida. Cancelando...${RESET}\n"
        exit 1
        ;;
esac

# 4. Registrar la baja en Git de forma interna
git add -A
git commit -m "$MSG" --allow-empty

# 5. Aplicar la URL con el Token en vivo para que no pida contraseña vieja
git remote remove origin 2>/dev/null
URL_REMOTA="https://$USUARIO:$TOKEN@github.com/$USUARIO/$REPO.git"
git remote add origin "$URL_REMOTA"

# 6. Subir el borrado a GitHub
echo -e "\n${VERDE}📤 Sincronizando baja con GitHub...${RESET}"
if git push origin main; then
    echo -e "\n${VERDE}✔ ¡Listo! Solo el archivo '$TARGET' fue eliminado de GitHub. 🎉${RESET}"
else
    echo -e "\n${ROJO}✕ No se pudo actualizar en GitHub. Verifica tu Token.${RESET}"
fi
echo -e "${CIAN}=========================================${RESET}\n"
