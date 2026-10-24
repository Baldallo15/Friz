@echo off
chcp 65001 >nul
title Friz - Instalador para Windows
echo.
echo    ███████╗██████╗ ██╗███████╗
echo    ██╔════╝██╔══██╗██║╚══███╔╝
echo    █████╗  ██████╔╝██║  ███╔╝ 
echo    ██╔══╝  ██╔══██╗██║ ███╔╝  
echo    ██║     ██║  ██║███████╗
echo    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝
echo.
echo    Instalador para Windows 7/8/10/11
echo.

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python no encontrado. Instala Python 3.8+ desde https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Actualizando pip...
python -m pip install --upgrade pip

echo [2/4] Instalando dependencias...
pip install -r requirements.txt

echo [3/4] Creando carpeta de descargas...
if not exist "%USERPROFILE%\Downloads\Friz" mkdir "%USERPROFILE%\Downloads\Friz"

echo [4/4] Listo!
echo.
echo Instalación completada. Para ejecutar Friz:
echo   run_friz.bat
echo   o
echo   python friz.py
echo.
pause
