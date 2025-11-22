# ⚡ Inicio Rápido - 5 Minutos

## 🎯 Lo que necesitas

✅ Windows 10/11
✅ 5 minutos de tu tiempo
✅ Conexión a internet

## 🚀 3 Pasos para Empezar

### **Paso 1: Instalar FFmpeg** (2 minutos)

Abre PowerShell como administrador y ejecuta:

```powershell
# Si tienes Chocolatey
choco install ffmpeg

# Si no tienes Chocolatey, instálalo primero:
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Luego instala FFmpeg
choco install ffmpeg
```

### **Paso 2: Instalar Dependencias** (2 minutos)

Haz doble clic en:
```
📄 install.bat
```

Espera a que termine (instalará Python y Node.js dependencies).

### **Paso 3: Iniciar la App** (1 minuto)

Haz doble clic en:
```
🚀 start.bat
```

Se abrirán 2 ventanas de terminal. Espera 10 segundos y abre tu navegador en:
```
http://localhost:5173
```

## 🎵 ¡Listo! Ahora puedes:

1. **Pegar un link de YouTube**
2. **Ver la info y el cover de la canción**
3. **Descargar el audio en MP3**
4. **Separar los stems (vocals, drums, bass, other)**

## 📝 Ejemplo Rápido

```
1. Copia este link: https://www.youtube.com/watch?v=dQw4w9WgXcQ
2. Pégalo en el input de la app
3. Haz clic en el botón de búsqueda 🔍
4. Haz clic en "Descargar Audio MP3" 📥
5. ¡Disfruta tu música! 🎵
```

## ❓ ¿Problemas?

### **FFmpeg no se instala**
Descárgalo manualmente desde: https://ffmpeg.org/download.html

### **Python no encontrado**
Descárgalo desde: https://python.org (marca "Add to PATH")

### **Node.js no encontrado**
Descárgalo desde: https://nodejs.org

### **Puertos ocupados**
Cierra otros programas y vuelve a ejecutar `start.bat`

## 📚 Más Información

- **Guía completa**: README.md
- **Solución de problemas**: TROUBLESHOOTING.md
- **Demo y características**: DEMO.md
- **Documentación técnica**: TECHNICAL.md

## 💡 Tips

- La separación de stems toma 2-5 minutos (es normal)
- Usa canciones de menos de 5 minutos para empezar
- Mantén las ventanas de terminal abiertas
- Si algo falla, revisa TROUBLESHOOTING.md

## 🎉 ¡Disfruta!

Ya tienes tu propio descargador de música de YouTube con separación de stems.

**Características**:
- ✅ Descarga en MP3 320kbps
- ✅ Separación de stems con IA
- ✅ Interfaz hermosa y moderna
- ✅ 100% gratis y local
- ✅ Sin publicidad ni límites

---

**Tiempo total**: ~5 minutos
**Dificultad**: Fácil 🟢
**Resultado**: ¡Increíble! 🎵✨
