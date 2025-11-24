"""
Configuration file for the YouTube Music Downloader backend
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / "downloads"
STEMS_DIR = BASE_DIR / "stems"

# Create directories if they don't exist
DOWNLOADS_DIR.mkdir(exist_ok=True)
STEMS_DIR.mkdir(exist_ok=True)

# YouTube Cookies configuration
# Por defecto usa el archivo cookies.txt en el directorio backend
YOUTUBE_COOKIES_FILE = os.getenv('YOUTUBE_COOKIES_FILE', str(BASE_DIR / 'cookies.txt'))
YOUTUBE_COOKIES_BROWSER = os.getenv('YOUTUBE_COOKIES_BROWSER', None)  # chrome, firefox, edge, etc.

# Proxy configuration (para evitar bot detection)
PROXY_URL = os.getenv('PROXY_URL', None)  # Ejemplo: http://user:pass@proxy.com:port

# Server configuration
HOST = "0.0.0.0"
PORT = 8000

# CORS origins
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "https://youtube-steams.vercel.app",
    "https://youtube-steams-frontend.onrender.com",
    "https://*.vercel.app",  # Permitir todos los subdominios de Vercel
]

# yt-dlp configuration - MÁXIMA CALIDAD
YTDLP_FORMAT = "bestaudio[ext=m4a]/bestaudio/best"  # Preferir M4A (mejor calidad)
AUDIO_QUALITY = "0"  # 0 = mejor calidad VBR (Variable Bit Rate)
AUDIO_FORMAT = "mp3"
AUDIO_BITRATE = "320k"  # Bitrate fijo para MP3

# yt-dlp extra options to bypass bot detection
YTDLP_EXTRA_OPTS = {
    'nocheckcertificate': True,
    'extractor_args': {
        'youtube': {
            # Clientes que funcionan sin autenticación (Nov 2024+)
            'player_client': ['tv_embedded', 'mediaconnect'],
            'player_skip': ['webpage', 'configs'],
        }
    },
    # Opciones adicionales para evitar detección
    'socket_timeout': 30,
    'source_address': '0.0.0.0',
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    },
}

# Add proxy if configured
if PROXY_URL:
    YTDLP_EXTRA_OPTS['proxy'] = PROXY_URL
    print(f"✅ Using proxy: {PROXY_URL.split('@')[1] if '@' in PROXY_URL else PROXY_URL}")

# Video download configuration - ALTA CALIDAD
VIDEO_FORMAT = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"  # Mejor video + audio en MP4
VIDEO_QUALITY = "1080"  # Máxima resolución preferida

# Demucs configuration - OPTIMIZADO PARA VELOCIDAD
DEMUCS_MODEL_FULL = "htdemucs_ft"  # Modelo completo (4 stems: vocals, drums, bass, other)
DEMUCS_MODEL_FAST = "htdemucs"     # Modelo rápido para 2 stems (vocals, instrumental)
DEMUCS_OUTPUT_FORMAT = "mp3"
DEMUCS_BITRATE = "320"
DEMUCS_JOBS = 0  # 0 = usar todos los cores disponibles (más rápido)
DEMUCS_SEGMENT = 7  # Segmento para procesamiento (7 segundos - debe ser entero)
DEMUCS_TWO_STEMS = True  # Usar modo 2 stems por defecto (más rápido)

# FFmpeg optimization
FFMPEG_THREADS = 0  # 0 = usar todos los threads disponibles

# File cleanup (optional - set to True to auto-delete old files)
AUTO_CLEANUP = False
CLEANUP_AFTER_HOURS = 24
