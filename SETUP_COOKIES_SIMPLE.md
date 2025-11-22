# 🍪 Configuración Simple de Cookies (5 minutos)

## Para que la app funcione para TODOS los usuarios

Necesitas exportar TUS cookies de YouTube una sola vez y subirlas al servidor.

---

## 📋 Pasos:

### 1. Instala la Extensión de Chrome

Ve a: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc

O busca "Get cookies.txt LOCALLY" en Chrome Web Store

### 2. Exporta las Cookies

1. Abre Chrome y ve a [youtube.com](https://youtube.com)
2. **Inicia sesión** con tu cuenta de YouTube/Google
3. Haz clic en el ícono de la extensión (arriba a la derecha)
4. Haz clic en **"Export"**
5. Se descargará un archivo llamado `youtube.com_cookies.txt`

### 3. Reemplaza el Archivo

1. Renombra el archivo descargado a `cookies.txt`
2. Cópialo a la carpeta `backend` de tu proyecto:
   ```powershell
   copy C:\Users\TU_USUARIO\Downloads\youtube.com_cookies.txt C:\Users\altov\Downloads\youtube-descarga\backend\cookies.txt
   ```

### 4. Sube los Cambios

```powershell
cd C:\Users\altov\Downloads\youtube-descarga
git add backend/cookies.txt
git commit -m "Add YouTube cookies for all users"
git push
```

### 5. Espera el Redespliegue

Render redesplegará automáticamente en 3-5 minutos.

---

## ✅ ¡Listo!

Ahora **TODOS** los usuarios podrán usar la app sin problemas.

Las cookies funcionarán para todos porque el servidor las usa en segundo plano.

---

## 🔄 Mantenimiento

Las cookies de YouTube expiran después de **1-2 meses**.

Cuando dejen de funcionar:
1. Repite los pasos 2-4
2. Las cookies se actualizarán automáticamente

---

## 🔒 Seguridad

**¿Es seguro?**
- ✅ Las cookies solo permiten descargar videos públicos
- ✅ No dan acceso a tu cuenta
- ✅ No permiten hacer compras ni cambios
- ⚠️ Mantén el repositorio privado si usas cookies

**Recomendación**: Usa una cuenta de Google secundaria solo para esto.

---

## 🎯 Alternativa Sin Cookies

Si no quieres usar cookies, la única alternativa es:
- Migrar a un VPS con IP diferente
- Usar un servicio de proxy/VPN
- Esperar a que YouTube relaje las restricciones

Pero las cookies son la solución más simple y confiable. 🚀
