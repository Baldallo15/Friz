import os
import subprocess
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from .base import BaseDownloader

console = Console(force_terminal=True)

class YoutubeDownloader(BaseDownloader):
    def __init__(self):
        super().__init__(plataforma="YouTube")
    
    def descargar_audio(self, url, calidad="192"):
        """Descarga audio"""
        yt_dlp_bin = self.obtener_ytdlp_bin()
        ffmpeg_args = self.obtener_ffmpeg_args()
        tiene_ffmpeg, _ = self.tiene_ffmpeg_real()
        
        if tiene_ffmpeg:
            cmd = [
                yt_dlp_bin,
                "-P", str(self.output_dir),
                "-f", "bestaudio/best",
                "-o", "%(title)s.%(ext)s",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", calidad,
                "--ignore-errors",
            ]
            cmd = [c for c in cmd if c != ""]
            cmd.extend(ffmpeg_args)
            cmd.append(url)
            return self.ejecutar_comando_animado(cmd, "YouTube Audio")
        else:
            console.print("[yellow]⚠ Sin ffmpeg real, descargando en formato original (.webm/.opus/.m4a)[/]")
            cmd = [
                yt_dlp_bin,
                "-P", str(self.output_dir),
                "-f", "bestaudio/best",
                "-o", "%(title)s.%(ext)s",
                "--ignore-errors",
            ]
            cmd = [c for c in cmd if c != ""]
            cmd.append(url)
            return self.ejecutar_comando_animado(cmd, "YouTube Audio")
    
    def descargar_video(self, url, calidad="best"):
        """Descarga video"""
        yt_dlp_bin = self.obtener_ytdlp_bin()
        ffmpeg_args = self.obtener_ffmpeg_args()
        
        cmd = [
            yt_dlp_bin,
            "-P", str(self.output_dir),
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "-o", "%(title)s.%(ext)s",
            "--merge-output-format", "mp4",
            "--ignore-errors",
        ]
        cmd = [c for c in cmd if c != ""]
        cmd.extend(ffmpeg_args)
        cmd.append(url)
        
        return self.ejecutar_comando_animado(cmd, "YouTube Video")
    
    def descargar_playlist_audio(self, url, calidad="192", tracks_seleccionados=None):
        """Descarga playlist/audio con selección"""
        yt_dlp_bin = self.obtener_ytdlp_bin()
        ffmpeg_args = self.obtener_ffmpeg_args()
        tiene_ffmpeg, _ = self.tiene_ffmpeg_real()
        
        if tracks_seleccionados and len(tracks_seleccionados) > 0:
            if len(tracks_seleccionados) == 1 and "directo" in tracks_seleccionados[0]["titulo"].lower():
                if tiene_ffmpeg:
                    cmd = [
                        yt_dlp_bin,
                        "-P", str(self.output_dir),
                        "-f", "bestaudio/best",
                        "-o", "%(playlist_index)s - %(title)s.%(ext)s",
                        "--extract-audio",
                        "--audio-format", "mp3",
                        "--audio-quality", calidad,
                        "--yes-playlist",
                        "--ignore-errors",
                    ]
                    cmd = [c for c in cmd if c != ""]
                    cmd.extend(ffmpeg_args)
                    cmd.append(url)
                    return self.ejecutar_comando_animado(cmd, "YouTube Playlist Audio")
                else:
                    console.print("[yellow]⚠ Sin ffmpeg real, descargando en formato original[/]")
                    cmd = [
                        yt_dlp_bin,
                        "-P", str(self.output_dir),
                        "-f", "bestaudio/best",
                        "-o", "%(playlist_index)s - %(title)s.%(ext)s",
                        "--yes-playlist",
                        "--ignore-errors",
                    ]
                    cmd = [c for c in cmd if c != ""]
                    cmd.append(url)
                    return self.ejecutar_comando_animado(cmd, "YouTube Playlist Audio")
            else:
                exito_total = True
                if not tiene_ffmpeg:
                    console.print("[yellow]⚠ Sin ffmpeg real, descargando en formato original[/]")
                for i, track in enumerate(tracks_seleccionados):
                    track_url = track.get("url", url)
                    console.print(f"\n[cyan]Descargando {i+1}/{len(tracks_seleccionados)}: {track['titulo'][:60]}[/]")
                    if tiene_ffmpeg:
                        cmd = [
                            yt_dlp_bin,
                            "-P", str(self.output_dir),
                            "-f", "bestaudio/best",
                            "-o", "%(title)s.%(ext)s",
                            "--extract-audio",
                            "--audio-format", "mp3",
                            "--audio-quality", calidad,
                            "--no-playlist",
                            "--ignore-errors",
                        ]
                        cmd = [c for c in cmd if c != ""]
                        cmd.extend(ffmpeg_args)
                        cmd.append(track_url)
                    else:
                        cmd = [
                            yt_dlp_bin,
                            "-P", str(self.output_dir),
                            "-f", "bestaudio/best",
                            "-o", "%(title)s.%(ext)s",
                            "--no-playlist",
                            "--ignore-errors",
                        ]
                        cmd = [c for c in cmd if c != ""]
                        cmd.append(track_url)
                    res = self.ejecutar_comando_animado(cmd, f"Pista {i+1}")
                    if not res:
                        exito_total = False
                return exito_total
        else:
            if tiene_ffmpeg:
                cmd = [
                    yt_dlp_bin,
                    "-P", str(self.output_dir),
                    "-f", "bestaudio/best",
                    "-o", "%(playlist_index)s - %(title)s.%(ext)s",
                    "--extract-audio",
                    "--audio-format", "mp3",
                    "--audio-quality", calidad,
                    "--yes-playlist",
                    "--ignore-errors",
                ]
                cmd = [c for c in cmd if c != ""]
                cmd.extend(ffmpeg_args)
                cmd.append(url)
                return self.ejecutar_comando_animado(cmd, "YouTube Playlist Audio")
            else:
                console.print("[yellow]⚠ Sin ffmpeg real, descargando en formato original[/]")
                cmd = [
                    yt_dlp_bin,
                    "-P", str(self.output_dir),
                    "-f", "bestaudio/best",
                    "-o", "%(playlist_index)s - %(title)s.%(ext)s",
                    "--yes-playlist",
                    "--ignore-errors",
                ]
                cmd = [c for c in cmd if c != ""]
                cmd.append(url)
                return self.ejecutar_comando_animado(cmd, "YouTube Playlist Audio")
    
    def download_seguro(self, url: str):
        """Descarga segura con soporte para playlist"""
        try:
            if self._es_playlist_o_album(url):
                lista = self.escanear_playlist(url)
                if not lista:
                    console.print("[red]No se pudo escanear la playlist[/]")
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
                
                tiene_ffmpeg, _ = self.tiene_ffmpeg_real()
                if tiene_ffmpeg:
                    console.print("\n[bold bright_cyan]🎵 Selecciona calidad de audio[/]")
                    console.print("  [cyan][1][/] 320 kbps (Mejor calidad)")
                    console.print("  [cyan][2][/] 256 kbps (Alta calidad)")
                    console.print("  [cyan][3][/] 192 kbps (Calidad estándar)")
                    console.print("  [cyan][4][/] 128 kbps (Menor tamaño)")
                    
                    cal_op = Prompt.ask("[bold bright_magenta]Calidad", choices=["1","2","3","4"], default="3")
                    calidad_map = {"1": "320", "2": "256", "3": "192", "4": "128"}
                    calidad = calidad_map[cal_op]
                    self.mostrar_resumen(len(tracks), calidad, dur_total)
                else:
                    console.print("[yellow]⚠ Sin ffmpeg real, se descargará en formato original[/]")
                    calidad = "192"
                    self.mostrar_resumen(len(tracks), "original", dur_total)
                
                if not Confirm.ask("[bold yellow]¿Iniciar descarga?[/]", default=True):
                    console.print("[yellow]Descarga cancelada[/]")
                    return False
                
                return self.descargar_playlist_audio(url, calidad, tracks)
            else:
                tiene_ffmpeg, _ = self.tiene_ffmpeg_real()
                if tiene_ffmpeg:
                    console.print("\n[bold bright_cyan]🎵 ¿Qué deseas descargar?[/]")
                    console.print("  [cyan][1][/] Solo audio (MP3)")
                    console.print("  [cyan][2][/] Video (MP4)")
                    
                    tipo = Prompt.ask("[bold bright_magenta]Opción", choices=["1","2"], default="1")
                    
                    if tipo == "1":
                        console.print("\n[bold bright_cyan]🎵 Selecciona calidad[/]")
                        console.print("  [cyan][1][/] 320 kbps")
                        console.print("  [cyan][2][/] 256 kbps")
                        console.print("  [cyan][3][/] 192 kbps")
                        console.print("  [cyan][4][/] 128 kbps")
                        cal_op = Prompt.ask("[bold bright_magenta]Calidad", choices=["1","2","3","4"], default="3")
                        calidad_map = {"1": "320", "2": "256", "3": "192", "4": "128"}
                        return self.descargar_audio(url, calidad_map[cal_op])
                    else:
                        return self.descargar_video(url)
                else:
                    console.print("[yellow]⚠ Sin ffmpeg real, descargando audio en formato original[/]")
                    return self.descargar_audio(url, "192")
        except Exception as e:
            console.print(f"[bold red]Error: {e}[/]")
            import traceback
            traceback.print_exc()
            return False
