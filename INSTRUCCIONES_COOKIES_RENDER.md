# 🍪 Configurar Cookies en Render (2 minutos)

GitHub bloqueó el push de cookies por seguridad. Vamos a usar variables de entorno en Render.

---

## 📋 Pasos:

### 1. Abre el archivo de cookies

El archivo está en: `C:\Users\altov\Downloads\youtube-descarga\95f608f8-5ce2-4786-9340-8b5e5eeee403.txt`

### 2. Copia TODO el contenido

1. Abre el archivo con Notepad
2. Presiona `Ctrl + A` (seleccionar todo)
3. Presiona `Ctrl + C` (copiar)

### 3. Ve a Render

1. Abre [render.com](https://render.com)
2. Ve a tu servicio **youtube-steams-backend**
3. Click en **"Environment"** en el menú izquierdo

### 4. Agrega la Variable de Entorno

1. Click en **"Add Environment Variable"**
2. En **Key** escribe: `YOUTUBE_COOKIES`
3. En **Value** pega TODO el contenido del archivo (Ctrl + V)
4. Click en **"Save Changes"**

### 5. Espera el Redespliegue

Render redesplegará automáticamente en 2-3 minutos.

---

## ✅ ¡Listo!

Ahora la app funcionará para TODOS los usuarios sin problemas de bot detection.

---

## 🔄 Mantenimiento

Las cookies expiran en 1-2 meses. Cuando dejen de funcionar:
1. Exporta nuevas cookies
2. Actualiza la variable `YOUTUBE_COOKIES` en Render
3. Guarda los cambios

---

## 🔒 Seguridad

✅ Las cookies están seguras en Render (no en GitHub)
✅ Solo tú tienes acceso a las variables de entorno
✅ Los usuarios no ven las cookies
