"""
Proxy Manager - Maneja proxies públicos gratuitos con rotación automática
"""

import requests
import random
from typing import Optional, List

class ProxyManager:
    def __init__(self):
        self.proxies: List[str] = []
        self.current_index = 0
        self.load_proxies()
    
    def load_proxies(self):
        """Carga lista de proxies públicos gratuitos"""
        # Lista de proxies públicos confiables (actualizar periódicamente)
        # Estos son ejemplos - en producción usar API de proxies
        self.proxies = [
            # Formato: http://ip:puerto
            "http://proxy.server.com:8080",  # Placeholder
        ]
        
        # Intentar cargar desde API pública
        try:
            # Free Proxy List API
            response = requests.get(
                "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
                timeout=5
            )
            if response.status_code == 200:
                proxy_list = response.text.strip().split('\n')
                self.proxies = [f"http://{proxy}" for proxy in proxy_list if proxy]
                print(f"✅ Loaded {len(self.proxies)} public proxies")
        except Exception as e:
            print(f"⚠️ Could not load public proxies: {e}")
            # Fallback: usar sin proxy
            self.proxies = []
    
    def get_proxy(self) -> Optional[str]:
        """Obtiene el siguiente proxy de la lista"""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
    
    def get_random_proxy(self) -> Optional[str]:
        """Obtiene un proxy aleatorio"""
        if not self.proxies:
            return None
        return random.choice(self.proxies)
    
    def test_proxy(self, proxy: str) -> bool:
        """Prueba si un proxy funciona"""
        try:
            response = requests.get(
                "https://www.google.com",
                proxies={"http": proxy, "https": proxy},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False

# Instancia global
proxy_manager = ProxyManager()
