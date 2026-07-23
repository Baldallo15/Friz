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
