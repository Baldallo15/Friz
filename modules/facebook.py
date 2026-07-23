from modules.base import BaseDownloader, console

class FacebookDownloader(BaseDownloader):
    def download(self, url: str) -> bool:
        formato_calidad = self.seleccionar_calidad()
        console.print(f"\n[bold bright_cyan]⚡ INICIANDO EXTRACCIÓN DE FACEBOOK...[/]")
        
        cmd = [
            "yt-dlp",
            "-P", self.output_dir,
            "-f", formato_calidad,
            "-o", "FB_%(id)s.%(ext)s",
            url
        ]
        return self.ejecutar_comando_animado(cmd, "Facebook")
