"""
Pruebas unitarias de modules/validator.py.

Se prioriza este módulo porque es el único con lógica pura, sin
dependencias de red ni de procesos externos (yt-dlp/spotdl), por lo
que no requiere mocks para ser probado (ver Sección 3.5 de la
auditoría técnica).
"""
import pytest

from modules.validator import es_url_bien_formada, validar_url_para_plataforma


class TestEsUrlBienFormada:
    def test_url_https_valida(self):
        assert es_url_bien_formada("https://www.youtube.com/watch?v=abc123") is True

    def test_url_http_valida(self):
        assert es_url_bien_formada("http://youtu.be/abc123") is True

    def test_url_sin_esquema_es_invalida(self):
        assert es_url_bien_formada("www.youtube.com/watch?v=abc123") is False

    def test_cadena_vacia_es_invalida(self):
        assert es_url_bien_formada("") is False

    def test_texto_no_url_es_invalido(self):
        assert es_url_bien_formada("esto no es una url") is False

    def test_esquema_no_http_es_invalido(self):
        assert es_url_bien_formada("ftp://ejemplo.com/archivo") is False


class TestValidarUrlParaPlataforma:
    def test_url_vacia(self):
        valida, mensaje = validar_url_para_plataforma("", "YouTube")
        assert valida is False
        assert "vacía" in mensaje

    def test_url_mal_formada(self):
        valida, mensaje = validar_url_para_plataforma("no-es-una-url", "YouTube")
        assert valida is False

    def test_youtube_url_correcta(self):
        valida, mensaje = validar_url_para_plataforma(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "YouTube"
        )
        assert valida is True
        assert mensaje == ""

    def test_youtu_be_url_correcta(self):
        valida, _ = validar_url_para_plataforma("https://youtu.be/dQw4w9WgXcQ", "YouTube")
        assert valida is True

    def test_dominio_incorrecto_para_plataforma(self):
        # URL de TikTok enviada al módulo de YouTube -> debe rechazarse
        valida, mensaje = validar_url_para_plataforma(
            "https://www.tiktok.com/@usuario/video/12345", "YouTube"
        )
        assert valida is False
        assert "YouTube" in mensaje

    def test_spotify_dominio_alternativo(self):
        valida, _ = validar_url_para_plataforma("https://spotify.link/abc123", "Spotify")
        assert valida is True

    def test_pinterest_dominio_corto(self):
        valida, _ = validar_url_para_plataforma("https://pin.it/abc123", "Pinterest")
        assert valida is True

    def test_plataforma_desconocida_no_filtra_por_dominio(self):
        # Si la plataforma no está en DOMINIOS_PERMITIDOS, solo se exige
        # que la URL esté bien formada.
        valida, _ = validar_url_para_plataforma("https://ejemplo.com/x", "PlataformaInexistente")
        assert valida is True

    @pytest.mark.parametrize("plataforma,url", [
        ("Instagram", "https://www.instagram.com/p/abc123/"),
        ("Facebook", "https://fb.watch/abc123/"),
        ("X (Twitter)", "https://x.com/usuario/status/12345"),
    ])
    def test_urls_validas_por_plataforma(self, plataforma, url):
        valida, _ = validar_url_para_plataforma(url, plataforma)
        assert valida is True
