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
    git branch -M main
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

# 4. Configurar la URL del remoto usando la autenticación por TOKEN
REMOTE_URL="https://${TOKEN}@github.com/${USERNAME}/${REPO_NAME}.git"

if git remote | grep -q "^origin$"; then
    echo "🔄 Actualizando la URL del remoto 'origin'..."
    git remote set-url origin "$REMOTE_URL"
else
    echo "🔗 Añadiendo remoto 'origin'..."
    git remote add origin "$REMOTE_URL"
fi

# 5. Subir repositorio a GitHub
echo "🚀 Subiendo cambios a GitHub..."
git push -u origin main

echo ""
echo "✅ ¡Proceso completado con éxito!"
echo "🔗 Repositorio disponible en: https://github.com/${USERNAME}/${REPO_NAME}"
