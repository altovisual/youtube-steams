from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import yt_dlp
import os
import uuid
from pathlib import Path
import asyncio
from typing import Optional
import json
import re
from datetime import datetime
import httpx
import config
from proxy_manager import proxy_manager
from rate_limiter import rate_limiter, check_rate_limit
from cobalt_service import cobalt_service

app = FastAPI(title="YouTube Music Downloader API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use directories from config
DOWNLOADS_DIR = config.DOWNLOADS_DIR
STEMS_DIR = config.STEMS_DIR

# Store metadata for downloaded files
file_metadata = {}

def get_ytdlp_opts_with_cookies(base_opts: dict, use_proxy: bool = True) -> dict:
    """Add cookies and proxy to yt-dlp options if configured"""
    opts = base_opts.copy()
    
    # Solo usar proxy si está configurado explícitamente en config
    # Los proxies públicos gratuitos no son confiables
    if use_proxy and config.PROXY_URL:
        opts['proxy'] = config.PROXY_URL
        print(f"🔄 Using configured proxy")
    
    # Check if cookies are in environment variable (for Render/production)
    cookies_content = os.getenv('YOUTUBE_COOKIES')
    if cookies_content:
        try:
            print(f"Found YOUTUBE_COOKIES environment variable (length: {len(cookies_content)} chars)")
            # Write cookies to temporary file with proper Netscape format
            temp_cookies_file = DOWNLOADS_DIR / 'temp_cookies.txt'
            
            # Write entire content (should already have Netscape header)
            temp_cookies_file.write_text(cookies_content, encoding='utf-8')
            opts['cookiefile'] = str(temp_cookies_file)
            
            # Count non-comment lines
            cookie_lines = [line for line in cookies_content.split('\n') if line.strip() and not line.startswith('#')]
            print(f"✅ Using cookies file with {len(cookie_lines)} cookie entries")
            print(f"📁 Cookies written to: {temp_cookies_file}")
        except Exception as e:
            print(f"❌ Error processing cookies from environment: {e}")
            import traceback
            traceback.print_exc()
    # For local development: use browser cookies if configured
    elif config.YOUTUBE_COOKIES_BROWSER:
        opts['cookiesfrombrowser'] = (config.YOUTUBE_COOKIES_BROWSER,)
        print(f"🍪 Using cookies from browser: {config.YOUTUBE_COOKIES_BROWSER}")
    # Or from file if it exists
    elif config.YOUTUBE_COOKIES_FILE and Path(config.YOUTUBE_COOKIES_FILE).exists():
        opts['cookiefile'] = config.YOUTUBE_COOKIES_FILE
        print(f"🍪 Using cookies from file: {config.YOUTUBE_COOKIES_FILE}")
    else:
        print("⚠️ No cookies configured")
    
    return opts

def sanitize_filename(filename: str) -> str:
    """Clean filename to be safe for file systems"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace multiple spaces with single space
    filename = re.sub(r'\s+', ' ', filename)
    # Trim and limit length
    filename = filename.strip()[:200]
    return filename

class VideoURL(BaseModel):
    url: str

class SeparateRequest(BaseModel):
    file_id: str
    two_stems: bool = True  # True = solo vocals/instrumental (rápido), False = 4 stems completos
    
    class Config:
        json_schema_extra = {
            "example": {
                "file_id": "abc123",
                "two_stems": True
            }
        }

@app.get("/")
async def root():
    return {"message": "YouTube Music Downloader API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint para mantener el servicio activo"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "youtube-steams-backend"
    }

@app.get("/api/rate-limit-status")
async def get_rate_limit_status(request: Request):
    """Obtiene el estado actual del límite de descargas para el usuario"""
    status = rate_limiter.get_status(request)
    return {
        "remaining": status["remaining"],
        "total": status["total"],
        "reset_time": status["reset_time"]
    }

@app.get("/api/test-youtube")
async def test_youtube():
    """Test endpoint to verify YouTube extraction works"""
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # Me at the zoo - primer video de YouTube
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'noplaylist': True,
            **config.YTDLP_EXTRA_OPTS,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
            
        return {
            "status": "success",
            "title": info.get('title'),
            "duration": info.get('duration'),
            "extractor": info.get('extractor'),
            "player_client": "android_creator"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "config": config.YTDLP_EXTRA_OPTS
        }

@app.get("/api/test-stems")
async def test_stems():
    """Test endpoint to verify Demucs configuration"""
    import shutil
    import sys
    
    # Check if demucs module can be imported
    demucs_module = False
    demucs_version = None
    try:
        import demucs
        demucs_module = True
        demucs_version = demucs.__version__
    except ImportError:
        pass
    
    # List downloaded audio files
    audio_files = []
    if DOWNLOADS_DIR.exists():
        audio_files = [f.name for f in DOWNLOADS_DIR.glob("*.mp3")]
    
    return {
        "demucs_module_installed": demucs_module,
        "demucs_version": demucs_version,
        "demucs_executable": shutil.which("demucs"),
        "python_executable": sys.executable,
        "model_fast": config.DEMUCS_MODEL_FAST,
        "model_full": config.DEMUCS_MODEL_FULL,
        "downloads_dir": str(DOWNLOADS_DIR),
        "stems_dir": str(STEMS_DIR),
        "audio_files_count": len(audio_files),
        "audio_files": audio_files[:5]  # Show first 5 files
    }

def extract_video_id(url: str) -> Optional[str]:
    """Extrae el ID del video de una URL de YouTube"""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

async def get_video_info_oembed(video_id: str) -> dict:
    """Obtiene info del video usando YouTube oEmbed API (no requiere auth)"""
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(oembed_url)
        response.raise_for_status()
        data = response.json()
        
        return {
            "id": video_id,
            "title": data.get("title", "Unknown"),
            "artist": data.get("author_name", "Unknown"),
            "thumbnail": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            "duration": 0,  # oEmbed no proporciona duración
            "view_count": 0,
            "upload_date": None,
            "description": "",
        }

@app.post("/api/video-info")
async def get_video_info(video: VideoURL):
    """Get video information - usa oEmbed como método principal (no requiere cookies)"""
    try:
        print(f"Fetching info for URL: {video.url}")
        
        # Extraer video ID
        video_id = extract_video_id(video.url)
        if not video_id:
            raise HTTPException(status_code=400, detail="URL de YouTube inválida")
        
        # Intentar primero con oEmbed (no requiere auth)
        try:
            video_info = await get_video_info_oembed(video_id)
            print(f"✅ Video info retrieved via oEmbed: {video_info['title']}")
            return video_info
        except Exception as oembed_error:
            print(f"⚠️ oEmbed failed: {oembed_error}, trying yt-dlp...")
        
        # Fallback a yt-dlp si oEmbed falla
        base_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'ignoreerrors': False,
            'no_color': True,
            'noplaylist': True,
            'skip_download': True,
            'format': None,
            'nocheckcertificate': True,
            'socket_timeout': 30,
        }
        
        ydl_opts = get_ytdlp_opts_with_cookies(base_opts)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video.url, download=False)
            
            if not info:
                raise HTTPException(status_code=400, detail="No se pudo obtener información del video")
            
            video_info = {
                "id": info.get('id'),
                "title": info.get('title'),
                "artist": info.get('artist') or info.get('uploader') or info.get('channel'),
                "thumbnail": info.get('thumbnail') or info.get('thumbnails', [{}])[0].get('url'),
                "duration": info.get('duration', 0),
                "view_count": info.get('view_count', 0),
                "upload_date": info.get('upload_date'),
                "description": (info.get('description') or '')[:200],
            }
            
            print(f"✅ Video info retrieved via yt-dlp: {video_info['title']}")
            return video_info
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching video info: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Error al obtener información del video: {str(e)}")

async def download_audio_cobalt(video_url: str, file_id: str) -> tuple[Path, str]:
    """Intenta descargar audio usando Cobalt API"""
    cobalt_response = await cobalt_service.get_download_url(
        url=video_url,
        download_mode="audio",
        audio_format="mp3",
        audio_bitrate="320"
    )
    
    if cobalt_response.get("status") == "error":
        error_msg = cobalt_response.get("error", {}).get("message", "Error desconocido")
        raise Exception(f"Cobalt: {error_msg}")
    
    download_url = cobalt_response.get("url")
    filename = cobalt_response.get("filename", "audio.mp3")
    
    if not download_url:
        raise Exception("Cobalt: No se obtuvo URL de descarga")
    
    print(f"📥 Descargando desde Cobalt: {download_url[:60]}...")
    
    output_path = DOWNLOADS_DIR / f"{file_id}.mp3"
    
    async with httpx.AsyncClient(timeout=120.0, follow_redirects=True) as client:
        response = await client.get(download_url)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
    
    clean_title = sanitize_filename(filename.replace('.mp3', '').replace('.m4a', ''))
    return output_path, clean_title

def download_audio_ytdlp(video_url: str, file_id: str) -> tuple[Path, str]:
    """Fallback: descarga audio usando yt-dlp con cookies"""
    base_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',  # Formato más flexible
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': str(DOWNLOADS_DIR / f"{file_id}.%(ext)s"),
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'socket_timeout': 30,
        # Usar cliente web que tiene más formatos disponibles
        'extractor_args': {
            'youtube': {
                'player_client': ['web', 'mweb'],
            }
        },
    }
    
    ydl_opts = get_ytdlp_opts_with_cookies(base_opts)
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
    
    title = info.get('title', 'audio')
    clean_title = sanitize_filename(title)
    output_path = DOWNLOADS_DIR / f"{file_id}.mp3"
    
    return output_path, clean_title

@app.post("/api/download")
async def download_audio(video: VideoURL, request: Request, limit_status: dict = Depends(check_rate_limit)):
    """Download audio from YouTube - intenta Cobalt primero, fallback a yt-dlp"""
    try:
        # Registrar la descarga
        rate_limiter.record_download(request)
        
        file_id = str(uuid.uuid4())
        clean_title = None
        
        print(f"🎵 Downloading audio: {video.url}")
        
        # Intentar primero con Cobalt
        try:
            output_path, clean_title = await download_audio_cobalt(video.url, file_id)
            print(f"✅ Downloaded via Cobalt: {clean_title}")
        except Exception as cobalt_error:
            print(f"⚠️ Cobalt failed: {cobalt_error}")
            print(f"🔄 Trying yt-dlp fallback...")
            
            # Fallback a yt-dlp
            try:
                output_path, clean_title = download_audio_ytdlp(video.url, file_id)
                print(f"✅ Downloaded via yt-dlp: {clean_title}")
            except Exception as ytdlp_error:
                print(f"❌ yt-dlp also failed: {ytdlp_error}")
                raise Exception(f"No se pudo descargar. Cobalt: {cobalt_error} | yt-dlp: {ytdlp_error}")
        
        if not clean_title:
            clean_title = f"audio_{file_id[:8]}"
        
        # Store metadata
        file_metadata[file_id] = {
            'title': clean_title,
            'filename': f"{clean_title}.mp3",
            'type': 'audio'
        }
        
        # Obtener estado actualizado del límite
        updated_status = rate_limiter.get_status(request)
            
        return {
            "file_id": file_id,
            "filename": f"{clean_title}.mp3",
            "message": "Download completed successfully",
            "rate_limit": {
                "remaining": updated_status["remaining"],
                "total": updated_status["total"],
                "reset_time": updated_status["reset_time"]
            }
        }
        
    except Exception as e:
        print(f"❌ Error downloading: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error downloading audio: {str(e)}")

async def download_video_cobalt(video_url: str, file_id: str) -> tuple[Path, str]:
    """Intenta descargar video usando Cobalt API"""
    cobalt_response = await cobalt_service.get_download_url(
        url=video_url,
        download_mode="auto",
        video_quality="1080"
    )
    
    if cobalt_response.get("status") == "error":
        error_msg = cobalt_response.get("error", {}).get("message", "Error desconocido")
        raise Exception(f"Cobalt: {error_msg}")
    
    download_url = cobalt_response.get("url")
    filename = cobalt_response.get("filename", "video.mp4")
    
    if not download_url:
        raise Exception("Cobalt: No se obtuvo URL de descarga")
    
    print(f"📥 Descargando video desde Cobalt: {download_url[:60]}...")
    
    output_path = DOWNLOADS_DIR / f"{file_id}.mp4"
    
    async with httpx.AsyncClient(timeout=300.0, follow_redirects=True) as client:
        response = await client.get(download_url)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
    
    clean_title = sanitize_filename(filename.replace('.mp4', '').replace('.webm', ''))
    return output_path, clean_title

def download_video_ytdlp(video_url: str, file_id: str) -> tuple[Path, str]:
    """Fallback: descarga video usando yt-dlp con cookies"""
    base_opts = {
        'format': 'bestvideo+bestaudio/best',  # Formato más flexible
        'outtmpl': str(DOWNLOADS_DIR / f"{file_id}.%(ext)s"),
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'merge_output_format': 'mp4',
        'nocheckcertificate': True,
        'socket_timeout': 30,
        # Usar cliente web que tiene más formatos disponibles
        'extractor_args': {
            'youtube': {
                'player_client': ['web', 'mweb'],
            }
        },
    }
    
    ydl_opts = get_ytdlp_opts_with_cookies(base_opts)
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
    
    title = info.get('title', 'video')
    clean_title = sanitize_filename(title)
    output_path = DOWNLOADS_DIR / f"{file_id}.mp4"
    
    return output_path, clean_title

@app.post("/api/download-video")
async def download_video(video: VideoURL, request: Request, limit_status: dict = Depends(check_rate_limit)):
    """Download video from YouTube - intenta Cobalt primero, fallback a yt-dlp"""
    try:
        # Registrar la descarga
        rate_limiter.record_download(request)
        
        file_id = str(uuid.uuid4())
        clean_title = None
        
        print(f"🎬 Downloading video: {video.url}")
        
        # Intentar primero con Cobalt
        try:
            output_path, clean_title = await download_video_cobalt(video.url, file_id)
            print(f"✅ Video downloaded via Cobalt: {clean_title}")
        except Exception as cobalt_error:
            print(f"⚠️ Cobalt failed: {cobalt_error}")
            print(f"🔄 Trying yt-dlp fallback...")
            
            # Fallback a yt-dlp
            try:
                output_path, clean_title = download_video_ytdlp(video.url, file_id)
                print(f"✅ Video downloaded via yt-dlp: {clean_title}")
            except Exception as ytdlp_error:
                print(f"❌ yt-dlp also failed: {ytdlp_error}")
                raise Exception(f"No se pudo descargar. Cobalt: {cobalt_error} | yt-dlp: {ytdlp_error}")
        
        if not clean_title:
            clean_title = f"video_{file_id[:8]}"
        
        # Store metadata
        file_metadata[file_id] = {
            'title': clean_title,
            'filename': f"{clean_title}.mp4",
            'type': 'video'
        }
        
        # Obtener estado actualizado del límite
        updated_status = rate_limiter.get_status(request)
            
        return {
            "file_id": file_id,
            "filename": f"{clean_title}.mp4",
            "message": "Video download completed successfully",
            "rate_limit": {
                "remaining": updated_status["remaining"],
                "total": updated_status["total"],
                "reset_time": updated_status["reset_time"]
            }
        }
        
    except Exception as e:
        print(f"❌ Error downloading video: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error downloading video: {str(e)}")

@app.post("/api/separate-stems")
async def separate_stems(request: SeparateRequest):
    """Separate audio into stems using Demucs - OPTIMIZADO PARA MÁXIMA CALIDAD Y VELOCIDAD"""
    print(f"\n{'='*60}")
    print(f"STEM SEPARATION REQUEST RECEIVED")
    print(f"{'='*60}")
    print(f"Request data: {request}")
    print(f"file_id: {request.file_id}")
    print(f"two_stems: {request.two_stems}")
    
    try:
        # Verificar si Demucs está instalado como módulo de Python
        try:
            import demucs
            print(f"✓ Demucs module found: {demucs.__version__}")
        except ImportError:
            print("✗ Demucs module NOT found")
            raise HTTPException(
                status_code=400, 
                detail="Demucs no está instalado. Por favor instala Demucs ejecutando: pip install demucs"
            )
        
        input_file = DOWNLOADS_DIR / f"{request.file_id}.mp3"
        
        print(f"Looking for file: {input_file}")
        print(f"File exists: {input_file.exists()}")
        
        if not input_file.exists():
            print(f"File not found: {input_file}")
            raise HTTPException(status_code=404, detail=f"Audio file not found: {request.file_id}.mp3")
        
        output_dir = STEMS_DIR / request.file_id
        output_dir.mkdir(exist_ok=True)
        
        mode = "2 stems (vocals + instrumental)" if request.two_stems else "4 stems completos"
        print(f"Starting stem separation for: {request.file_id} - Mode: {mode}")
        
        # Seleccionar modelo según el modo
        model = config.DEMUCS_MODEL_FAST if request.two_stems else config.DEMUCS_MODEL_FULL
        
        # Comando Demucs optimizado para velocidad usando Python
        import sys
        cmd = [
            sys.executable,  # Usar el Python del entorno virtual
            "-m", "demucs",  # Ejecutar demucs como módulo
            "--mp3",  # Formato de salida MP3
            "--mp3-bitrate", config.DEMUCS_BITRATE,  # 320 kbps
            "-o", str(STEMS_DIR),  # Directorio de salida
            "-n", model,  # Modelo según modo seleccionado
            "--segment", str(config.DEMUCS_SEGMENT),  # Segmento (7.8 segundos máximo)
            "-j", str(int(config.DEMUCS_JOBS)),  # Usar todos los cores (0 = auto)
        ]
        
        # Agregar opción de 2 stems si está activada (MUCHO MÁS RÁPIDO)
        if request.two_stems:
            cmd.extend(["--two-stems", "vocals"])  # Solo separar vocals del resto
        
        cmd.append(str(input_file))
        
        print(f"Executing command: {' '.join(cmd)}")
        
        # Ejecutar Demucs con configuración optimizada
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                stdout_msg = stdout.decode() if stdout else ""
                print(f"Demucs error (stderr): {error_msg}")
                print(f"Demucs output (stdout): {stdout_msg}")
                print(f"Return code: {process.returncode}")
                
                # Extraer el mensaje de error más relevante
                if "usage:" in error_msg or "error:" in error_msg:
                    # Es un error de argumentos
                    error_lines = error_msg.split('\n')
                    relevant_error = next((line for line in error_lines if 'error:' in line.lower()), error_msg)
                    raise Exception(f"Error en argumentos de Demucs: {relevant_error}")
                else:
                    raise Exception(f"Demucs falló: {error_msg[:500]}")
        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e}")
            raise Exception(f"No se pudo ejecutar Python: {sys.executable}. Verifica la instalación.")
        except Exception as e:
            print(f"Exception during subprocess execution: {e}")
            raise
        
        print(f"Stem separation complete for: {request.file_id}")
        
        # Buscar archivos separados (puede estar en diferentes ubicaciones según el modelo)
        possible_paths = [
            STEMS_DIR / model / request.file_id,
            STEMS_DIR / config.DEMUCS_MODEL_FULL / request.file_id,
            STEMS_DIR / config.DEMUCS_MODEL_FAST / request.file_id,
            STEMS_DIR / "htdemucs_ft" / request.file_id,
            STEMS_DIR / "htdemucs" / request.file_id,
        ]
        
        stems = []
        stems_path = None
        
        for path in possible_paths:
            if path.exists():
                stems_path = path
                break
        
        if stems_path and stems_path.exists():
            for stem_file in stems_path.glob("*.mp3"):
                stems.append({
                    "name": stem_file.stem,
                    "file_id": f"{request.file_id}/{stem_file.name}"
                })
            
            print(f"Found {len(stems)} stems: {[s['name'] for s in stems]}")
        
        if not stems:
            raise Exception("No stems were generated")
        
        return {
            "file_id": request.file_id,
            "stems": stems,
            "message": "Stems separated successfully"
        }
        
    except HTTPException as he:
        # Re-raise HTTP exceptions as-is
        raise he
    except Exception as e:
        print(f"Error separating stems: {str(e)}")
        import traceback
        traceback.print_exc()
        error_detail = str(e)
        if "No such file or directory" in error_detail:
            error_detail = "Archivo de audio no encontrado. Asegúrate de descargar el audio primero."
        raise HTTPException(status_code=400, detail=f"Error al separar stems: {error_detail}")

@app.get("/api/download-file/{file_id}")
async def download_file(file_id: str):
    """Download the audio file"""
    file_path = DOWNLOADS_DIR / f"{file_id}.mp3"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Get original filename from metadata
    filename = file_metadata.get(file_id, {}).get('filename', f"audio_{file_id}.mp3")
    
    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=filename
    )

@app.get("/api/download-video-file/{file_id}")
async def download_video_file(file_id: str):
    """Download the video file"""
    file_path = DOWNLOADS_DIR / f"{file_id}.mp4"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Video file not found")
    
    # Get original filename from metadata
    filename = file_metadata.get(file_id, {}).get('filename', f"video_{file_id}.mp4")
    
    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename
    )

@app.get("/api/download-stem/{file_id}/{stem_name}")
async def download_stem(file_id: str, stem_name: str):
    """Download a specific stem"""
    # Buscar en múltiples ubicaciones posibles
    possible_paths = [
        STEMS_DIR / config.DEMUCS_MODEL_FULL / file_id / f"{stem_name}.mp3",
        STEMS_DIR / config.DEMUCS_MODEL_FAST / file_id / f"{stem_name}.mp3",
        STEMS_DIR / "htdemucs_ft" / file_id / f"{stem_name}.mp3",
        STEMS_DIR / "htdemucs" / file_id / f"{stem_name}.mp3",
    ]
    
    stem_path = None
    for path in possible_paths:
        if path.exists():
            stem_path = path
            break
    
    if not stem_path:
        raise HTTPException(status_code=404, detail="Stem file not found")
    
    # Get original title from metadata and create descriptive filename
    original_title = file_metadata.get(file_id, {}).get('title', 'audio')
    filename = f"{original_title} - {stem_name}.mp3"
    
    return FileResponse(
        path=stem_path,
        media_type="audio/mpeg",
        filename=filename
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
