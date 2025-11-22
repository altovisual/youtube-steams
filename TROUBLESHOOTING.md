# 🔧 Solución de Problemas

## ❌ Errores Comunes y Soluciones

### 1. **"FFmpeg not found" o "FFmpeg no encontrado"**

**Problema**: FFmpeg no está instalado o no está en el PATH.

**Solución**:
```bash
# Opción A: Instalar con Chocolatey
choco install ffmpeg

# Opción B: Descargar manualmente
# 1. Ve a https://ffmpeg.org/download.html
# 2. Descarga la versión para Windows
# 3. Extrae el ZIP
# 4. Agrega la carpeta bin al PATH de Windows
```

**Verificar instalación**:
```bash
ffmpeg -version
```

### 2. **"Python not found"**

**Problema**: Python no está instalado o no está en el PATH.

**Solución**:
1. Descarga Python 3.9+ desde https://python.org
2. Durante la instalación, marca "Add Python to PATH"
3. Reinicia tu terminal

**Verificar instalación**:
```bash
python --version
```

### 3. **"npm not found" o "Node not found"**

**Problema**: Node.js no está instalado.

**Solución**:
1. Descarga Node.js LTS desde https://nodejs.org
2. Instala con opciones por defecto
3. Reinicia tu terminal

**Verificar instalación**:
```bash
node --version
npm --version
```

### 4. **Error al instalar dependencias de Python**

**Problema**: Falla `pip install -r requirements.txt`

**Soluciones**:

**A. Actualizar pip**:
```bash
python -m pip install --upgrade pip
```

**B. Instalar PyTorch manualmente (versión CPU)**:
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**C. Instalar dependencias una por una**:
```bash
pip install fastapi
pip install uvicorn[standard]
pip install yt-dlp
pip install demucs
```

### 5. **Puerto 8000 o 5173 ya en uso**

**Problema**: Otro programa está usando el puerto.

**Solución A - Cerrar el programa**:
```bash
# Ver qué está usando el puerto 8000
netstat -ano | findstr :8000

# Matar el proceso (reemplaza PID con el número que aparece)
taskkill /PID <PID> /F
```

**Solución B - Cambiar puerto**:

En `backend/main.py` (última línea):
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Cambiar a 8001
```

En `frontend/vite.config.js`:
```javascript
server: {
  port: 5174,  // Cambiar a 5174
}
```

### 6. **Error CORS / No se puede conectar al backend**

**Problema**: Frontend no puede comunicarse con backend.

**Solución**:
1. Verifica que el backend esté corriendo en http://localhost:8000
2. Verifica que el frontend esté corriendo en http://localhost:5173
3. Revisa la consola del navegador (F12) para ver errores
4. Asegúrate de que ambos servidores estén corriendo

### 7. **"Error fetching video info" al pegar URL**

**Problema**: No se puede obtener información del video.

**Causas posibles**:
- URL inválida
- Video privado o eliminado
- Restricciones geográficas
- yt-dlp desactualizado

**Soluciones**:
```bash
# Actualizar yt-dlp
pip install --upgrade yt-dlp

# Probar URL directamente
yt-dlp --get-title "URL_DEL_VIDEO"
```

### 8. **Separación de stems muy lenta**

**Problema**: Tarda mucho en separar stems.

**Causas**:
- CPU lento (normal)
- No hay GPU disponible
- Canción muy larga

**Soluciones**:
- **Usar GPU**: Instala PyTorch con CUDA si tienes GPU NVIDIA
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

- **Esperar pacientemente**: Es normal que tome 2-5 minutos por canción
- **Canciones más cortas**: Prueba con canciones de menos de 4 minutos

### 9. **Error al descargar stems**

**Problema**: Los botones de stems no funcionan.

**Solución**:
1. Verifica que la separación haya terminado
2. Revisa la carpeta `backend/stems/htdemucs/`
3. Verifica que los archivos .mp3 existan
4. Revisa la consola del backend para errores

### 10. **Interfaz se ve mal / sin estilos**

**Problema**: TailwindCSS no está funcionando.

**Solución**:
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### 11. **"Module not found" en Python**

**Problema**: Falta alguna dependencia.

**Solución**:
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### 12. **Demucs falla con error de memoria**

**Problema**: No hay suficiente RAM.

**Soluciones**:
- Cierra otros programas
- Usa canciones más cortas
- Reduce la calidad en `config.py`:
```python
DEMUCS_MODEL = "htdemucs_ft"  # Modelo más ligero
```

## 🐛 Debugging

### Ver logs del backend
El backend muestra logs en la terminal donde lo ejecutaste.

### Ver logs del frontend
1. Abre el navegador
2. Presiona F12
3. Ve a la pestaña "Console"

### Verificar archivos descargados
```bash
# Ver archivos de audio
dir backend\downloads

# Ver stems
dir backend\stems\htdemucs
```

## 📞 Obtener Ayuda

Si ninguna solución funciona:

1. **Revisa los logs** en ambas terminales (backend y frontend)
2. **Copia el error completo**
3. **Verifica versiones**:
```bash
python --version
node --version
npm --version
ffmpeg -version
```

## ✅ Checklist de Verificación

Antes de reportar un problema, verifica:

- [ ] Python 3.9+ instalado
- [ ] Node.js 18+ instalado
- [ ] FFmpeg instalado y en PATH
- [ ] Dependencias de Python instaladas
- [ ] Dependencias de Node instaladas
- [ ] Backend corriendo en puerto 8000
- [ ] Frontend corriendo en puerto 5173
- [ ] Sin errores en las terminales
- [ ] Navegador actualizado
- [ ] URL de YouTube válida

## 🔄 Reinstalación Completa

Si todo falla, reinstala desde cero:

```bash
# 1. Eliminar entornos virtuales y node_modules
rmdir /s backend\venv
rmdir /s frontend\node_modules

# 2. Ejecutar instalador
install.bat

# 3. Iniciar aplicación
start.bat
```

## 💡 Tips de Rendimiento

### Para descargas más rápidas:
- Usa conexión por cable en vez de WiFi
- Cierra otros programas que usen internet

### Para separación de stems más rápida:
- Usa GPU si está disponible
- Cierra otros programas
- Procesa canciones de una en una

### Para mejor experiencia:
- Usa Chrome o Edge (mejor rendimiento)
- Mantén las ventanas de terminal abiertas
- No cierres el navegador mientras procesa

---

¿Aún tienes problemas? Revisa los archivos README.md y DEMO.md para más información.
