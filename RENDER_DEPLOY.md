# 🚀 Despliegue en Render

## Paso 1: Preparar el Repositorio

El repositorio ya está listo con `render.yaml` configurado.

## Paso 2: Crear Cuenta en Render

1. Ve a [render.com](https://render.com)
2. Regístrate con tu cuenta de GitHub

## Paso 3: Desplegar desde GitHub

### Opción A: Blueprint (Automático - Recomendado)

1. En Render Dashboard, haz clic en **"New +"** → **"Blueprint"**
2. Conecta tu repositorio: `altovisual/youtube-steams`
3. Render detectará automáticamente el `render.yaml`
4. Haz clic en **"Apply"**
5. Render creará automáticamente:
   - Backend: `youtube-steams-backend`
   - Frontend: `youtube-steams-frontend`

### Opción B: Manual

#### Backend:
1. New + → Web Service
2. Conecta el repo `altovisual/youtube-steams`
3. Configuración:
   - **Name**: `youtube-steams-backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt && pip install demucs`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
4. Click "Create Web Service"

#### Frontend:
1. New + → Web Service
2. Conecta el repo `altovisual/youtube-steams`
3. Configuración:
   - **Name**: `youtube-steams-frontend`
   - **Runtime**: Node
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm run preview`
   - **Plan**: Free
4. Variables de entorno:
   - `VITE_API_URL`: `https://youtube-steams-backend.onrender.com`
5. Click "Create Web Service"

## Paso 4: Configurar CORS en el Backend

Una vez desplegado el frontend, copia su URL (ej: `https://youtube-steams-frontend.onrender.com`)

Actualiza `backend/config.py`:
```python
CORS_ORIGINS = [
    "https://youtube-steams-frontend.onrender.com",
    "http://localhost:5173",
]
```

Haz commit y push para actualizar.

## Paso 5: Acceder a tu Aplicación

- **Frontend**: `https://youtube-steams-frontend.onrender.com`
- **Backend API**: `https://youtube-steams-backend.onrender.com`

## ⚠️ Notas Importantes

### Plan Free de Render:
- ✅ 750 horas/mes gratis
- ⚠️ Los servicios se duermen después de 15 minutos de inactividad
- ⚠️ Primera petición después de dormir tarda ~30 segundos

### Demucs:
- La primera vez que uses separación de stems, descargará los modelos (~500MB)
- Esto puede tardar 5-10 minutos en el plan free
- Los modelos se mantienen mientras el servicio esté activo

### Rendimiento:
- El plan free tiene CPU limitada
- La separación de stems puede tardar 3-5 minutos por canción
- Para mejor rendimiento, considera el plan Starter ($7/mes)

## 🔧 Troubleshooting

### Error: "Service Unavailable"
- El servicio está iniciando o dormido
- Espera 30 segundos y recarga

### Error: "CORS"
- Verifica que la URL del frontend esté en `CORS_ORIGINS` del backend
- Asegúrate de hacer commit y push después de cambiar

### Separación de stems muy lenta
- Es normal en el plan free
- Considera actualizar al plan Starter para mejor CPU

## 📊 Monitoreo

En el Dashboard de Render puedes ver:
- Logs en tiempo real
- Uso de recursos
- Métricas de rendimiento
- Estado del servicio

## 🔄 Actualizaciones

Render se actualiza automáticamente cuando haces push a GitHub:
1. Haz cambios en tu código local
2. `git add .`
3. `git commit -m "descripción"`
4. `git push`
5. Render detectará los cambios y redesplegará automáticamente
