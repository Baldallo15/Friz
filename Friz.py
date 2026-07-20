#Friz V1.1.0

import os
import subprocess
from yt_dlp import YoutubeDL

# --- COLORES ANSI PARA LA TERMINAL ---
VERDE = "\033[1;32m"
AZUL = "\033[1;34m"
CIAN = "\033[1;36m"
AMARILLO = "\033[1;33m"
ROJO = "\033[1;31m"
MAGENTA = "\033[1;35m"
RESET = "\033[0m"
NEGrita = "\033[1m"

# --- CONFIGURACIÓN PREVIA PARA TERMUX ---
try:
    ruta_friz = "/sdcard/Download/Friz"
    if not os.path.exists(ruta_friz):
        os.makedirs(ruta_friz)
    os.chdir(ruta_friz)
except Exception as e:
    print(f"{ROJO}✕ No se pudo acceder o crear /sdcard/Download/Friz ({e}).{RESET}")
    print(f"{AMARILLO}⚠ Se guardará en la carpeta local de Termux.{RESET}")

def limpiar_pantalla():
    os.system('clear')

def banner():
    print(f"{CIAN}╔════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CIAN}║{VERDE}{NEGrita}     __     _        ____                             {CIAN}║{RESET}")
    print(f"{CIAN}║{VERDE}{NEGrita}    / /_ __(_)__    / __ \___ _    ______  ___  ___ _ {CIAN}║{RESET}")
    print(f"{CIAN}║{VERDE}{NEGrita}   / __/ // / /_   / /_/ / _ \ | |/ / __ \/ _ \/ _ `/ {CIAN}║{RESET}")
    print(f"{CIAN}║{VERDE}{NEGrita}  /_/  \_,_/_/(_) /_____/\___/|___/_/ /_/_//_/\_, /  {CIAN}║{RESET}")
    print(f"{CIAN}║{VERDE}{NEGrita}                                             /___/   {CIAN}║{RESET}")
    print(f"{CIAN}║{AMARILLO}             ★ Hacking_V3nezuela ★             {CIAN}║{RESET}")
    print(f"{CIAN}╚════════════════════════════════════════════════════════╝{RESET}")
    print(f"{AZUL}📂 Destino:{RESET} {VERDE}{os.getcwd()}{RESET}")
    print(f"{CIAN}----------------------------------------------------------{RESET}")

def descargar_youtube(url, calidad):
    print(f"\n{AMARILLO}🚀 [Procesando descarga desde YouTube...]{RESET}")
    
    calidades_yt = {"1": "320", "2": "192", "3": "128"}
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': calidades_yt.get(calidad, '192'),
        }],
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': False, # Muestra el progreso nativo de yt-dlp que ya es bastante estético
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n{VERDE}✔ ¡ÉXITO! Canción de YouTube guardada en Download/Friz 🎉{RESET}")
    except Exception as e:
        print(f"\n{ROJO}✕ Error crítico en YouTube: {e}{RESET}")

def descargar_spotify(url, calidad):
    print(f"\n{MAGENTA}🎵 [Iniciando puente Spotify ➔ YouTube...]{RESET}")
    print(f"{AMARILLO}ℹ Buscando metadatos, carátula e igualando pistas...{RESET}")
    
    calidades_spot = {"1": "320k", "2": "192k", "3": "128k"}
    bitrate = calidades_spot.get(calidad, "192k")
    
    comando = ["python3.11", "-m", "spotdl", "download", url, "--bitrate", bitrate]
    
    try:
        # Ejecutamos permitiendo que spotdl muestre su hermosa barra de progreso nativa
        resultado = subprocess.run(comando, check=True)
        if resultado.returncode == 0:
            print(f"\n{VERDE}✔ ¡ÉXITO! Spotify track guardado con carátula en Download/Friz 🎧{RESET}")
    except Exception as e:
        print(f"\n{ROJO}✕ Error crítico en Spotify: {e}{RESET}")

def menu():
    while True:
        limpiar_pantalla()
        banner()
        
        print(f"{NEGrita}Selecciona tu plataforma multimedia:{RESET}\n")
        print(f"  {ROJO}[1]{RESET} YouTube Audio  {ROJO}➔{RESET} {AMARILLO}📹{RESET}")
        print(f"  {VERDE}[2]{RESET} Spotify Tracks {VERDE}➔{RESET} {AMARILLO}🎵{RESET}")
        print(f"  {CIAN}[3]{RESET} Salir del Script {CIAN}➔{RESET} {ROJO}❌{RESET}")
        
        opcion = input(f"\n{NEGrita}{CIAN}⚡ Friz-Downloader » {RESET}").strip()
        
        if opcion == "3":
            print(f"\n{AMARILLO}👋 ¡Gracias por usar Friz-Downloader! Saliendo...{RESET}\n")
            break
            
        if opcion not in ["1", "2"]:
            print(f"\n{ROJO}⚠ Opción inválida. Intenta de nuevo.{RESET}")
            input(f"{AZUL}Presiona Enter para continuar...{RESET}")
            continue
            
        url = input(f"\n{NEGrita}{AMARILLO}🔗 Pega el enlace (URL): {RESET}").strip()
        if not url:
            print(f"{ROJO}⚠ El enlace no puede estar vacío.{RESET}")
            input(f"{AZUL}Presiona Enter...{RESET}")
            continue
            
        limpiar_pantalla()
        banner()
        print(f"{NEGrita}Ajusta la fidelidad del archivo de audio:{RESET}\n")
        print(f"  {CIAN}[1]{RESET} Alta fidelidad  {VERDE}(320 kbps - Pesado){RESET}")
        print(f"  {CIAN}[2]{RESET} Calidad Estándar {AMARILLO}(192 kbps - Recomendado){RESET}")
        print(f"  {CIAN}[3]{RESET} Calidad Ahorro   {ROJO}(128 kbps - Ligero){RESET}")
        
        calidad = input(f"\n{NEGrita}{CIAN}⚡ Calidad (1-3) [Defecto 2] » {RESET}").strip()
        if calidad not in ["1", "2", "3"]:
            calidad = "2"
            
        if opcion == "1":
            descargar_youtube(url, calidad)
        elif opcion == "2":
            descargar_spotify(url, calidad)
            
        print(f"\n{CIAN}----------------------------------------------------------{RESET}")
        input(f"{AZUL}⌨ Presiona Enter para volver al menú principal...{RESET}")

if __name__ == "__main__":
    menu()
