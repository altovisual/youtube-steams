# 🚀 Guía de Despliegue

## Arquitectura de Despliegue

Esta aplicación requiere dos componentes:
1. **Frontend (React)** - Puede desplegarse en Vercel
2. **Backend (FastAPI + Python)** - Requiere servidor con Python (Railway, Render, etc.)

---

## 📦 Opción 1: Despliegue Completo

### Backend en Railway (Recomendado)

1. Ve a [Railway.app](https://railway.app)
2. Conecta tu repositorio de GitHub
3. Selecciona la carpeta `backend`
4. Railway detectará automáticamente Python
5. Configura las variables de entorno:
   ```
   PORT=8000
   ```
6. Copia la URL del backend (ej: `https://tu-app.railway.app`)

### Frontend en Vercel

1. Ve a [Vercel.com](https://vercel.com)
2. Importa tu repositorio de GitHub
3. Configura:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Agrega variable de entorno:
   ```
   VITE_API_URL=https://tu-app.railway.app
   ```
5. Despliega

### Actualizar Frontend para usar API_URL

Edita `frontend/vite.config.js`:
```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

---

## 📦 Opción 2: Despliegue Local con Túnel

Si prefieres mantener el backend local pero accesible:

1. Instala [ngrok](https://ngrok.com/)
2. Ejecuta el backend localmente
3. Crea un túnel:
   ```bash
   ngrok http 8000
   ```
4. Usa la URL de ngrok como `VITE_API_URL`

---

## 📦 Opción 3: Todo en un VPS

Desplegar ambos en un servidor VPS (DigitalOcean, AWS, etc.):

1. Instala Node.js y Python en el servidor
2. Clona el repositorio
3. Instala dependencias:
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install demucs
   
   # Frontend
   cd ../frontend
   npm install
   npm run build
   ```
4. Configura Nginx como reverse proxy
5. Usa PM2 para mantener los procesos corriendo

---

## ⚠️ Consideraciones Importantes

### Demucs
- Requiere ~500MB de espacio para los modelos
- Necesita buena CPU para procesamiento
- La primera ejecución descargará los modelos automáticamente

### CORS
El backend ya está configurado para aceptar peticiones del frontend.

### Límites
- Railway Free Tier: 500 horas/mes
- Vercel Free Tier: Ilimitado para proyectos personales

---

## 🔧 Configuración de Producción

### Backend (config.py)
```python
# Para producción, considera:
CORS_ORIGINS = [
    "https://tu-frontend.vercel.app",
    "http://localhost:5173",  # Para desarrollo
]
```

### Frontend
Actualiza las URLs de la API según tu despliegue.

---

## 📝 Notas

- **Demucs** es pesado y puede no funcionar bien en servicios gratuitos con CPU limitada
- Considera usar servicios con GPU para mejor rendimiento
- Para producción seria, considera AWS/GCP con instancias optimizadas
