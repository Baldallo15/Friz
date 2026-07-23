<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
# modules/twitter.py
from modules.base import YtDlpDownloader


class TwitterDownloader(YtDlpDownloader):
    PLATAFORMA = "X (Twitter)"
    PREFIJO_ARCHIVO = "X_%(id)s"
<<<<<<< HEAD
=======
=======
from modules.base import BaseDownloader, console

class TwitterDownloader(BaseDownloader):
    def download(self, url: str) -> bool:
        formato_calidad = self.seleccionar_calidad()
        console.print(f"\n[bold bright_cyan]⚡ INICIANDO EXTRACCIÓN DE X (TWITTER)...[/]")
        
        cmd = [
            "yt-dlp",
            "-P", self.output_dir,
            "-f", formato_calidad,
            "-o", "X_%(id)s.%(ext)s",
            url
        ]
        return self.ejecutar_comando_animado(cmd, "X / Twitter")
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
