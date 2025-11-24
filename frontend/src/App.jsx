import { useState } from 'react'
import { Music2, Loader2 } from 'lucide-react'
import UrlInput from './components/UrlInput'
import VideoCard from './components/VideoCard'
import RateLimitBadge from './components/RateLimitBadge'
import { cn } from './lib/utils'

function App() {
  const [videoInfo, setVideoInfo] = useState(null)
  const [loading, setLoading] = useState(false)

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-purple-600 to-pink-500 relative overflow-hidden">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          {/* Rate Limit Badge */}
          <div className="flex justify-end mb-4">
            <RateLimitBadge />
          </div>
          
          <div className="flex items-center justify-center gap-3 mb-4">
            <Music2 className="w-12 h-12 text-white" />
            <h1 className="text-5xl font-bold text-white">
              YouTube Music Downloader
            </h1>
          </div>
          <p className="text-white/90 text-lg">
            Descarga música y videos de YouTube en alta calidad y separa los stems de tus canciones favoritas
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          <UrlInput 
            onVideoInfo={setVideoInfo} 
            loading={loading}
            setLoading={setLoading}
          />

          {loading && (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-12 h-12 text-white animate-spin" />
            </div>
          )}

          {videoInfo && !loading && (
            <VideoCard videoInfo={videoInfo} />
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-16 text-white/70">
          <p>Desarrollado por Altovisual</p>
        </div>
      </div>
    </div>
  )
}

export default App
