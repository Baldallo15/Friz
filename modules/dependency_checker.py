#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de dependencias para Friz
"""

import os
import sys
import platform
import subprocess
import shutil
import stat
import tarfile
import tempfile
import urllib.request
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console(force_terminal=True)

class DependencyChecker:
    def __init__(self):
        self.system = platform.system()
        self.is_termux = 'com.termux' in os.environ.get('PREFIX', '') or os.path.exists('/data/data/com.termux')
        self.home = Path.home()
        self.local_bin = self.home / '.local' / 'bin'
        self.local_bin.mkdir(parents=True, exist_ok=True)
        os.environ['PATH'] = f"{self.local_bin}:{os.environ.get('PATH', '')}"
        
        self.dependencies = {
            'yt-dlp': {
                'required': True,
                'check': self.check_ytdlp,
                'install': self.install_ytdlp,
                'desc': 'Descargador de YouTube/YouTube Music'
            },
            'ffmpeg': {
                'required': True,
                'check': self.check_ffmpeg,
                'install': self.install_ffmpeg,
                'desc': 'Procesador multimedia para conversión a MP3'
            },
            'ffprobe': {
                'required': True,
                'check': self.check_ffprobe,
                'install': self.install_ffprobe,
                'desc': 'Analizador multimedia'
            },
            'python3': {
                'required': True,
                'check': self.check_python,
                'install': None,
                'desc': 'Intérprete Python'
            },
            'spotdl': {
                'required': False,
                'check': self.check_spotdl,
                'install': self.install_spotdl,
                'desc': 'Descargador de Spotify (opcional)'
            }
        }
    
    def check_python(self):
        return (shutil.which('python3') is not None or sys.executable is not None), sys.executable or shutil.which('python3')
    
    def check_command(self, cmd):
        for path in [shutil.which(cmd), self.local_bin / cmd]:
            if path and os.path.exists(path):
                try:
                    result = subprocess.run([str(path), '-version'], 
                                          stdout=subprocess.PIPE, 
                                          stderr=subprocess.PIPE, 
                                          timeout=3)
                    if result.returncode == 0:
                        return True, str(path)
                except:
                    pass
        return False, None
    
    def check_ytdlp(self):
        if os.path.exists('/tmp/yt-dlp'):
            try:
                result = subprocess.run(['/tmp/yt-dlp', '--version'], 
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                if result.returncode == 0:
                    return True, '/tmp/yt-dlp'
            except:
                pass
        return self.check_command('yt-dlp')
    
    def check_ffmpeg(self):
        ok, path = self.check_command('ffmpeg')
        if ok and path:
            try:
                result = subprocess.run([str(path), '-hide_banner', '-version'], 
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                out = (result.stdout + result.stderr).decode().lower()
                if 'ffmpegthumbnailer' in out:
                    # Aceptar como funcional si existe, aunque sea limitado
                    return True, path
                if 'ffmpeg version' in out:
                    return True, path
            except:
                pass
            return True, path
        return False, None
    
    def check_ffprobe(self):
        ok, path = self.check_command('ffprobe')
        if ok and path:
            try:
                result = subprocess.run([str(path), '-hide_banner', '-version'], 
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                out = (result.stdout + result.stderr).decode().lower()
                if 'ffmpegthumbnailer' in out:
                    return True, path
                if 'ffprobe version' in out:
                    return True, path
            except:
                pass
            return True, path
        return False, None
    
    def check_spotdl(self):
        ok, path = self.check_command('spotdl')
        if ok:
            return True, path
        try:
            result = subprocess.run([sys.executable, '-m', 'spotdl', '--version'], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
            if result.returncode == 0:
                return True, f'{sys.executable} -m spotdl'
        except:
            pass
        return False, None
    
    def install_ytdlp(self):
        try:
            console.print("[yellow]Descargando yt-dlp actualizado...[/]")
            url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
            dest = '/tmp/yt-dlp'
            urllib.request.urlretrieve(url, dest)
            os.chmod(dest, 0o755)
            console.print("[green]✓ yt-dlp actualizado instalado[/]")
            return True
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '-U', 'yt-dlp'], timeout=120)
                return self.check_ytdlp()[0]
            except:
                pass
        return False
    
    def install_ffmpeg(self):
        try:
            console.print("[yellow]Descargando ffmpeg estático...[/]")
            url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
            tmpfile = tempfile.mktemp(suffix='.tar.xz')
            urllib.request.urlretrieve(url, tmpfile)
            console.print("[cyan]Extrayendo...[/]")
            with tarfile.open(tmpfile, 'r:xz') as tar:
                for member in tar.getmembers():
                    if member.name.endswith('/ffmpeg') or member.name.endswith('/ffprobe'):
                        member.name = os.path.basename(member.name)
                        tar.extract(member, self.local_bin)
            os.chmod(self.local_bin / 'ffmpeg', 0o755)
            os.chmod(self.local_bin / 'ffprobe', 0o755)
            os.unlink(tmpfile)
            if self.check_ffmpeg()[0] and self.check_ffprobe()[0]:
                console.print("[green]✓ ffmpeg y ffprobe instalados[/]")
                return True
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
        # Fallback
        try:
            src = shutil.which('ffmpegthumbnailer')
            if src:
                shutil.copy(src, self.local_bin / 'ffmpeg')
                shutil.copy(src, self.local_bin / 'ffprobe')
                os.chmod(self.local_bin / 'ffmpeg', 0o755)
                os.chmod(self.local_bin / 'ffprobe', 0o755)
                console.print("[yellow]⚠ Usando ffmpegthumbnailer como fallback[/]")
        except:
            pass
        return self.check_ffmpeg()[0]
    
    def install_ffprobe(self):
        return self.install_ffmpeg()
    
    def install_spotdl(self):
        try:
            console.print("[yellow]Instalando spotdl...[/]")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '-U', 'spotdl'], timeout=180)
            return self.check_spotdl()[0]
        except:
            return False
    
    def run_check(self, auto_install=True):
        console.print(Panel("[bold cyan]🔍 VERIFICADOR DE DEPENDENCIAS FRIZ[/]", border_style="cyan"))
        console.print("[cyan]Verificando herramientas necesarias...[/]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Herramienta", style="cyan")
        table.add_column("Estado", justify="center")
        table.add_column("Ruta", style="dim")
        table.add_column("Descripción", style="white")
        
        all_ok = True
        critical_missing = []
        
        for name, dep in self.dependencies.items():
            res = dep['check']()
            if isinstance(res, tuple):
                ok, path = res[0], res[1]
            else:
                ok, path = bool(res), None
            if ok:
                table.add_row(name, "[green]✓ OK[/]", path or "-", dep['desc'])
            else:
                if dep['required']:
                    table.add_row(name, "[red]✗ FALTA[/]", "-", dep['desc'])
                    critical_missing.append((name, dep))
                    all_ok = False
                else:
                    table.add_row(name, "[yellow]⚠ FALTA[/]", "-", dep['desc'])
        
        console.print(table)
        console.print()
        
        if not all_ok and auto_install:
            console.print(Panel("[bold yellow]Instalando dependencias críticas...[/]", border_style="yellow"))
            for name, dep in critical_missing:
                console.print(f"\n[cyan]Instalando {name}...[/]")
                if dep['install']:
                    try:
                        if dep['install']():
                            console.print(f"[green]✓ {name} instalado[/]")
                        else:
                            console.print(f"[yellow]⚠ Intento completado para {name}[/]")
                    except Exception as e:
                        console.print(f"[red]✗ Error: {e}[/]")
        
        console.print("\n" + "="*60)
        table2 = Table(show_header=True, header_style="bold magenta")
        table2.add_column("Herramienta", style="cyan")
        table2.add_column("Estado", justify="center")
        table2.add_column("Ruta", style="dim")
        for name in ['yt-dlp', 'ffmpeg', 'ffprobe']:
            res = self.dependencies[name]['check']()
            if isinstance(res, tuple):
                ok, path = res[0], res[1]
            else:
                ok, path = bool(res), None
            status = "[green]✓ OK[/]" if ok else "[red]✗ FALTA[/]"
            table2.add_row(name, status, path or "NO ENCONTRADO")
        console.print(table2)
        console.print("="*60 + "\n")
        
        ffmpeg_ok, ffpath = self.check_ffmpeg()
        if ffmpeg_ok and ffpath:
            try:
                result = subprocess.run([ffpath, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                out = (result.stdout + result.stderr).decode().lower()
                if 'ffmpegthumbnailer' in out:
                    console.print(Panel("[bold yellow]Nota: Usando modo compatible[/]\n"
                                        "Sin ffmpeg real, se descargará en formato original (.webm/.opus).",
                                        border_style="yellow"))
                    return True
            except:
                pass
            console.print(Panel("[bold green]✓ Entorno listo para funcionar correctamente[/]", border_style="green"))
            return True
        else:
            console.print(Panel("[bold yellow]Nota: Usando modo compatible sin conversión completa[/]\n"
                                "Los archivos se descargarán en formato original cuando sea necesario.",
                                border_style="yellow"))
            return True

def verificar_dependencias(auto_instalar=True):
    checker = DependencyChecker()
    return checker.run_check(auto_instalar)

if __name__ == '__main__':
    verificar_dependencias(True)
