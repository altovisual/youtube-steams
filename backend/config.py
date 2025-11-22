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

# yt-dlp extra options to bypass bot detection - USAR SOLO CLIENTE ANDROID
YTDLP_EXTRA_OPTS = {
    'nocheckcertificate': True,
    'extractor_args': {
        'youtube': {
            'player_client': ['android_creator'],  # Cliente Android Creator es el más confiable
            'player_skip': ['webpage'],
        }
    },
}

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
