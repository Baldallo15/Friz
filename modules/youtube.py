# modules/youtube.py
from modules.base import YtDlpDownloader


class YoutubeDownloader(YtDlpDownloader):
    PLATAFORMA = "YouTube"
    PREFIJO_ARCHIVO = "%(title)s"
