# 🎬 Demo y Capturas

## 🎯 Características Visuales

### 1. **Pantalla Principal**
- Gradiente vibrante de fondo (azul → púrpura → rosa)
- Logo con icono de música
- Input de búsqueda con glassmorphism
- Diseño centrado y limpio

### 2. **Card de Video**
Cuando pegas un link de YouTube, aparece una hermosa card con:
- ✅ Thumbnail grande del video
- ✅ Título de la canción
- ✅ Nombre del artista
- ✅ Número de vistas
- ✅ Duración
- ✅ Botones de acción con gradientes

### 3. **Botones de Acción**

#### **Descargar Audio MP3**
- Gradiente azul → púrpura
- Icono de descarga
- Animación de loading mientras descarga
- Cambia a verde con checkmark cuando completa

#### **Separar Stems**
- Gradiente púrpura → rosa
- Icono de disco
- Mensaje de progreso (puede tomar varios minutos)
- Muestra los 4 stems cuando termina

### 4. **Lista de Stems**
Cuando la separación termina, aparecen 4 botones:
- 🎤 **vocals** - Solo la voz
- 🥁 **drums** - Solo la batería
- 🎸 **bass** - Solo el bajo
- 🎹 **other** - Otros instrumentos

Cada uno con:
- Fondo degradado suave
- Borde azul
- Hover effect
- Descarga directa al hacer clic

## 🎨 Diseño Inspirado en Genius

La interfaz está inspirada en la imagen de Genius que proporcionaste:
- **Layout similar**: Imagen grande a la izquierda, info a la derecha
- **Colores vibrantes**: Uso de gradientes llamativos
- **Tipografía clara**: Títulos grandes y legibles
- **Metadata visible**: Vistas, duración, artista
- **Botones de acción prominentes**: Fáciles de encontrar y usar

## 🚀 Flujo de Uso

```
1. Usuario abre http://localhost:5173
   ↓
2. Ve pantalla con gradiente hermoso y input grande
   ↓
3. Pega link de YouTube (ej: https://youtube.com/watch?v=...)
   ↓
4. Hace clic en buscar (icono de lupa)
   ↓
5. Aparece card con cover, título, artista, vistas
   ↓
6. Hace clic en "Descargar Audio MP3"
   ↓
7. Botón muestra loading spinner
   ↓
8. Descarga automática del MP3
   ↓
9. Botón cambia a verde con checkmark
   ↓
10. Hace clic en "Separar Stems"
    ↓
11. Mensaje: "La separación puede tomar varios minutos..."
    ↓
12. Aparecen 4 botones de stems
    ↓
13. Descarga los stems que quiera
```

## 💡 Detalles de UX

### **Feedback Visual**
- ✅ Loading spinners durante operaciones
- ✅ Cambio de color de botones al completar
- ✅ Mensajes de error en rojo si algo falla
- ✅ Animaciones suaves en hover
- ✅ Transiciones fluidas

### **Responsive**
- ✅ Funciona en desktop
- ✅ Se adapta a tablets
- ✅ Usable en móvil

### **Accesibilidad**
- ✅ Contraste alto en textos
- ✅ Botones grandes y fáciles de clickear
- ✅ Estados disabled claros
- ✅ Mensajes de error descriptivos

## 🎯 Ejemplos de Uso

### **Ejemplo 1: Descargar una canción**
```
URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Resultado: Rick Astley - Never Gonna Give You Up.mp3 (320kbps)
Tiempo: ~10 segundos
```

### **Ejemplo 2: Separar stems de una canción**
```
URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Resultado: 4 archivos MP3
  - vocals.mp3 (solo voz de Rick Astley)
  - drums.mp3 (solo batería)
  - bass.mp3 (solo bajo)
  - other.mp3 (otros instrumentos)
Tiempo: ~2-5 minutos (depende de la duración)
```

## 🌟 Características Destacadas

### **Velocidad**
- ⚡ React con Vite = carga instantánea
- ⚡ FastAPI = respuestas ultra rápidas
- ⚡ yt-dlp = descarga optimizada

### **Calidad**
- 🎵 Audio MP3 a 320kbps
- 🎵 Stems de alta calidad con Demucs
- 🎵 Sin pérdida de calidad en procesamiento

### **Experiencia**
- 😍 Interfaz hermosa y moderna
- 😍 Fácil de usar (3 clics y listo)
- 😍 Feedback visual constante
- 😍 Sin publicidad ni distracciones

## 📱 Compatibilidad

### **Navegadores**
- ✅ Chrome/Edge (recomendado)
- ✅ Firefox
- ✅ Safari
- ✅ Opera

### **Sistemas Operativos**
- ✅ Windows 10/11
- ✅ macOS
- ✅ Linux

### **Videos Soportados**
- ✅ YouTube (cualquier video con audio)
- ✅ YouTube Music
- ✅ Videos privados (si tienes acceso)
- ✅ Videos con restricción de edad (con cookies)

## 🎉 ¡Disfruta!

Esta aplicación combina:
- 🎨 Diseño hermoso
- ⚡ Velocidad extrema
- 🎵 Calidad profesional
- 🚀 Facilidad de uso

Todo en una sola herramienta local y gratuita.

---

**Nota**: Recuerda respetar los derechos de autor y usar esta herramienta solo para contenido que tengas permiso de descargar.
