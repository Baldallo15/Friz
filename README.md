<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=250&section=header&text=Friz%20Universal%20Multi-Downloader&fontSize=50&animation=fadeIn&fontColor=ffffff&desc=Cyberpunk%20Multi-Platform%20Downloader&descColor=00F0FF" alt="Banner Friz">
</div>

<h1 align="center"><img src="https://github.com/Baldallo15/Friz/blob/main/fotos/logotipo.png" alt="Friz Logo" width="64" height="64" align="middle" /> Friz</h1>

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=1000&color=00F0FF&center=true&vCenter=true&width=500&lines=Universal+Multi-Downloader;Windows%2C+Linux+%26+Termux;Open-Source+%26+Free" alt="Typing SVG" />
</div>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/OS-Windows%20%7C%20Linux%20%7C%20Termux-lightgrey?style=for-the-badge&logo=linux" alt="Platforms">
  <img src="https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/github/stars/Baldallo15/Friz_Descargas?style=for-the-badge&color=yellow" alt="Stars">
  <img src="https://img.shields.io/badge/UI-Rich%20Library-purple?style=for-the-badge" alt="UI">
</div>

<br>

<p align="center">
  <b>Friz Universal Multi-Downloader</b> es una herramienta avanzada desarrollada en Python, diseñada para simplificar y acelerar las descargas de archivos desde múltiples fuentes. Con un enfoque en rendimiento, flexibilidad y una interfaz de terminal moderna, es el compañero ideal tanto para entornos de escritorio como móviles.
</p>

<br>

<p align="center">
  <a href="https://github.com/Baldallo15/Friz_Descargas">
    <img src="https://img.shields.io/badge/Fork-Contribute-yellow?style=for-the-badge&logo=github" alt="Fork">
  </a>
  <a href="https://github.com/Baldallo15/Friz_Descargas/issues">
    <img src="https://img.shields.io/github/issues/Baldallo15/Friz_Descargas?style=for-the-badge" alt="Issues">
  </a>
</p>

---

## 📋 Tabla de Contenidos

- [✨ Características Principales](#-características-principales)
- [🎬 Vista Previa](#-vista-previa)
- [📦 Instalación](#-instalación)
  - [Windows](#windows)
  - [Linux](#linux)
  - [Termux (Android)](#termux)
- [🚀 Uso](#-uso)
- [🐛 Correcciones](#-correcciones)
- [🏗️ Arquitectura](#-%EF%B8%8F-arquitectura)
- [🤝 Contribución](#-contribución)
- [📜 Licencia](#-licencia)

---

## ✨ Características Principales

- **🎨 Interfaz Moderna**: Terminal UI con efectos neón, paneles con borde redondeado y animaciones de carga cyberpunk.
- **🌐 Multiplataforma Real**: Funciona a la perfección en **Windows**, **Linux** y **Termux** (Android).
- **⚡ Descargas Optimizadas**: Algoritmos mejorados para maximizar la velocidad de conexión y minimizar fallos.
- **🛡️ 7 Plataformas Soportadas**: YouTube, Spotify, TikTok, Instagram, Facebook, X (Twitter) y Pinterest.
- **🔄 Defensa en Profundidad**: Validación de URL en dos capas (UI + módulo) para mayor seguridad.
- **📊 Progreso en Tiempo Real**: Barras de progreso animadas con spinner cibernético.
- **💾 Gestión Inteligente de Rutas**: Detección automática del sistema operativo y creación de directorio de descargas.
- **🌙 Soporte de Tema**: Detección automática de tema oscuro/claro según la terminal.
- **🐛 Termux Optimizado**: Compatible con xterm-256color, detección automática de entorno TERMUX_VERSION.

---

## 🎬 Vista Previa

<div align="center">
  <img src="fotos/Frizi.png" alt="Demo de Terminal" width="80%">
  <br>
  <i>Interfaz cyberpunk de Friz en acción</i>
</div>

---

## 📦 Instalación

Asegúrate de tener **Git** y **Python 3** instalados en tu sistema antes de comenzar.

### Windows
```bash
git clone https://github.com/Baldallo15/Friz_Descargas.git
cd Friz_Descargas
pip install -r requirements.txt
python friz.py
```

### Linux
```bash
git clone https://github.com/Baldallo15/Friz_Descargas.git
cd Friz_Descargas
pip3 install -r requirements.txt
python3 friz.py
```

### Termux (Android)
```bash
pkg update && pkg upgrade
pkg install git python
git clone https://github.com/Baldallo15/Friz_Descargas.git
cd Friz_Descargas
chmod +x *
bash install.sh
```

---

## 🚀 Uso

Una vez ejecutado el script, simplemente sigue las instrucciones interactivas en pantalla. Selecciona el módulo de plataforma e ingresa la URL objetivo.

**Windows:**
```bash
run_friz.bat
# o
python friz.py
```

**Linux / macOS:**
```bash
./run_friz.sh
# o
python3 friz.py
```

**Termux (Android):**
```bash
friz
# o
python3 friz.py
```

### Plataformas Disponibles

| #  | Plataforma    | Icono |
|----|---------------|-------|
| 1  | YouTube       | 🔴    |
| 2  | Spotify       | 🟢    |
| 3  | TikTok        | 🎵    |
| 4  | Instagram     | 📸    |
| 5  | Facebook      | 🔵    |
| 6  | X (Twitter)   | 🌐    |
| 7  | Pinterest     | 📌    |

---

## 🐛 Correcciones

- **`padding_x` eliminado** en `Table` constructor — parámetro inválido que causaba `TypeError` en tiempo de ejecución. Reemplazado con `expand=True` y `padding` estándar.
- **`_resolve_theme()` corregido** — la lógica siempre devolvía `THEME_DARK` independientemente del terminal. Ahora detecta correctamente soporte de color.
- **Código muerto eliminado** — función `_resolve_style_name()` sin uso fue removida para limpiar el código.
- **`HEAVY_ROUND` eliminado** — estilo de caja no disponible en la versión instalada de `rich`. Reemplazado por `ROUNDED` y `DOUBLE`.
- **`console = Console()`** — configurado para detección automática de terminal en Termux (xterm-256color).

---

## 🏗️ Arquitectura

```
Friz/
├── friz.py              # Punto de entrada principal (UI)
├── README.md            # Documentación del proyecto
├── requirements.txt     # Dependencias de Python
├── pyproject.toml       # Configuración del proyecto
├── install.sh           # Instalador automatizado para Termux
├── .github/workflows/   # CI con GitHub Actions
├── modules/
│   ├── __init__.py      # Paquete de módulos
│   ├── base.py          # Clase base y descargador genérico
│   ├── validator.py     # Validación centralizada de URLs
│   ├── youtube.py       # Módulo YouTube
│   ├── spotify.py       # Módulo Spotify
│   ├── tiktok.py        # Módulo TikTok (limpieza de URL)
│   ├── instagram.py     # Módulo Instagram
│   ├── facebook.py      # Módulo Facebook
│   ├── twitter.py       # Módulo X (Twitter)
│   └── pinterest.py     # Módulo Pinterest
├── scripts/             # Scripts de utilidad
├── tests/               # Suite de pruebas
└── fotos/               # Recursos visuales
```

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto:

1. Haz un *Fork* del repositorio.
2. Crea una rama para tu función (`git checkout -b feature/NuevaFuncion`).
3. Confirma tus cambios (`git commit -m 'Añadir nueva función'`).
4. Sube los cambios (`git push origin feature/NuevaFuncion`).
5. Abre un *Pull Request*.

---

## 📜 Licencia

Este proyecto está bajo la Licencia **MIT**. Consulta el archivo [`LICENSE`](./LICENSE) para más detalles.

---

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" width="100%"/>
  <br>
  <i>Hecho con ❤️ por <a href="https://github.com/Baldallo15">Baldallo15</a></i>
</div>
