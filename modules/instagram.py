<<<<<<< HEAD
# modules/instagram.py
from modules.base import YtDlpDownloader


class InstagramDownloader(YtDlpDownloader):
    PLATAFORMA = "Instagram"
    PREFIJO_ARCHIVO = "Instagram_%(id)s"
=======
from modules.base import BaseDownloader, console

class InstagramDownloader(BaseDownloader):
    def download(self, url: str) -> bool:
        formato_calidad = self.seleccionar_calidad()
        console.print(f"\n[bold bright_cyan]⚡ INICIANDO EXTRACCIÓN DE INSTAGRAM...[/]")
        
        cmd = [
            "yt-dlp",
            "-P", self.output_dir,
            "-f", formato_calidad,
            "-o", "Instagram_%(id)s.%(ext)s",
            url
        ]
        return self.ejecutar_comando_animado(cmd, "Instagram")
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
