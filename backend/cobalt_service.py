"""
Cobalt API Service - Alternativa a yt-dlp para evitar bloqueos de YouTube
https://github.com/imputnet/cobalt

Nota: Cobalt API ahora requiere autenticación en la mayoría de instancias.
Usamos instancias públicas disponibles con fallback a yt-dlp.
"""

import httpx
import os
from typing import Optional, Dict, Any

# Instancias públicas de Cobalt que aún funcionan (actualizar si cambian)
# Nota: La API oficial (api.cobalt.tools) ahora requiere API key
COBALT_INSTANCES = [
    "https://cobalt.api.timelessnesses.me",
    "https://api.cobalt.best",
    "https://cobalt-api.kwiatekmiki.com",
    "https://dl.khyernet.xyz",
]

class CobaltService:
    def __init__(self):
        self.current_instance = 0
        self.timeout = 60.0  # segundos
    
    def _get_instance(self) -> str:
        """Obtiene la instancia actual de Cobalt"""
        return COBALT_INSTANCES[self.current_instance % len(COBALT_INSTANCES)]
    
    def _rotate_instance(self):
        """Rota a la siguiente instancia si hay error"""
        self.current_instance += 1
    
    async def get_download_url(
        self, 
        url: str, 
        download_mode: str = "auto",  # auto, audio, mute
        audio_format: str = "mp3",
        audio_bitrate: str = "320",
        video_quality: str = "1080"
    ) -> Dict[str, Any]:
        """
        Obtiene la URL de descarga desde Cobalt
        
        Args:
            url: URL del video de YouTube
            download_mode: "auto" (video+audio), "audio" (solo audio), "mute" (video sin audio)
            audio_format: "mp3", "ogg", "wav", "opus", "best"
            audio_bitrate: "320", "256", "128", "96", "64"
            video_quality: "max", "2160", "1080", "720", "480", "360"
        
        Returns:
            Dict con status, url de descarga, filename, etc.
        """
        
        payload = {
            "url": url,
            "downloadMode": download_mode,
            "audioFormat": audio_format,
            "audioBitrate": audio_bitrate,
            "videoQuality": video_quality,
            "filenameStyle": "basic",
            "disableMetadata": False,
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        
        last_error = None
        
        # Intentar con cada instancia
        for attempt in range(len(COBALT_INSTANCES)):
            instance = self._get_instance()
            
            try:
                print(f"🔄 Usando Cobalt: {instance}")
                
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        instance,
                        json=payload,
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        print(f"✅ Cobalt response: {data.get('status')}")
                        return data
                    else:
                        print(f"❌ Cobalt error {response.status_code}: {response.text}")
                        last_error = f"HTTP {response.status_code}"
                        self._rotate_instance()
                        
            except Exception as e:
                print(f"❌ Error con {instance}: {str(e)}")
                last_error = str(e)
                self._rotate_instance()
        
        return {
            "status": "error",
            "error": {
                "code": "service.unavailable",
                "message": f"No se pudo conectar a Cobalt: {last_error}"
            }
        }
    
    async def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene información del video (título, thumbnail, etc.)
        Nota: Cobalt no tiene endpoint de info, así que hacemos una request
        y extraemos lo que podamos del filename
        """
        # Por ahora retornamos None, usaremos yt-dlp solo para info
        # ya que no requiere cookies para metadata básica
        return None


# Instancia global
cobalt_service = CobaltService()
