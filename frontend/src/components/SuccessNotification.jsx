import { useEffect, useState } from 'react'
import { CheckCircle2, Download, Video, Music } from 'lucide-react'
import { cn } from '../lib/utils'

export default function SuccessNotification({ show, type, message, onClose }) {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    if (show) {
      setIsVisible(true)
      const timer = setTimeout(() => {
        setIsVisible(false)
        setTimeout(() => onClose && onClose(), 300)
      }, 3000)
      return () => clearTimeout(timer)
    }
  }, [show, onClose])

  if (!show) return null

  const icons = {
    audio: Download,
    video: Video,
    stems: Music
  }

  const colors = {
    audio: 'from-blue-500 to-cyan-500',
    video: 'from-purple-500 to-pink-500',
    stems: 'from-indigo-500 to-violet-500'
  }

  const Icon = icons[type] || Download

  return (
    <div
      className={cn(
        "fixed top-8 right-8 z-50 transition-all duration-300 transform",
        isVisible ? "translate-x-0 opacity-100" : "translate-x-full opacity-0"
      )}
    >
      <div className={cn(
        "bg-white rounded-2xl shadow-2xl p-4 flex items-center gap-4 min-w-[320px]",
        "border-2 border-transparent bg-gradient-to-r",
        colors[type]
      )}>
        <div className="bg-white rounded-xl p-3">
          <div className={cn(
            "bg-gradient-to-br p-2 rounded-lg",
            colors[type]
          )}>
            <Icon className="w-6 h-6 text-white" />
          </div>
        </div>
        
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <CheckCircle2 className="w-5 h-5 text-green-500" />
            <h3 className="font-bold text-gray-900">¡Completado!</h3>
          </div>
          <p className="text-sm text-gray-600">{message}</p>
        </div>
      </div>
    </div>
  )
}
