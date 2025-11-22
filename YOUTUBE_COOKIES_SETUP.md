# 🍪 Configuración de Cookies de YouTube

YouTube ahora requiere cookies para evitar detección de bots. Aquí está cómo configurarlas:

---

## ⚠️ Problema

YouTube bloquea las descargas automatizadas con el error:
```
Sign in to confirm you're not a bot
```

**Solución**: Usar cookies de una sesión autenticada de YouTube.

---

## 🔧 Solución para Render (Producción)

### Opción 1: Cookies de Navegador (Más Fácil - Solo para desarrollo local)

Esta opción NO funciona en Render porque el servidor no tiene navegador instalado.

### Opción 2: Archivo de Cookies (Recomendado para Render)

#### Paso 1: Exportar Cookies de tu Navegador

**Usando Chrome:**
1. Instala la extensión [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
2. Ve a [youtube.com](https://youtube.com) e inicia sesión
3. Click en el ícono de la extensión
4. Click en "Export" para descargar `cookies.txt`

**Usando Firefox:**
1. Instala el addon [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)
2. Ve a [youtube.com](https://youtube.com) e inicia sesión
3. Click en el ícono del addon
4. Guarda el archivo `cookies.txt`

#### Paso 2: Subir Cookies a Render

**Método A: Variable de Entorno (Más Seguro)**

1. Abre tu `cookies.txt`
2. Copia TODO el contenido
3. En Render Dashboard → tu servicio backend → Environment
4. Agrega variable:
   - **Key**: `YOUTUBE_COOKIES`
   - **Value**: Pega el contenido completo del archivo

5. Actualiza el código para leer de la variable de entorno

**Método B: Archivo en el Repositorio (Menos Seguro)**

⚠️ **NO RECOMENDADO** - Las cookies son sensibles

1. Renombra `cookies.txt` a `youtube_cookies.txt`
2. Agrégalo a `.gitignore` si es privado
3. Súbelo al repositorio
4. En Render → Environment Variables:
   - **Key**: `YOUTUBE_COOKIES_FILE`
   - **Value**: `/opt/render/project/src/backend/youtube_cookies.txt`

---

## 🚀 Alternativa: Usar un Proxy/VPN

Si no quieres manejar cookies, puedes usar un servicio proxy:

### Opción: ProxyCrawl / ScraperAPI

Estos servicios manejan la evasión de bots automáticamente:

1. Regístrate en [ScraperAPI](https://www.scraperapi.com/) (plan gratuito disponible)
2. Obtén tu API key
3. Modifica las peticiones de yt-dlp para usar el proxy

---

## 💡 Solución Temporal: Usar API de YouTube

En lugar de yt-dlp, usar la API oficial de YouTube:

### Ventajas:
- ✅ No requiere cookies
- ✅ Más estable
- ✅ Oficial de Google

### Desventajas:
- ❌ Requiere API Key de Google Cloud
- ❌ Tiene cuotas diarias
- ❌ No permite descargas directas (solo metadata)

---

## 🎯 Recomendación Final

**Para Producción en Render:**

1. **Mejor opción**: Exportar cookies y guardarlas como variable de entorno
2. **Renovar cookies**: Cada 1-2 meses (cuando expiren)
3. **Alternativa**: Migrar a un VPS donde puedas instalar un navegador

**Para Desarrollo Local:**

El backend ya está configurado para funcionar sin cookies en local si YouTube lo permite.

---

## 📝 Código Actualizado

El backend ya está preparado para usar cookies. Solo necesitas configurar la variable de entorno:

```bash
# En Render → Environment Variables
YOUTUBE_COOKIES_BROWSER=chrome  # Si tienes Chrome instalado en el servidor (no aplica en Render)
# O
YOUTUBE_COOKIES_FILE=/path/to/cookies.txt  # Ruta al archivo de cookies
```

---

## ⚡ Solución Rápida (5 minutos)

1. Exporta cookies de YouTube usando la extensión
2. En Render → tu backend → Environment
3. Agrega: `YOUTUBE_COOKIES_FILE=/opt/render/project/src/backend/cookies.txt`
4. Sube el archivo `cookies.txt` a tu repositorio en `/backend/cookies.txt`
5. Redespliega

**Nota**: Asegúrate de agregar `cookies.txt` a `.gitignore` si el repo es público.
