import { useState, useEffect } from 'react'
import { Download, Clock } from 'lucide-react'
import { API_ENDPOINTS } from '../config/api'

function RateLimitBadge() {
  const [limitStatus, setLimitStatus] = useState(null)
  const [loading, setLoading] = useState(true)

  const fetchLimitStatus = async () => {
    try {
      const response = await fetch(API_ENDPOINTS.rateLimitStatus)
      if (response.ok) {
        const data = await response.json()
        setLimitStatus(data)
      }
    } catch (error) {
      console.error('Error fetching rate limit:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchLimitStatus()
    // Actualizar cada 30 segundos
    const interval = setInterval(fetchLimitStatus, 30000)
    return () => clearInterval(interval)
  }, [])

  // Escuchar evento de descarga completada para actualizar
  useEffect(() => {
    const handleDownload = () => {
      setTimeout(fetchLimitStatus, 1000)
    }
    window.addEventListener('download-complete', handleDownload)
    return () => window.removeEventListener('download-complete', handleDownload)
  }, [])

  if (loading || !limitStatus) return null

  const { remaining, total, reset_time } = limitStatus
  const percentage = (remaining / total) * 100
  
  // Formatear tiempo de reset
  const resetDate = new Date(reset_time)
  const now = new Date()
  const hoursUntilReset = Math.max(0, Math.ceil((resetDate - now) / (1000 * 60 * 60)))

  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2 flex items-center gap-3">
      <Download className="w-5 h-5 text-white/80" />
      <div className="flex flex-col">
        <div className="flex items-center gap-2">
          <span className="text-white font-medium">
            {remaining}/{total} descargas
          </span>
          {remaining === 0 && (
            <span className="text-xs bg-red-500/80 text-white px-2 py-0.5 rounded">
              Límite alcanzado
            </span>
          )}
        </div>
        {remaining < total && (
          <div className="flex items-center gap-1 text-white/60 text-xs">
            <Clock className="w-3 h-3" />
            <span>Se reinicia en {hoursUntilReset}h</span>
          </div>
        )}
      </div>
      {/* Barra de progreso */}
      <div className="w-20 h-2 bg-white/20 rounded-full overflow-hidden">
        <div 
          className={`h-full transition-all duration-300 ${
            remaining === 0 ? 'bg-red-500' : 
            remaining <= 2 ? 'bg-yellow-500' : 'bg-green-500'
          }`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}

export default RateLimitBadge
