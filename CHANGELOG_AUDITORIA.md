# Changelog — Correcciones aplicadas según la Auditoría Técnica

Este documento resume, punto por punto, todos los cambios aplicados al
proyecto a partir de `Auditoria_Friz_Descargas.md`. Cada entrada indica
el archivo modificado y la sección de la auditoría a la que responde.

## 🔴 Prioridad Alta

- **`friz.py`** — Resuelto el conflicto de merge de Git sin resolver
  (`<<<<<<< HEAD` / `=======` / `>>>>>>>`) que impedía que el programa
  compilara. Verificado con `python -m py_compile`. *(Sección 4.1)*
- **`.github/workflows/ci.yml`** — Añadido pipeline de CI con prueba de
  humo (`py_compile`), lint (`ruff`) y `pytest` en cada push/PR a
  `main`, para que un fallo como el anterior sea detectado
  automáticamente antes de llegar a producción. *(Sección 4.1 / 5.2)*
- **`modules/tiktok.py`** — Eliminado el flag `--no-check-certificates`
  que deshabilitaba la verificación de certificados TLS. *(Sección 4.2)*
- **`modules/base.py`** — Añadido el método `download_seguro()` en
  `BaseDownloader`, que vuelve a validar la URL contra
  `modules/validator.py` dentro de cada descargador (defensa en
  profundidad), y `friz.py` ahora lo invoca en vez de llamar a
  `download()` directamente. *(Sección 4.3)*

## 🟠 Prioridad Media

- **`modules/pinterest.py`** — Corregida la indentación irregular (3
  espacios) y la línea "fantasma" con espacios sueltos. *(Sección 3.4 / 4.4)*
- **`modules/base.py`** — Nueva clase `YtDlpDownloader`, plantilla
  reutilizable que centraliza la lógica común a las 5 plataformas
  basadas en `yt-dlp`. **`youtube.py`, `instagram.py`, `facebook.py`,
  `twitter.py` y `pinterest.py`** se reescribieron para heredar de
  ella, reduciéndose cada uno a ~5 líneas y eliminando la duplicación
  de código. `tiktok.py` sobreescribe `limpiar_url()` para conservar su
  lógica de limpieza de parámetros de rastreo. *(Sección 4.4)*
- **`requirements.txt`** — Fijadas las versiones de todas las
  dependencias con rangos explícitos. Eliminadas `colorama`, `pillow`,
  `certifi`, `urllib3` y `requests`, confirmadas como no utilizadas en
  ningún archivo `.py` del proyecto (verificado con `grep` recursivo).
  *(Sección 4.5)*
- **`LICENSE`** — Creado el archivo de licencia MIT que el README ya
  declaraba pero que no existía en el repositorio. *(Sección 1 / 3.4)*

## 🟡 Prioridad Baja

- **`.gitignore`** — Creado; excluye `__pycache__/`, entornos
  virtuales, logs y artefactos de empaquetado. *(Sección 4.6)*
- **`.gitattributes`** — Creado; enruta `fotos/*.mp4` y `fotos/*.png` a
  Git LFS para no seguir inflando el historial del repositorio con
  binarios pesados. *(Sección 3.3 / 4.6)*
- **`README.md`** — Corregidos todos los errores de codificación de
  caracteres detectados (*"Caracterasticas"* → *"Características"*,
  *"Instalaci9n"* → *"Instalación"*, *"estqs"* → *"estás"*, *"bqsico"*
  → *"básico"*, *"estÃ¡"* → *"está"*, tildes faltantes en
  *"Contribución"*, *"múltiples"*, *"móviles"*, *"función"*, y el
  carácter de cedilla corrupto en el pie de página). Corregido también
  el comando de ejecución, que indicaba erróneamente `python main.py`
  en vez de `python friz.py`, y se añadió el paso `pip install -r
  requirements.txt` que faltaba antes de ejecutar el script.
  *(Sección 3.4)*
- **`install.sh`** — Corregido el carácter cirílico corrupto
  ("Androчid" → "Android") en el comentario de cabecera. *(Sección 3.4)*
- **`modules/__pycache__/`** — Eliminado del árbol de archivos (ya no
  debe versionarse gracias al nuevo `.gitignore`). *(Sección 4.6)*

## 🟢 Roadmap aplicado parcialmente (testing y CI/CD)

- **`tests/test_validator.py`** — Nueva suite de pruebas unitarias
  (16 casos) para `modules/validator.py`, el módulo con lógica pura
  identificado en la auditoría como el más sencillo de cubrir sin
  mocks de red. Verificados manualmente en este entorno (sin acceso a
  red para instalar `pytest`); el workflow de CI los ejecutará con
  `pytest` de forma automática en cada push. *(Sección 3.5 / 5.2)*

## Mejoras adicionales no listadas explícitamente en el checklist

- **`modules/base.py`** — Añadido logging estructurado (`logging`,
  archivo rotativo en `~/.friz/logs/friz.log`) en paralelo a la UI de
  `rich`, para poder depurar fallos reportados por usuarios sin
  depender solo de lo mostrado en pantalla.
- **`modules/base.py`** — El manejo de excepciones en
  `ejecutar_comando_animado()` ahora distingue `FileNotFoundError`
  (binario externo no instalado) de `subprocess.SubprocessError`, en
  vez de capturar `Exception` genérica, dando mensajes más accionables
  al usuario.
- **`friz.py`** — Añadido manejo específico de `KeyboardInterrupt`
  para que `Ctrl+C` durante una descarga no se reporte como un "error
  no controlado".
- Añadidos docstrings a `BaseDownloader`, `YtDlpDownloader` y todos sus
  métodos públicos, ausentes en el código original.

## Pendiente (no aplicado en este ciclo — requiere decisiones de producto)

Estos puntos del roadmap (Sección 5) son funcionalidades nuevas, no
correcciones, y se dejan fuera de este ciclo de correcciones para no
mezclar "arreglar lo roto" con "construir features nuevas" en el mismo
cambio:

- Descarga por lotes / modo CLI no interactivo (`argparse`).
- Historial de descargas en SQLite.
- Archivo de configuración `.friz.toml`.
- Sistema de plugins para nuevas plataformas.
- Empaquetado como paquete PyPI instalable / imagen Docker oficial.
- Migración real del historial de Git de `fotos/video.mp4` a Git LFS
  (el `.gitattributes` ya está listo; falta ejecutar la migración
  sobre el repositorio real con `git lfs migrate`, que requiere acceso
  al historial de Git completo y no solo al snapshot de archivos).
