# 🎵 YouTube Music Downloader

Una aplicación moderna y rápida para descargar música de YouTube y separar los stems (vocals, drums, bass, other) de tus canciones favoritas.

## ✨ Características

- 🎬 **Descarga audio de YouTube** en formato MP3 de alta calidad (320kbps)
- 🎼 **Separación de stems** usando Demucs (state-of-the-art AI)
- 🖼️ **Interfaz hermosa** con diseño moderno inspirado en Genius
- ⚡ **Rápido y optimizado** con React + FastAPI
- 📱 **Responsive** - funciona en desktop y móvil

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno y rápido
- **yt-dlp** - Descargador de YouTube más actualizado
- **Demucs** - Separación de stems con IA
- **Python 3.9+**

### Frontend
- **React 18** - Biblioteca UI moderna
- **Vite** - Build tool ultra rápido
- **TailwindCSS** - Estilos utility-first
- **Lucide React** - Iconos hermosos
- **Axios** - Cliente HTTP

## 📦 Instalación

### Requisitos Previos

- Python 3.9 o superior
- Node.js 18 o superior
- FFmpeg instalado en tu sistema

#### Instalar FFmpeg (Windows)

```bash
# Usando Chocolatey
choco install ffmpeg

# O descarga desde: https://ffmpeg.org/download.html
```

### 1. Clonar el repositorio

```bash
cd youtube-descarga
```

### 2. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Frontend

```bash
cd ../frontend

# Instalar dependencias
npm install
```

## 🚀 Uso

### Iniciar Backend

```bash
cd backend
.\venv\Scripts\activate  # Si no está activado
python main.py
```

El backend estará corriendo en: `http://localhost:8000`

### Iniciar Frontend

```bash
cd frontend
npm run dev
```

El frontend estará corriendo en: `http://localhost:5173`

## 📖 Cómo Usar

1. **Abre la aplicación** en tu navegador: `http://localhost:5173`
2. **Pega el link** de YouTube de la canción que quieres descargar
3. **Haz clic en buscar** - verás la información de la canción con su cover
4. **Descarga el audio** haciendo clic en "Descargar Audio MP3"
5. **Separa los stems** (opcional) haciendo clic en "Separar Stems"
6. **Descarga los stems individuales** (vocals, drums, bass, other)

## 🎨 Características de la UI

- **Gradiente vibrante** de fondo (azul → púrpura → rosa)
- **Cards con glassmorphism** para un look moderno
- **Animaciones suaves** en hover y transiciones
- **Feedback visual** con loaders y estados de éxito
- **Responsive design** que se adapta a cualquier pantalla

## 🔧 API Endpoints

### `POST /api/video-info`
Obtiene información del video de YouTube
```json
{
  "url": "https://www.youtube.com/watch?v=..."
}
```

### `POST /api/download`
Descarga el audio del video
```json
{
  "url": "https://www.youtube.com/watch?v=..."
}
```

### `POST /api/separate-stems`
Separa el audio en stems
```json
{
  "file_id": "uuid-del-archivo"
}
```

### `GET /api/download-file/{file_id}`
Descarga el archivo de audio completo

### `GET /api/download-stem/{file_id}/{stem_name}`
Descarga un stem específico

## ⚠️ Notas Importantes

- La separación de stems puede tomar **varios minutos** dependiendo de la duración de la canción
- Se requiere una **GPU** para separación de stems más rápida (opcional)
- Los archivos descargados se guardan en `backend/downloads` y `backend/stems`
- Asegúrate de tener **suficiente espacio en disco** para los archivos

## 🐛 Solución de Problemas

### Error: "FFmpeg not found"
Instala FFmpeg y asegúrate de que está en tu PATH

### Error al separar stems
Demucs requiere PyTorch. Si tienes problemas, instala la versión CPU:
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Puerto ya en uso
Cambia el puerto en `backend/main.py` o `frontend/vite.config.js`

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Si encuentras un bug o tienes una sugerencia, abre un issue.

## ❤️ Créditos

- **yt-dlp** - Descarga de YouTube
- **Demucs** - Separación de stems con IA
- **FastAPI** - Framework backend
- **React** - Framework frontend
- **TailwindCSS** - Estilos

---

Hecho con ❤️ para los amantes de la música
