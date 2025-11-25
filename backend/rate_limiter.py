"""
Rate Limiter - Sistema de límites por IP
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
from fastapi import HTTPException, Request

class RateLimiter:
    def __init__(self, max_downloads: int = 5, window_hours: int = 24):
        """
        Args:
            max_downloads: Máximo de descargas permitidas por IP
            window_hours: Ventana de tiempo en horas
        """
        self.max_downloads = max_downloads
        self.window_hours = window_hours
        self.ip_records: Dict[str, list] = {}  # {ip: [timestamp1, timestamp2, ...]}
    
    def _clean_old_records(self, ip: str):
        """Elimina registros fuera de la ventana de tiempo"""
        if ip not in self.ip_records:
            return
        
        cutoff = datetime.now() - timedelta(hours=self.window_hours)
        self.ip_records[ip] = [ts for ts in self.ip_records[ip] if ts > cutoff]
    
    def get_client_ip(self, request: Request) -> str:
        """Obtiene la IP real del cliente (considera proxies)"""
        # Render y otros servicios usan X-Forwarded-For
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            # El primer IP es el cliente real
            return forwarded.split(",")[0].strip()
        
        # Fallback a la IP directa
        return request.client.host if request.client else "unknown"
    
    def check_limit(self, request: Request) -> Dict:
        """
        Verifica si el IP puede hacer una descarga.
        Returns: {allowed: bool, remaining: int, reset_time: str}
        """
        ip = self.get_client_ip(request)
        self._clean_old_records(ip)
        
        if ip not in self.ip_records:
            self.ip_records[ip] = []
        
        current_count = len(self.ip_records[ip])
        remaining = max(0, self.max_downloads - current_count)
        
        # Calcular tiempo de reset
        if self.ip_records[ip]:
            oldest = min(self.ip_records[ip])
            reset_time = oldest + timedelta(hours=self.window_hours)
        else:
            reset_time = datetime.now() + timedelta(hours=self.window_hours)
        
        return {
            "allowed": current_count < self.max_downloads,
            "remaining": remaining,
            "total": self.max_downloads,
            "reset_time": reset_time.isoformat(),
            "ip": ip
        }
    
    def record_download(self, request: Request):
        """Registra una descarga para el IP"""
        ip = self.get_client_ip(request)
        self._clean_old_records(ip)
        
        if ip not in self.ip_records:
            self.ip_records[ip] = []
        
        self.ip_records[ip].append(datetime.now())
    
    def get_status(self, request: Request) -> Dict:
        """Obtiene el estado actual del límite para un IP"""
        return self.check_limit(request)


# Instancia global - 10 descargas cada 24 horas
rate_limiter = RateLimiter(max_downloads=10, window_hours=24)

# Instancia para stems - 3 separaciones cada 24 horas (más restrictivo)
stems_rate_limiter = RateLimiter(max_downloads=3, window_hours=24)


def check_rate_limit(request: Request):
    """Dependency para verificar límite antes de descargar"""
    status = rate_limiter.check_limit(request)
    
    if not status["allowed"]:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Límite de descargas alcanzado",
                "message": f"Has alcanzado el límite de {status['total']} descargas. Vuelve más tarde.",
                "remaining": 0,
                "reset_time": status["reset_time"]
            }
        )
    
    return status


def check_stems_rate_limit(request: Request):
    """Dependency para verificar límite antes de separar stems"""
    status = stems_rate_limiter.check_limit(request)
    
    if not status["allowed"]:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Límite de separación alcanzado",
                "message": f"Has alcanzado el límite de {status['total']} separaciones de stems por día. Vuelve mañana.",
                "remaining": 0,
                "reset_time": status["reset_time"]
            }
        )
    
    return status
