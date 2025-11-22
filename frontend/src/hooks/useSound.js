import { useCallback } from 'react'

export const useSound = () => {
  const playSuccess = useCallback(() => {
    // Create audio context
    const audioContext = new (window.AudioContext || window.webkitAudioContext)()
    
    // Success sound - ascending notes
    const playNote = (frequency, startTime, duration) => {
      const oscillator = audioContext.createOscillator()
      const gainNode = audioContext.createGain()
      
      oscillator.connect(gainNode)
      gainNode.connect(audioContext.destination)
      
      oscillator.frequency.value = frequency
      oscillator.type = 'sine'
      
      gainNode.gain.setValueAtTime(0, startTime)
      gainNode.gain.linearRampToValueAtTime(0.3, startTime + 0.01)
      gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + duration)
      
      oscillator.start(startTime)
      oscillator.stop(startTime + duration)
    }
    
    const now = audioContext.currentTime
    playNote(523.25, now, 0.15)        // C5
    playNote(659.25, now + 0.1, 0.15)  // E5
    playNote(783.99, now + 0.2, 0.25)  // G5
  }, [])

  const playComplete = useCallback(() => {
    // Create audio context
    const audioContext = new (window.AudioContext || window.webkitAudioContext)()
    
    // Complete sound - triumphant chord
    const playChord = (frequencies, startTime, duration) => {
      frequencies.forEach(frequency => {
        const oscillator = audioContext.createOscillator()
        const gainNode = audioContext.createGain()
        
        oscillator.connect(gainNode)
        gainNode.connect(audioContext.destination)
        
        oscillator.frequency.value = frequency
        oscillator.type = 'sine'
        
        gainNode.gain.setValueAtTime(0, startTime)
        gainNode.gain.linearRampToValueAtTime(0.2, startTime + 0.01)
        gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + duration)
        
        oscillator.start(startTime)
        oscillator.stop(startTime + duration)
      })
    }
    
    const now = audioContext.currentTime
    // C major chord
    playChord([523.25, 659.25, 783.99], now, 0.4)
  }, [])

  const playStemsComplete = useCallback(() => {
    // Create audio context
    const audioContext = new (window.AudioContext || window.webkitAudioContext)()
    
    // Stems complete sound - magical ascending arpeggio
    const playNote = (frequency, startTime, duration) => {
      const oscillator = audioContext.createOscillator()
      const gainNode = audioContext.createGain()
      
      oscillator.connect(gainNode)
      gainNode.connect(audioContext.destination)
      
      oscillator.frequency.value = frequency
      oscillator.type = 'triangle'
      
      gainNode.gain.setValueAtTime(0, startTime)
      gainNode.gain.linearRampToValueAtTime(0.25, startTime + 0.01)
      gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + duration)
      
      oscillator.start(startTime)
      oscillator.stop(startTime + duration)
    }
    
    const now = audioContext.currentTime
    playNote(523.25, now, 0.12)         // C5
    playNote(659.25, now + 0.08, 0.12)  // E5
    playNote(783.99, now + 0.16, 0.12)  // G5
    playNote(1046.50, now + 0.24, 0.3)  // C6
  }, [])

  return {
    playSuccess,
    playComplete,
    playStemsComplete
  }
}
