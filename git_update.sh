#!/bin/bash

# ======================================================
# Script para subir proyectos a GitHub usando Username + PAT
# ======================================================

set -e # Detener ejecución si ocurre un error inesperado

# 1. Solicitar datos de entrada
read -p "👤 Usuario de GitHub: " USERNAME
read -sp "🔑 Personal Access Token (PAT): " TOKEN
echo ""
read -p "📦 Nombre del repositorio en GitHub: " REPO_NAME
read -p "💬 Mensaje del commit [Por defecto: 'Initial commit']: " COMMIT_MSG

# Asignar mensaje por defecto si se deja en blanco
COMMIT_MSG=${COMMIT_MSG:-"Initial commit"}

# 2. Inicializar Git si no existe en el directorio actual
if [ ! -d ".git" ]; then
    echo "📌 Inicializando repositorio Git local..."
    git init
fi

# 3. Preparar archivos y hacer commit
echo "📂 Agregando archivos al staging..."
git add .

# Verificar si hay cambios pendientes por commitear
if git status --porcelain | grep -q .; then
    echo "📝 Creando commit..."
    git commit -m "$COMMIT_MSG"
else
    echo "ℹ️ No hay cambios nuevos para commitear. Continuando..."
fi

# 4. Obtener la rama actual activamente (evita errores entre master/main)
CURRENT_BRANCH=$(git branch --show-current)

# Si por alguna razón la rama no tiene nombre todavía, asignar 'main' por defecto
if [ -z "$CURRENT_BRANCH" ]; then
    git branch -M main
    CURRENT_BRANCH="main"
fi

# 5. Configurar la URL del remoto usando la autenticación por TOKEN
REMOTE_AUTH_URL="https://${USERNAME}:${TOKEN}@github.com/${USERNAME}/${REPO_NAME}.git"
REMOTE_CLEAN_URL="https://github.com/${USERNAME}/${REPO_NAME}.git"

if git remote | grep -q "^origin$"; then
    echo "🔄 Actualizando la URL del remoto 'origin'..."
    git remote set-url origin "$REMOTE_AUTH_URL"
else
    echo "🔗 Añadiendo remoto 'origin'..."
    git remote add origin "$REMOTE_AUTH_URL"
fi

# 6. Subir repositorio a GitHub detectando la rama dinámica
echo "🚀 Subiendo cambios a GitHub en la rama '$CURRENT_BRANCH'..."
git push -u origin "$CURRENT_BRANCH"

# 7. Limpieza de seguridad: quitar el Token del remoto guardado
git remote set-url origin "$REMOTE_CLEAN_URL"

echo ""
echo "✅ ¡Proceso completado con éxito!"
echo "🔗 Repositorio disponible en: https://github.com/${USERNAME}/${REPO_NAME}"
