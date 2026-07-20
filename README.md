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
