import { useEffect, useState } from 'react'
import { cn } from '../lib/utils'

export default function DownloadAnimation({ isActive, type = 'audio' }) {
  const [pulseIntensity, setPulseIntensity] = useState(0)

  useEffect(() => {
    if (!isActive) {
      setPulseIntensity(0)
      return
    }

    let intensity = 0
    let direction = 1

    const interval = setInterval(() => {
      intensity += direction * 0.05
      if (intensity >= 1) direction = -1
      if (intensity <= 0) direction = 1
      setPulseIntensity(intensity)
    }, 50)

    return () => clearInterval(interval)
  }, [isActive])

  if (!isActive) return null

  const colors = {
    audio: 'from-blue-500/20 via-cyan-500/20 to-blue-500/20',
    video: 'from-purple-500/20 via-pink-500/20 to-purple-500/20',
    stems: 'from-indigo-500/20 via-violet-500/20 to-indigo-500/20'
  }

  return (
    <div className="fixed inset-0 pointer-events-none z-0">
      {/* Animated gradient overlay */}
      <div 
        className={cn(
          "absolute inset-0 bg-gradient-to-t transition-opacity duration-1000",
          colors[type]
        )}
        style={{ 
          opacity: pulseIntensity * 0.5,
          animation: 'pulse-glow 2s ease-in-out infinite'
        }}
      />
      
      {/* Energy waves */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(3)].map((_, i) => (
          <div
            key={i}
            className={cn(
              "absolute bottom-0 left-0 right-0 h-1/3 bg-gradient-to-t opacity-30",
              colors[type]
            )}
            style={{
              animation: `wave-up ${2 + i * 0.5}s ease-in-out infinite`,
              animationDelay: `${i * 0.3}s`,
              transform: `translateY(${100 - pulseIntensity * 20}%)`
            }}
          />
        ))}
      </div>
    </div>
  )
}
