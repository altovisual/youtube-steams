# 🔬 Documentación Técnica

## 🏗️ Arquitectura

### **Patrón de Diseño**: Cliente-Servidor con API REST

```
┌─────────────────┐         HTTP/REST        ┌─────────────────┐
│                 │ ◄────────────────────────►│                 │
│  React Frontend │                           │  FastAPI Backend│
│   (Port 5173)   │                           │   (Port 8000)   │
│                 │                           │                 │
└─────────────────┘                           └─────────────────┘
                                                       │
                                                       ▼
                                              ┌────────────────┐
                                              │   yt-dlp       │
                                              │   Demucs       │
                                              │   FFmpeg       │
                                              └────────────────┘
```

## 🔧 Backend (FastAPI)

### **Tecnologías Core**

#### **FastAPI**
- Framework web moderno basado en Starlette
- Async/await nativo
- Validación automática con Pydantic
- Documentación auto-generada (Swagger UI)
- Alto rendimiento (comparable a Node.js y Go)

#### **yt-dlp**
- Fork actualizado de youtube-dl
- Soporte para 1000+ sitios
- Extracción de metadata
- Descarga de audio/video
- Post-procesamiento con FFmpeg

#### **Demucs**
- Modelo de IA para separación de fuentes
- Basado en PyTorch
- Arquitectmo U-Net con transformers
- 4 stems: vocals, drums, bass, other
- Modelo htdemucs: state-of-the-art

### **Endpoints Detallados**

#### `POST /api/video-info`
```python
Request:
{
  "url": "https://youtube.com/watch?v=..."
}

Response:
{
  "id": "video_id",
  "title": "Song Title",
  "artist": "Artist Name",
  "thumbnail": "https://...",
  "duration": 180,  # seconds
  "view_count": 1000000,
  "upload_date": "20231115",
  "description": "..."
}
```

#### `POST /api/download`
```python
Request:
{
  "url": "https://youtube.com/watch?v=..."
}

Response:
{
  "file_id": "uuid-v4",
  "filename": "Song Title.mp3",
  "message": "Download completed successfully"
}
```

#### `POST /api/separate-stems`
```python
Request:
{
  "file_id": "uuid-v4"
}

Response:
{
  "file_id": "uuid-v4",
  "stems": [
    {"name": "vocals", "file_id": "uuid/vocals.mp3"},
    {"name": "drums", "file_id": "uuid/drums.mp3"},
    {"name": "bass", "file_id": "uuid/bass.mp3"},
    {"name": "other", "file_id": "uuid/other.mp3"}
  ],
  "message": "Stems separated successfully"
}
```

### **Procesamiento de Audio**

#### **Descarga con yt-dlp**
```python
ydl_opts = {
    'format': 'bestaudio/best',  # Mejor calidad de audio
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',  # 320 kbps
    }],
    'outtmpl': 'downloads/%(id)s.%(ext)s',
}
```

#### **Separación con Demucs**
```bash
demucs --mp3 --mp3-bitrate 320 -o stems -n htdemucs audio.mp3
```

**Proceso interno**:
1. Carga el audio
2. Normaliza la amplitud
3. Divide en chunks (si es muy largo)
4. Procesa cada chunk con el modelo
5. Recombina los chunks
6. Exporta 4 stems separados

**Modelos disponibles**:
- `htdemucs`: Hybrid Transformer Demucs (mejor calidad)
- `htdemucs_ft`: Fine-tuned (más rápido)
- `mdx_extra`: Modelo alternativo

### **Gestión de Archivos**

```python
downloads/
  ├── {uuid1}.mp3
  ├── {uuid2}.mp3
  └── ...

stems/
  └── htdemucs/
      ├── {uuid1}/
      │   ├── vocals.mp3
      │   ├── drums.mp3
      │   ├── bass.mp3
      │   └── other.mp3
      └── {uuid2}/
          └── ...
```

## 🎨 Frontend (React)

### **Tecnologías Core**

#### **React 18**
- Hooks (useState, useEffect)
- Componentes funcionales
- Virtual DOM para rendimiento
- Concurrent features

#### **Vite**
- Build tool ultra rápido
- Hot Module Replacement (HMR)
- Optimización automática
- ESBuild para transpilación

#### **TailwindCSS**
- Utility-first CSS
- JIT compiler
- PurgeCSS integrado
- Responsive design

### **Componentes Detallados**

#### **App.jsx**
```jsx
State:
- videoInfo: null | VideoInfo
- loading: boolean

Funciones:
- Maneja estado global
- Renderiza layout principal
```

#### **UrlInput.jsx**
```jsx
Props:
- onVideoInfo: (info) => void
- loading: boolean
- setLoading: (bool) => void

State:
- url: string
- error: string

Funciones:
- handleSubmit: Valida y envía URL
- Maneja errores de API
```

#### **VideoCard.jsx**
```jsx
Props:
- videoInfo: VideoInfo

State:
- downloading: boolean
- separating: boolean
- downloadComplete: boolean
- stems: Stem[]
- fileId: string | null
- error: string

Funciones:
- handleDownload: Descarga audio
- handleSeparateStems: Inicia separación
- handleDownloadStem: Descarga stem individual
```

### **Utilidades**

#### **cn() - Class Names**
```javascript
// Combina clases de Tailwind
cn('base-class', condition && 'conditional-class', {
  'class-1': true,
  'class-2': false
})
```

#### **formatDuration()**
```javascript
formatDuration(185) // "3:05"
formatDuration(3661) // "61:01"
```

#### **formatNumber()**
```javascript
formatNumber(1500) // "1.5K"
formatNumber(2500000) // "2.5M"
```

### **Estilos y Animaciones**

#### **Gradientes**
```css
/* Background principal */
bg-gradient-to-br from-blue-600 via-purple-600 to-pink-500

/* Botones primary */
bg-gradient-to-r from-blue-500 to-purple-600

/* Botones secondary */
bg-gradient-to-r from-purple-500 to-pink-600
```

#### **Animaciones**
```css
/* Hover scale */
hover:scale-[1.02]

/* Spin (loading) */
animate-spin

/* Fade in */
animate-in fade-in slide-in-from-bottom-4
```

#### **Glassmorphism**
```css
bg-white/95 backdrop-blur-sm
```

## 🔄 Flujo de Datos Completo

### **1. Obtener Info del Video**
```
Usuario ingresa URL
  ↓
UrlInput.jsx → axios.post('/api/video-info', {url})
  ↓
FastAPI → yt_dlp.extract_info(url, download=False)
  ↓
YouTube API → Metadata
  ↓
FastAPI → JSON response
  ↓
UrlInput.jsx → onVideoInfo(data)
  ↓
App.jsx → setVideoInfo(data)
  ↓
VideoCard.jsx renderiza
```

### **2. Descargar Audio**
```
Usuario hace clic en "Descargar"
  ↓
VideoCard.jsx → axios.post('/api/download', {url})
  ↓
FastAPI → yt_dlp.download(url)
  ↓
yt-dlp → Descarga de YouTube
  ↓
FFmpeg → Convierte a MP3 320kbps
  ↓
Guarda en downloads/{uuid}.mp3
  ↓
FastAPI → JSON response con file_id
  ↓
VideoCard.jsx → window.open('/api/download-file/{id}')
  ↓
Navegador descarga el archivo
```

### **3. Separar Stems**
```
Usuario hace clic en "Separar Stems"
  ↓
VideoCard.jsx → axios.post('/api/separate-stems', {file_id})
  ↓
FastAPI → asyncio.create_subprocess_shell('demucs ...')
  ↓
Demucs carga modelo (primera vez: descarga ~300MB)
  ↓
Demucs procesa audio con IA
  ↓
Genera 4 archivos MP3 en stems/htdemucs/{uuid}/
  ↓
FastAPI → JSON response con lista de stems
  ↓
VideoCard.jsx → Renderiza botones de stems
  ↓
Usuario hace clic en stem
  ↓
window.open('/api/download-stem/{id}/{name}')
  ↓
Navegador descarga el stem
```

## 📊 Rendimiento

### **Tiempos Aproximados**

| Operación | CPU | GPU | Notas |
|-----------|-----|-----|-------|
| Obtener info | <1s | <1s | Muy rápido |
| Descargar 3min | 5-10s | 5-10s | Depende de internet |
| Separar 3min | 2-5min | 30-60s | GPU 10x más rápido |

### **Uso de Recursos**

| Recurso | Descarga | Separación |
|---------|----------|------------|
| CPU | 10-20% | 80-100% |
| RAM | 100MB | 2-4GB |
| Disco | +5MB/min | +20MB/min |
| Red | Variable | 0 |

### **Optimizaciones**

#### **Backend**
- Async/await para no bloquear
- Streaming de archivos grandes
- Compresión de respuestas
- Cache de metadata (futuro)

#### **Frontend**
- Code splitting con Vite
- Lazy loading de componentes
- Optimización de imágenes
- Debouncing de inputs (futuro)

## 🔐 Seguridad

### **CORS**
```python
allow_origins = [
    "http://localhost:5173",
    "http://localhost:3000"
]
```

### **Validación**
- Pydantic valida todos los inputs
- URLs sanitizadas antes de procesar
- File IDs son UUIDs (no predecibles)

### **Limitaciones**
- Sin rate limiting (uso local)
- Sin autenticación (no necesaria)
- Sin encriptación (HTTP local)

## 🧪 Testing (Futuro)

### **Backend**
```python
# pytest
def test_video_info():
    response = client.post("/api/video-info", 
                          json={"url": "..."})
    assert response.status_code == 200
```

### **Frontend**
```javascript
// Jest + React Testing Library
test('renders input', () => {
  render(<UrlInput />)
  expect(screen.getByPlaceholderText(/pega/i)).toBeInTheDocument()
})
```

## 📦 Deployment (Futuro)

### **Docker**
```dockerfile
# Backend
FROM python:3.11
RUN apt-get install ffmpeg
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

# Frontend
FROM node:18
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "run", "preview"]
```

### **Producción**
- Nginx como reverse proxy
- HTTPS con Let's Encrypt
- Rate limiting
- Autenticación JWT
- Base de datos para historial
- Redis para cache

## 🔮 Roadmap Técnico

### **v1.1**
- [ ] WebSocket para progreso en tiempo real
- [ ] Cola de trabajos con Celery
- [ ] Cache con Redis

### **v1.2**
- [ ] Base de datos (PostgreSQL)
- [ ] Autenticación de usuarios
- [ ] Historial de descargas

### **v2.0**
- [ ] Soporte para playlists
- [ ] Conversión a múltiples formatos
- [ ] Visualizador de audio con WaveSurfer.js
- [ ] Editor básico de stems

---

Documentación técnica completa para desarrolladores 🚀
