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

Toda la música, videos e imágenes se organizan de forma automática directamente en la carpeta física de tu teléfono dentro de `Download/Friz/`.

---

## 🔥 Plataformas e Inyecciones Soportadas

| Plataforma | Tipo de Contenido | ¿Sin Marca de Agua? | Calidad Máxima |
| :--- | :--- | :---: | :---: |
| **Spotify** | Pistas / Álbumes (Metadatos completos) | ✔ N/A | Hasta 320 kbps |
| **YouTube** | Audio (MP3) / Video (MP4) | ✔ Sí | Full HD / 320 kbps |
| **TikTok** | Videos / Audios de fondo | ✔ **Sí (Nativo)** | Calidad de Origen |
| **Instagram** | Reels / Fotos | ✔ Sí | Calidad de Origen |
| **Facebook** | Videos / Shorts | ✔ Sí | HD |
| **X (Twitter)** | Videos | ✔ Sí | Calidad de Origen |
| **Pinterest** | Imágenes / Pines estáticos | ✔ Sí | Alta Resolución |

---

## 🛠️ Métodos de Instalación

Elige el método que prefieras para configurar tu entorno en Termux.

### MÉTODOS 1: Instalación Express Semiatomática (Recomendado) 🚀
Copia y pega la siguiente línea en tu terminal para clonar el repositorio e iniciar el asistente de configuración automatizado:

```bash
pkg install git -y && git clone [https://github.com/Baldallo15/Friz_Descargas.git](https://github.com/Baldallo15/Friz_Descargas.git) && cd Friz_Descargas && bash install.sh
