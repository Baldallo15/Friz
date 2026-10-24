import os
import subprocess
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from .base import BaseDownloader

console = Console(force_terminal=True)

class SpotifyDownloader(BaseDownloader):
    def __init__(self):
        super().__init__(plataforma="Spotify")
    
    def descargar(self, url):
        """Descarga de Spotify con spotdl"""
        cmd = [
            "spotdl",
            url,
            "--output", str(self.output_dir / "{artist} - {title}.{output-ext}"),
            "--format", "mp3",
            "--bitrate", "192k",
        ]
        
        return self.ejecutar_comando_animado(cmd, "Spotify")
    
    def descargar_seleccionado(self, url, tracks_seleccionados=None):
        """Descarga tracks seleccionados"""
        if tracks_seleccionados and len(tracks_seleccionados) > 0:
            if len(tracks_seleccionados) == 1 and "directo" in tracks_seleccionados[0]["titulo"].lower():
                return self.descargar(url)
            else:
                exito_total = True
                for i, track in enumerate(tracks_seleccionados):
                    track_url = track.get("url", url)
                    console.print(f"\n[cyan]Descargando {i+1}/{len(tracks_seleccionados)}: {track['titulo'][:60]}[/]")
                    cmd = [
                        "spotdl",
                        track_url,
                        "--output", str(self.output_dir / "{artist} - {title}.{output-ext}"),
                        "--format", "mp3",
                        "--bitrate", "192k",
                    ]
                    res = self.ejecutar_comando_animado(cmd, f"Pista {i+1}")
                    if not res:
                        exito_total = False
                return exito_total
        else:
            return self.descargar(url)
    
    def download_seguro(self, url: str):
        """Descarga segura con soporte para playlist/álbum"""
        try:
            if self._es_playlist_o_album(url):
                lista = self.escanear_playlist(url)
                if not lista:
                    console.print("[red]No se pudo escanear la playlist/álbum[/]")
                    return False
                
                tracks = self.seleccionar_descarga(lista)
                if not tracks:
                    console.print("[yellow]Descarga cancelada[/]")
                    return False
                
                dur_total = 0
                for t in tracks:
                    d = t.get("duracion") or 0
                    if isinstance(d, (int, float)):
                        dur_total += d
                
                console.print("\n[bold bright_cyan]🎵 Calidad de audio[/]")
                console.print("  [cyan][1][/] 320 kbps")
                console.print("  [cyan][2][/] 256 kbps")
                console.print("  [cyan][3][/] 192 kbps")
                console.print("  [cyan][4][/] 128 kbps")
                
                cal_op = Prompt.ask("[bold bright_magenta]Calidad", choices=["1","2","3","4"], default="3")
                calidad_map = {"1": "320k", "2": "256k", "3": "192k", "4": "128k"}
                calidad = calidad_map[cal_op]
                
                self.mostrar_resumen(len(tracks), calidad.replace('k',''), dur_total)
                
                if not Confirm.ask("[bold yellow]¿Iniciar descarga?[/]", default=True):
                    console.print("[yellow]Descarga cancelada[/]")
                    return False
                
                if len(tracks) == 1 and "directo" in tracks[0]["titulo"].lower():
                    cmd = [
                        "spotdl",
                        url,
                        "--output", str(self.output_dir / "{artist} - {title}.{output-ext}"),
                        "--format", "mp3",
                        "--bitrate", calidad,
                    ]
                    return self.ejecutar_comando_animado(cmd, "Spotify")
                else:
                    exito_total = True
                    for i, track in enumerate(tracks):
                        console.print(f"\n[cyan]Descargando {i+1}/{len(tracks)}: {track['titulo'][:60]}[/]")
                        track_url = track.get("url") or url
                        cmd = [
                            "spotdl",
                            track_url,
                            "--output", str(self.output_dir / "{artist} - {title}.{output-ext}"),
                            "--format", "mp3",
                            "--bitrate", calidad,
                        ]
                        res = self.ejecutar_comando_animado(cmd, f"Pista {i+1}")
                        if not res:
                            exito_total = False
                    return exito_total
            else:
                console.print("\n[bold bright_cyan]🎵 Calidad de audio[/]")
                console.print("  [cyan][1][/] 320 kbps")
                console.print("  [cyan][2][/] 256 kbps")
                console.print("  [cyan][3][/] 192 kbps")
                console.print("  [cyan][4][/] 128 kbps")
                
                cal_op = Prompt.ask("[bold bright_magenta]Calidad", choices=["1","2","3","4"], default="3")
                calidad_map = {"1": "320k", "2": "256k", "3": "192k", "4": "128k"}
                calidad = calidad_map[cal_op]
                
                cmd = [
                    "spotdl",
                    url,
                    "--output", str(self.output_dir / "{artist} - {title}.{output-ext}"),
                    "--format", "mp3",
                    "--bitrate", calidad,
                ]
                return self.ejecutar_comando_animado(cmd, "Spotify")
        except Exception as e:
            console.print(f"[bold red]Error: {e}[/]")
            return False
