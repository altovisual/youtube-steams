import { useState } from 'react'
import { Search, Loader2 } from 'lucide-react'
import axios from 'axios'
import { cn } from '../lib/utils'

export default function UrlInput({ onVideoInfo, loading, setLoading }) {
  const [url, setUrl] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    
    if (!url.trim()) {
      setError('Por favor ingresa una URL de YouTube')
      return
    }

    setLoading(true)
    try {
      const response = await axios.post('/api/video-info', { url })
      onVideoInfo(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al obtener información del video')
      onVideoInfo(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mb-8">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Pega aquí el link de YouTube..."
            className={cn(
              "w-full px-6 py-4 pr-14 rounded-2xl text-lg",
              "bg-white/95 backdrop-blur-sm",
              "border-2 border-transparent",
              "focus:outline-none focus:border-white focus:bg-white",
              "transition-all duration-200",
              "shadow-xl",
              error && "border-red-500"
            )}
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading}
            className={cn(
              "absolute right-2 top-1/2 -translate-y-1/2",
              "p-3 rounded-xl",
              "bg-gradient-to-r from-blue-500 to-purple-600",
              "text-white",
              "hover:shadow-lg hover:scale-105",
              "transition-all duration-200",
              "disabled:opacity-50 disabled:cursor-not-allowed"
            )}
          >
            {loading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Search className="w-5 h-5" />
            )}
          </button>
        </div>
      </form>
      
      {error && (
        <div className="mt-3 p-3 bg-red-500/90 text-white rounded-lg text-sm">
          {error}
        </div>
      )}
    </div>
  )
}
