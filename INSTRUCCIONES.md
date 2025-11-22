# 🚀 Guía Rápida de Instalación

## ⚡ Instalación Rápida (Windows)

### 1. Instalar FFmpeg (REQUERIDO)

FFmpeg es necesario para procesar el audio. Opciones:

**Opción A - Chocolatey (Recomendado):**
```bash
choco install ffmpeg
```

**Opción B - Manual:**
1. Descarga FFmpeg desde: https://ffmpeg.org/download.html
2. Extrae el archivo ZIP
3. Agrega la carpeta `bin` al PATH de Windows

### 2. Ejecutar Instalador

Haz doble clic en `install.bat` - esto instalará todas las dependencias automáticamente.

### 3. Iniciar Aplicación

Haz doble clic en `start.bat` - esto abrirá dos ventanas:
- Backend (Python/FastAPI) en http://localhost:8000
- Frontend (React) en http://localhost:5173

### 4. Usar la Aplicación

1. Abre tu navegador en: http://localhost:5173
2. Pega un link de YouTube
3. ¡Descarga y disfruta!

---

## 🔧 Instalación Manual

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## ❓ Problemas Comunes

### "FFmpeg not found"
- Instala FFmpeg y reinicia tu terminal/PC

### "Python not found"
- Instala Python 3.9+ desde python.org
- Marca "Add Python to PATH" durante la instalación

### "npm not found"
- Instala Node.js desde nodejs.org

### Puerto ocupado
- Cierra otras aplicaciones que usen los puertos 8000 o 5173

---

## 📱 Características

✅ Descarga audio en MP3 320kbps
✅ Separación de stems con IA (vocals, drums, bass, other)
✅ Interfaz moderna y hermosa
✅ Muestra cover y metadata de la canción
✅ Descarga individual de cada stem

---

## 💡 Consejos

- La separación de stems puede tomar varios minutos
- Usa una GPU para procesamiento más rápido (opcional)
- Los archivos se guardan en `backend/downloads` y `backend/stems`

---

¿Necesitas ayuda? Revisa el README.md completo.
