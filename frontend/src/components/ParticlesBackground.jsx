import { useEffect, useRef } from 'react'

export default function ParticlesBackground({ isActive }) {
  const canvasRef = useRef(null)
  const particlesRef = useRef([])
  const animationFrameRef = useRef(null)

  useEffect(() => {
    if (!isActive) {
      // Clear animation when not active
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
      return
    }

    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    
    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    // Particle class
    class Particle {
      constructor() {
        this.reset()
      }

      reset() {
        this.x = Math.random() * canvas.width
        this.y = canvas.height + Math.random() * 100
        this.size = Math.random() * 4 + 1.5
        this.speedY = Math.random() * 5 + 3  // Más rápido
        this.speedX = Math.random() * 2 - 1
        this.opacity = Math.random() * 0.6 + 0.4  // Más brillante
        
        // Random colors: blue, purple, pink
        const colors = [
          { r: 59, g: 130, b: 246 },   // blue
          { r: 147, g: 51, b: 234 },   // purple
          { r: 236, g: 72, b: 153 },   // pink
          { r: 168, g: 85, b: 247 },   // violet
        ]
        this.color = colors[Math.floor(Math.random() * colors.length)]
      }

      update() {
        this.y -= this.speedY
        this.x += this.speedX
        
        // Add some wave motion
        this.x += Math.sin(this.y * 0.01) * 0.5

        // Reset particle when it goes off screen
        if (this.y < -10) {
          this.reset()
        }

        // Fade out near the top
        if (this.y < canvas.height * 0.3) {
          this.opacity = Math.max(0, this.opacity - 0.01)
        }
      }

      draw() {
        ctx.save()
        ctx.globalAlpha = this.opacity
        
        // Draw particle with glow effect
        const gradient = ctx.createRadialGradient(
          this.x, this.y, 0,
          this.x, this.y, this.size * 2
        )
        gradient.addColorStop(0, `rgba(${this.color.r}, ${this.color.g}, ${this.color.b}, 1)`)
        gradient.addColorStop(1, `rgba(${this.color.r}, ${this.color.g}, ${this.color.b}, 0)`)
        
        ctx.fillStyle = gradient
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.size * 2, 0, Math.PI * 2)
        ctx.fill()
        
        // Draw bright center
        ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity * 0.8})`
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.size * 0.5, 0, Math.PI * 2)
        ctx.fill()
        
        ctx.restore()
      }
    }

    // Create particles - más partículas para efecto más denso
    const particleCount = 150
    particlesRef.current = []
    for (let i = 0; i < particleCount; i++) {
      particlesRef.current.push(new Particle())
      // Stagger initial positions
      particlesRef.current[i].y = canvas.height + (i * 15)
    }

    // Animation loop
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      particlesRef.current.forEach(particle => {
        particle.update()
        particle.draw()
      })

      animationFrameRef.current = requestAnimationFrame(animate)
    }

    animate()

    // Cleanup
    return () => {
      window.removeEventListener('resize', resizeCanvas)
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
    }
  }, [isActive])

  if (!isActive) return null

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-10"
      style={{ mixBlendMode: 'screen' }}
    />
  )
}
