# modules/tiktok.py
<<<<<<< HEAD
"""
Descargador de TikTok.

Sobreescribe `limpiar_url` respecto a la plantilla genérica de
`YtDlpDownloader` porque TikTok añade parámetros de rastreo
(`?_r=1`, `&share_item_id`, etc.) a sus enlaces compartidos, que
conviene eliminar antes de pasarlos a yt-dlp.
"""
from modules.base import YtDlpDownloader


class TikTokDownloader(YtDlpDownloader):
    PLATAFORMA = "TikTok"
    PREFIJO_ARCHIVO = "TikTok_%(id)s"

    def limpiar_url(self, url: str) -> str:
        # Limpieza de parámetros de rastreo (?_r=1, &share_item_id, etc.)
        return url.split("?")[0].strip()
=======
from modules.base import BaseDownloader, console

class TikTokDownloader(BaseDownloader):
    def download(self, url: str) -> bool:
        # Limpieza de parámetros de rastreo (?_r=1, &share_item_id, etc.)
        url_limpia = url.split("?")[0].strip()
        
        # Menú de resolución Cyberpunk
        formato_calidad = self.seleccionar_calidad()

        console.print(f"\n[bold bright_cyan]⚡ INICIANDO EXTRACCIÓN DE TIKTOK...[/]")
        console.print(f"[bold bright_magenta]TARGET URL:[/] {url_limpia}")
        
        cmd = [
            "yt-dlp",
            "-P", self.output_dir,
            "-f", formato_calidad,
            "-o", "TikTok_%(id)s.%(ext)s",
            "--no-check-certificates",
            url_limpia
        ]
        
        # Ejecución con la animación neón centralizada
        return self.ejecutar_comando_animado(cmd, "TikTok")
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
