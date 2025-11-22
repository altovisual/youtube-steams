from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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
import config

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

@app.post("/api/video-info")
async def get_video_info(video: VideoURL):
    """Get video information including title, artist, thumbnail, duration"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'ignoreerrors': False,
            'no_color': True,
            'noplaylist': True,  # IMPORTANTE: Solo descargar el video, no la playlist
            **config.YTDLP_EXTRA_OPTS,  # Agregar opciones extra para evitar detección de bots
        }
        
        print(f"Fetching info for URL: {video.url}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video.url, download=False)
            
            if not info:
                raise HTTPException(status_code=400, detail="No se pudo obtener información del video")
            
            # Extract relevant information
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
            
            print(f"Video info retrieved: {video_info['title']}")
            return video_info
            
    except Exception as e:
        print(f"Error fetching video info: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Error al obtener información del video: {str(e)}")

@app.post("/api/download")
async def download_audio(video: VideoURL):
    """Download audio from YouTube video - OPTIMIZADO PARA MÁXIMA CALIDAD Y VELOCIDAD"""
    try:
        file_id = str(uuid.uuid4())
        output_path = DOWNLOADS_DIR / f"{file_id}.mp3"
        
        ydl_opts = {
            'format': config.YTDLP_FORMAT,  # Mejor formato de audio disponible
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': config.AUDIO_FORMAT,
                'preferredquality': config.AUDIO_QUALITY,
            }, {
                'key': 'FFmpegMetadata',  # Preservar metadata
            }],
            'outtmpl': str(DOWNLOADS_DIR / f"{file_id}.%(ext)s"),
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'concurrent_fragment_downloads': 5,  # Descargas paralelas (más rápido)
            'retries': 10,
            'fragment_retries': 10,
            'http_chunk_size': 10485760,  # 10MB chunks (más rápido)
            'postprocessor_args': {
                'ffmpeg': [
                    '-threads', str(config.FFMPEG_THREADS),  # Usar todos los threads
                    '-b:a', config.AUDIO_BITRATE,  # Bitrate fijo 320k
                    '-ar', '48000',  # Sample rate 48kHz (alta calidad)
                ]
            },
            **config.YTDLP_EXTRA_OPTS,  # Agregar opciones extra para evitar detección de bots
        }
        
        print(f"Downloading audio: {video.url}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video.url, download=True)
        
        title = info.get('title', 'audio')
        clean_title = sanitize_filename(title)
        
        # Store metadata
        file_metadata[file_id] = {
            'title': clean_title,
            'filename': f"{clean_title}.mp3",
            'type': 'audio'
        }
        
        print(f"Download complete: {title}")
            
        return {
            "file_id": file_id,
            "filename": f"{clean_title}.mp3",
            "message": "Download completed successfully"
        }
        
    except Exception as e:
        print(f"Error downloading: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error downloading audio: {str(e)}")

@app.post("/api/download-video")
async def download_video(video: VideoURL):
    """Download video from YouTube in high quality - OPTIMIZADO PARA MÁXIMA CALIDAD"""
    try:
        file_id = str(uuid.uuid4())
        
        ydl_opts = {
            'format': config.VIDEO_FORMAT,  # Mejor video + audio disponible
            'outtmpl': str(DOWNLOADS_DIR / f"{file_id}.%(ext)s"),
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'concurrent_fragment_downloads': 5,
            'retries': 10,
            'fragment_retries': 10,
            'http_chunk_size': 10485760,  # 10MB chunks
            'merge_output_format': 'mp4',  # Asegurar que el output sea MP4
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }, {
                'key': 'FFmpegMetadata',  # Preservar metadata
            }],
            'postprocessor_args': {
                'ffmpeg': [
                    '-threads', str(config.FFMPEG_THREADS),
                ]
            },
            **config.YTDLP_EXTRA_OPTS,  # Agregar opciones extra para evitar detección de bots
        }
        
        print(f"Downloading video: {video.url}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video.url, download=True)
        
        title = info.get('title', 'video')
        clean_title = sanitize_filename(title)
        
        # Store metadata
        file_metadata[file_id] = {
            'title': clean_title,
            'filename': f"{clean_title}.mp4",
            'type': 'video'
        }
        
        print(f"Video download complete: {title}")
            
        return {
            "file_id": file_id,
            "filename": f"{clean_title}.mp4",
            "message": "Video download completed successfully"
        }
        
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
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
