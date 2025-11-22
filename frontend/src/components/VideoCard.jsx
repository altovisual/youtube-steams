import { useState } from 'react'
import { Download, Music, Loader2, Play, CheckCircle2, Disc3, Video } from 'lucide-react'
import axios from 'axios'
import { cn, formatDuration, formatNumber } from '../lib/utils'
import Button from './ui/Button'
import ParticlesBackground from './ParticlesBackground'
import DownloadAnimation from './DownloadAnimation'
import SuccessNotification from './SuccessNotification'
import { useSound } from '../hooks/useSound'
import { API_ENDPOINTS } from '../config/api'

export default function VideoCard({ videoInfo }) {
  const [downloading, setDownloading] = useState(false)
  const [downloadingVideo, setDownloadingVideo] = useState(false)
  const [separating, setSeparating] = useState(false)
  const [downloadComplete, setDownloadComplete] = useState(false)
  const [videoDownloadComplete, setVideoDownloadComplete] = useState(false)
  const [stems, setStems] = useState([])
  const [fileId, setFileId] = useState(null)
  const [videoFileId, setVideoFileId] = useState(null)
  const [error, setError] = useState('')
  const [notification, setNotification] = useState({ show: false, type: '', message: '' })
  
  const { playSuccess, playComplete, playStemsComplete } = useSound()

  const handleDownload = async () => {
    setError('')
    setDownloading(true)
    try {
      const response = await axios.post(API_ENDPOINTS.download, { 
        url: `https://www.youtube.com/watch?v=${videoInfo.id}` 
      })
      setFileId(response.data.file_id)
      setDownloadComplete(true)
      
      // Play success sound
      playSuccess()
      
      // Show notification
      setNotification({
        show: true,
        type: 'audio',
        message: 'Audio descargado exitosamente'
      })
      
      // Auto download file
      window.open(API_ENDPOINTS.downloadFile(response.data.file_id), '_blank')
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al descargar el audio')
    } finally {
      setDownloading(false)
    }
  }

  const handleDownloadVideo = async () => {
    setError('')
    setDownloadingVideo(true)
    try {
      const response = await axios.post(API_ENDPOINTS.downloadVideo, { 
        url: `https://www.youtube.com/watch?v=${videoInfo.id}` 
      })
      setVideoFileId(response.data.file_id)
      setVideoDownloadComplete(true)
      
      // Play complete sound
      playComplete()
      
      // Show notification
      setNotification({
        show: true,
        type: 'video',
        message: 'Video descargado exitosamente en HD'
      })
      
      // Auto download file
      window.open(API_ENDPOINTS.downloadVideoFile(response.data.file_id), '_blank')
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al descargar el video')
    } finally {
      setDownloadingVideo(false)
    }
  }

  const handleSeparateStems = async (twoStems = true) => {
    if (!fileId) {
      setError('Primero debes descargar el audio')
      return
    }

    console.log('Separating stems with:', { file_id: fileId, two_stems: twoStems })
    
    setError('')
    setSeparating(true)
    try {
      const response = await axios.post(API_ENDPOINTS.separateStems, { 
        file_id: fileId,
        two_stems: twoStems
      })
      
      console.log('Stems separation response:', response.data)
      setStems(response.data.stems)
      
      // Play stems complete sound
      playStemsComplete()
      
      // Show notification
      const mode = twoStems ? 'Voces e Instrumental' : '4 stems'
      setNotification({
        show: true,
        type: 'stems',
        message: `${mode} separados exitosamente`
      })
    } catch (err) {
      console.error('Error separating stems:', err)
      console.error('Error response:', err.response?.data)
      setError(err.response?.data?.detail || 'Error al separar los stems')
    } finally {
      setSeparating(false)
    }
  }

  const handleDownloadStem = (stemFileId) => {
    const [fId, stemName] = stemFileId.split('/')
    window.open(API_ENDPOINTS.downloadStem(fId, stemName.replace('.mp3', '')), '_blank')
  }

  return (
    <>
      {/* Success notification */}
      <SuccessNotification
        show={notification.show}
        type={notification.type}
        message={notification.message}
        onClose={() => setNotification({ show: false, type: '', message: '' })}
      />
      
      {/* Background animations when downloading */}
      <DownloadAnimation 
        isActive={downloading} 
        type="audio" 
      />
      <DownloadAnimation 
        isActive={downloadingVideo} 
        type="video" 
      />
      <DownloadAnimation 
        isActive={separating} 
        type="stems" 
      />
      <ParticlesBackground isActive={downloading || downloadingVideo || separating} />
      
      <div className="bg-white/95 backdrop-blur-sm rounded-3xl shadow-2xl overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-500 relative z-20">
        <div className="md:flex">
        {/* Thumbnail */}
        <div className="md:w-2/5 relative group">
          <img
            src={videoInfo.thumbnail}
            alt={videoInfo.title}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <div className="absolute bottom-4 left-4 right-4">
              <div className="flex items-center gap-2 text-white text-sm">
                <Play className="w-4 h-4" />
                <span>{formatDuration(videoInfo.duration)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Info & Actions */}
        <div className="md:w-3/5 p-8">
          <div className="mb-6">
            <h2 className="text-3xl font-bold text-gray-900 mb-2 line-clamp-2">
              {videoInfo.title}
            </h2>
            <p className="text-lg text-gray-600 mb-3">
              {videoInfo.artist}
            </p>
            <div className="flex items-center gap-4 text-sm text-gray-500">
              <span>{formatNumber(videoInfo.view_count)} vistas</span>
              <span>•</span>
              <span>{formatDuration(videoInfo.duration)}</span>
            </div>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          {/* Action Buttons */}
          <div className="space-y-3 mb-6">
            <Button
              onClick={handleDownload}
              disabled={downloading || downloadComplete}
              variant={downloadComplete ? "success" : "primary"}
              className={cn(
                "w-full",
                downloading && "animate-pulse shadow-2xl shadow-blue-500/50"
              )}
            >
              {downloading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Descargando Audio...
                </>
              ) : downloadComplete ? (
                <>
                  <CheckCircle2 className="w-5 h-5" />
                  Audio Descargado
                </>
              ) : (
                <>
                  <Download className="w-5 h-5" />
                  Descargar Audio MP3
                </>
              )}
            </Button>

            <Button
              onClick={handleDownloadVideo}
              disabled={downloadingVideo || videoDownloadComplete}
              variant={videoDownloadComplete ? "success" : "primary"}
              className={cn(
                "w-full",
                downloadingVideo && "animate-pulse shadow-2xl shadow-purple-500/50"
              )}
            >
              {downloadingVideo ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Descargando Video...
                </>
              ) : videoDownloadComplete ? (
                <>
                  <CheckCircle2 className="w-5 h-5" />
                  Video Descargado
                </>
              ) : (
                <>
                  <Video className="w-5 h-5" />
                  Descargar Video HD
                </>
              )}
            </Button>

            {/* Botones de separación de stems */}
            <div className="space-y-2">
              <div className="grid grid-cols-2 gap-2">
                <Button
                  onClick={() => handleSeparateStems(true)}
                  disabled={!downloadComplete || separating || stems.length > 0}
                  variant="secondary"
                  className={cn(
                    "w-full text-sm",
                    separating && "animate-pulse shadow-2xl shadow-pink-500/50"
                  )}
                >
                  {separating ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span className="hidden sm:inline">Separando...</span>
                    </>
                  ) : stems.length > 0 ? (
                    <>
                      <CheckCircle2 className="w-4 h-4" />
                      <span className="hidden sm:inline">Separados</span>
                    </>
                  ) : (
                    <>
                      <Music className="w-4 h-4" />
                      <span>Voces + Pista</span>
                    </>
                  )}
                </Button>

                <Button
                  onClick={() => handleSeparateStems(false)}
                  disabled={!downloadComplete || separating || stems.length > 0}
                  variant="secondary"
                  className={cn(
                    "w-full text-sm",
                    separating && "animate-pulse shadow-2xl shadow-pink-500/50"
                  )}
                >
                  {separating ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span className="hidden sm:inline">Separando...</span>
                    </>
                  ) : stems.length > 0 ? (
                    <>
                      <CheckCircle2 className="w-4 h-4" />
                      <span className="hidden sm:inline">Separados</span>
                    </>
                  ) : (
                    <>
                      <Disc3 className="w-4 h-4" />
                      <span>4 Stems</span>
                    </>
                  )}
                </Button>
              </div>
              
              {!separating && stems.length === 0 && downloadComplete && (
                <div className="text-xs text-gray-500 text-center px-2">
                  <span className="font-semibold text-green-600">⚡ Rápido:</span> Voces + Instrumental | 
                  <span className="font-semibold text-blue-600 ml-1">🎵 Completo:</span> Vocals, Drums, Bass, Other
                </div>
              )}
            </div>
          </div>

          {/* Stems List */}
          {stems.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                <Music className="w-5 h-5" />
                Stems Disponibles
              </h3>
              <div className="grid grid-cols-2 gap-2">
                {stems.map((stem) => (
                  <button
                    key={stem.file_id}
                    onClick={() => handleDownloadStem(stem.file_id)}
                    className={cn(
                      "flex items-center gap-2 p-3 rounded-lg",
                      "bg-gradient-to-r from-blue-50 to-purple-50",
                      "border-2 border-blue-200",
                      "hover:border-blue-400 hover:shadow-md",
                      "transition-all duration-200",
                      "text-sm font-medium text-gray-700"
                    )}
                  >
                    <Download className="w-4 h-4" />
                    {stem.name}
                  </button>
                ))}
              </div>
            </div>
          )}

          {downloadingVideo && (
            <div className="mt-4 p-4 bg-purple-50 rounded-lg">
              <p className="text-sm text-purple-700">
                ⏳ La descarga de video puede tomar varios minutos dependiendo de la calidad y duración...
              </p>
            </div>
          )}

          {separating && (
            <div className="mt-4 p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-700 mb-2">
                ⏳ Separando stems...
              </p>
              <p className="text-xs text-blue-600">
                💡 <strong>Tip:</strong> El modo "Voces + Pista" es 2-3x más rápido que "4 Stems"
              </p>
            </div>
          )}
        </div>
      </div>
      </div>
    </>
  )
}
