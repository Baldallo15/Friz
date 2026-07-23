# modules/validator.py
"""
Validador de URLs centralizado para FRIZ.

Se encarga de:
 1. Verificar que la cadena ingresada sea una URL sintácticamente válida
    (esquema http/https + dominio).
 2. Verificar que el dominio de la URL corresponda a la plataforma
    seleccionada en el menú (evita, por ejemplo, pasar una URL de
    TikTok al módulo de YouTube).
"""

from urllib.parse import urlparse

# Dominios aceptados por cada plataforma del MODULE_MAP de friz.py
DOMINIOS_PERMITIDOS = {
    "YouTube": ["youtube.com", "youtu.be", "music.youtube.com"],
    "Spotify": ["open.spotify.com", "spotify.link"],
    "TikTok": ["tiktok.com", "vm.tiktok.com", "vt.tiktok.com"],
    "Instagram": ["instagram.com"],
    "Facebook": ["facebook.com", "fb.watch", "m.facebook.com"],
    "X (Twitter)": ["twitter.com", "x.com"],
    "Pinterest": ["pinterest.com", "pin.it"],
}


def es_url_bien_formada(url: str) -> bool:
    """
    Verifica que la URL tenga esquema (http/https) y dominio.
    """
    try:
        resultado = urlparse(url)
        return resultado.scheme in ("http", "https") and bool(resultado.netloc)
    except Exception:
        return False


def _dominio_coincide(netloc: str, dominios: list) -> bool:
    netloc = netloc.lower()
    # Quita un posible "www." al inicio para comparar mejor
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return any(netloc == d or netloc.endswith("." + d) for d in dominios)


def validar_url_para_plataforma(url: str, plataforma: str) -> tuple:
    """
    Valida la URL de forma integral para la plataforma indicada.

    Retorna una tupla (es_valida: bool, mensaje_error: str).
    Si es_valida es True, mensaje_error es "".
    """
    url = url.strip()

    if not url:
        return False, "La URL no puede estar vacía."

    if not es_url_bien_formada(url):
        return False, (
            "La URL no tiene un formato válido. "
            "Debe comenzar con http:// o https:// e incluir un dominio."
        )

    dominios = DOMINIOS_PERMITIDOS.get(plataforma)
    if dominios:
        netloc = urlparse(url).netloc
        if not _dominio_coincide(netloc, dominios):
            return False, (
                f"La URL no parece pertenecer a {plataforma}. "
                f"Dominios esperados: {', '.join(dominios)}."
            )

    return True, ""
