#!/bin/bash

# Script de arranque rápido para Friz
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Verificar si Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado. Ejecuta 'bash install.sh' primero."
    exit 1
fi

# Ejecutar el script Python principal
python3 "$DIR/Friz.py" "$@"
