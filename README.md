# 🎵 Friz — Universal Multi-Downloader (Termux Edition) 🚀

<p align="center">
  <img src="fotos/Frizi.png" alt="Friz Logo" width="600">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Termux%20%7C%20Android-green?style=for-the-badge&logo=android" alt="Platform">
  <img src="https://img.shields.io/badge/Language-Python%203-blue?style=for-the-badge&logo=python" alt="Language">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

---

Un script interactivo y optimizado en Python diseñado específicamente para **Termux (Android)**. Con **Friz**, puedes extraer y descargar contenido multimedia de casi cualquier red social sin limitaciones de velocidad y libre de marcas de agua. 

Toda la música, videos e imágenes se organizan de forma automática directamente en el almacenamiento interno de tu teléfono dentro de `Download/Friz/`.

---

## 🔥 Plataformas e Inyecciones Soportadas

| Plataforma | Tipo de Contenido | ¿Sin Marca de Agua? | Calidad Máxima |
| :--- | :--- | :---: | :---: |
| **Spotify** | Pistas / Álbumes (Metadatos completos) | ✔️ N/A | Hasta 320 kbps |
| **YouTube** | Audio (MP3) / Video (MP4) | ✔️ Sí | Full HD / 320 kbps |
| **TikTok** | Videos / Audios de fondo | ✔️ **Sí (Nativo)** | Calidad de Origen |
| **Instagram** | Reels / Fotos | ✔️ Sí | Calidad de Origen |
| **Facebook** | Videos / Shorts | ✔️ Sí | HD |
| **X (Twitter)** | Videos | ✔️ Sí | Calidad de Origen |
| **Pinterest** | Imágenes / Pines estáticos | ✔️ Sí | Alta Resolución |

---

## ⚡ Instalación Rápida (Recomendado)

Ejecuta este comando único en tu terminal de Termux para clonar el repositorio e iniciar el asistente de configuración automatizado:

```bash
pkg update && pkg upgrade -y && pkg install git -y && git clone https://github.com/Baldallo15/Friz_Descargas.git && cd Friz_Descargas && bash install.sh```


📅 Historial de Versiones
​<details>
<summary><b>🔄 Haz clic aquí para desplegar el registro de cambios (Changelog)</b></summary>

​### 🚀 v1.2.2 (Versión Actual)
​
Script de Instalación Automatizado (install.sh): Configuración en un solo comando de todas las dependencias de Termux, Python y FFmpeg.
​Lanzador Global (friz): Creación automática del ejecutable global en el sistema para poder arrancar el script escribiendo únicamente friz desde cualquier directorio.
​Script de Arranque (friz.sh): Añadido script lanzador ligero con comprobación automática de entorno.
​Directorio Automatizado: Creación y vinculación automática de la carpeta física /sdcard/Download/Friz/.

​### ⚡ v1.2.0
​
Compatibilidad Absoluta: Migración a sys.executable para prevenir cierres imprevistos al actualizar la versión de Python en Termux.
​Módulo Universal: Integración refinada de yt-dlp para descargas sin marca de agua en TikTok, Instagram, Facebook, X y Pinterest.
​Ruta Dinámica: Sustitución de rutas estáticas forzadas por rutas lógicas basadas en $HOME y el almacenamiento público de Android.

​### ⚙️ v1.1.0
​Rediseño estético del banner ANSI optimizado para entornos de terminal oscura.
​Estructuración del guardado automático unificado en la ruta /sdcard/Download/Friz/.
​Corrección en el bitrate nativo de conversión para transmisiones de Spotify.

​### 🌟 v1.0.0

​Lanzamiento inicial del script base.
​Soporte dedicado para enlaces individuales de YouTube y Spotify a 192kbps.

​</details>
​<p align="center">
<b>¡GRACIAS POR USAR FRIZ! ❤️ 🇻🇪</b>
</p>
