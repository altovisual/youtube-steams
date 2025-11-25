"""
Replicate API service for stem separation using Demucs
Uses cloud GPU for processing - much faster and doesn't require local resources
"""

import httpx
import asyncio
import os
from typing import Optional
from pathlib import Path

class ReplicateService:
    def __init__(self):
        self.base_url = "https://api.replicate.com/v1"
        # Modelo de Demucs en Replicate (htdemucs - versión correcta)
        self.model_version = "25a173108cff36ef9f80f854c162d01df9e6528be175794b81158fa03836d953"
        
    @property
    def api_token(self):
        return os.getenv('REPLICATE_API_TOKEN')
        
    def is_configured(self) -> bool:
        """Check if Replicate API is configured"""
        return bool(self.api_token)
    
    async def separate_stems(
        self, 
        audio_url: str, 
        two_stems: bool = True,
        output_format: str = "mp3"
    ) -> Optional[dict]:
        """
        Separate audio into stems using Replicate's Demucs model
        
        Args:
            audio_url: Public URL to the audio file
            two_stems: If True, only separate vocals and instrumental
            output_format: Output format (mp3, wav, flac)
            
        Returns:
            dict with stem URLs or None if failed
        """
        if not self.is_configured():
            print("❌ Replicate API not configured (REPLICATE_API_TOKEN not set)")
            return None
            
        try:
            print(f"🔗 Audio URL: {audio_url}")
            
            async with httpx.AsyncClient(timeout=600) as client:
                # Create prediction
                input_data = {
                    "audio": audio_url,
                    "output_format": output_format,
                }
                
                # Si es two_stems, separar solo vocals
                if two_stems:
                    input_data["stem"] = "vocals"
                
                print(f"📤 Sending to Replicate: {input_data}")
                
                response = await client.post(
                    f"{self.base_url}/predictions",
                    headers={
                        "Authorization": f"Token {self.api_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "version": self.model_version,
                        "input": input_data
                    }
                )
                
                if response.status_code != 201:
                    print(f"❌ Replicate API error: {response.status_code} - {response.text}")
                    return None
                
                prediction = response.json()
                prediction_id = prediction["id"]
                print(f"✅ Replicate prediction created: {prediction_id}")
                
                # Poll for completion (máximo 10 minutos)
                max_attempts = 300  # 300 * 2 segundos = 10 minutos
                attempts = 0
                
                while attempts < max_attempts:
                    await asyncio.sleep(2)
                    attempts += 1
                    
                    status_response = await client.get(
                        f"{self.base_url}/predictions/{prediction_id}",
                        headers={"Authorization": f"Token {self.api_token}"}
                    )
                    
                    status_data = status_response.json()
                    status = status_data["status"]
                    
                    if attempts % 5 == 0:  # Log cada 10 segundos
                        print(f"📊 Replicate status: {status} (attempt {attempts})")
                    
                    if status == "succeeded":
                        output = status_data.get("output")
                        print(f"✅ Replicate succeeded! Output: {output}")
                        return output
                    elif status == "failed":
                        error = status_data.get('error', 'Unknown error')
                        print(f"❌ Replicate failed: {error}")
                        return None
                    elif status == "canceled":
                        print("❌ Replicate prediction canceled")
                        return None
                
                print("❌ Replicate timeout (10 minutes)")
                return None
                        
        except Exception as e:
            print(f"❌ Replicate error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def download_stem(self, url: str, output_path: Path) -> bool:
        """Download a stem file from URL"""
        try:
            print(f"⬇️ Downloading stem from: {url}")
            async with httpx.AsyncClient(timeout=120, follow_redirects=True) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_bytes(response.content)
                    size_mb = len(response.content) / (1024 * 1024)
                    print(f"✅ Downloaded stem to: {output_path} ({size_mb:.2f} MB)")
                    return True
                else:
                    print(f"❌ Failed to download stem: {response.status_code}")
                    return False
        except Exception as e:
            print(f"❌ Error downloading stem: {e}")
            return False


replicate_service = ReplicateService()
