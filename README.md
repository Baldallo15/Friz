# 🎵 Friz - Multi Downloader (Termux Edition) 🚀

Un script interactivo en Python diseñado específicamente para **Termux (Android)** que permite descargar música de **Spotify** y **YouTube** en distintas calidades de audio (`128kbps`, `192kbps` y `320kbps`). 

Toda la música descargada se organiza automáticamente en la carpeta de almacenamiento de tu teléfono dentro de `Download/Friz/`.

---

## 🛠️ Requisitos e Instalación en Termux

Abre tu aplicación Termux y ejecuta los siguientes comandos en orden secuencial. 

### 1. Preparación del Sistema y Almacenamiento
Consiste en dar permisos de almacenamiento a Termux para guardar los archivos y actualizar los paquetes internos.
```bash
termux-setup-storage
pkg update && pkg upgrade -y

```
Instalación de Dependencias del Sistema 😎

Instalamos el repositorio de paquetes estables, la versión recomendada de Python (3.11), el procesador de audio FFmpeg y herramientas de compilación para evitar errores de compatibilidad.
```
pkg install tur-repo -y
pkg install python3.11 ffmpeg build-essential rust -y
```

Instalación de Librerías de Descarga (Python)📜📚

Configuramos las variables del sistema Android y descargamos los motores principales (yt-dlp y spotdl) directamente en el entorno aislado de Python 3.11

```
export ANDROID_API_LEVEL=24
python3.11 -m pip install --upgrade pip setuptools wheel
python3.11 -m pip install yt-dlp spotdl
```

