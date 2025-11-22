# 🔄 Mantener el Backend Siempre Activo

El plan gratuito de Render duerme los servicios después de 15 minutos de inactividad. Aquí hay varias soluciones para mantenerlo activo:

---

## ✅ Opción 1: UptimeRobot (Recomendado - Gratis)

[UptimeRobot](https://uptimerobot.com/) es un servicio gratuito que hace ping a tu backend cada 5 minutos.

### Pasos:
1. Ve a [uptimerobot.com](https://uptimerobot.com/)
2. Crea una cuenta gratuita
3. Click en "Add New Monitor"
4. Configura:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: YouTube Steams Backend
   - **URL**: `https://youtube-steams-backend.onrender.com/health`
   - **Monitoring Interval**: 5 minutes
5. Click "Create Monitor"

✅ **Ventajas**:
- Completamente gratis
- Hasta 50 monitores
- Notificaciones por email si el servicio cae
- Dashboard con estadísticas

---

## ✅ Opción 2: Cron-Job.org (Gratis)

[Cron-Job.org](https://cron-job.org/) ejecuta tareas programadas gratis.

### Pasos:
1. Ve a [cron-job.org](https://cron-job.org/)
2. Regístrate gratis
3. Click en "Create Cronjob"
4. Configura:
   - **Title**: Keep YouTube Steams Alive
   - **URL**: `https://youtube-steams-backend.onrender.com/health`
   - **Schedule**: Every 5 minutes
5. Guarda

---

## ✅ Opción 3: GitHub Actions (Gratis)

Usa GitHub Actions para hacer ping automáticamente.

### Crear archivo `.github/workflows/keep-alive.yml`:

```yaml
name: Keep Backend Alive

on:
  schedule:
    # Ejecutar cada 5 minutos
    - cron: '*/5 * * * *'
  workflow_dispatch: # Permitir ejecución manual

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Backend
        run: |
          curl -f https://youtube-steams-backend.onrender.com/health || exit 1
      - name: Log Success
        run: echo "Backend is alive!"
```

**Nota**: GitHub Actions tiene límites de minutos mensuales en el plan gratuito (2000 min/mes).

---

## ✅ Opción 4: Koyeb (Gratis - Sin Sleep)

[Koyeb](https://www.koyeb.com/) ofrece hosting gratuito sin sleep.

### Pasos:
1. Migrar el backend a Koyeb
2. Conectar el repositorio de GitHub
3. Koyeb mantiene el servicio activo 24/7 sin dormir

**Ventajas**:
- No se duerme nunca
- 512MB RAM gratis
- Despliegue automático desde GitHub

---

## ✅ Opción 5: Render Paid Plan ($7/mes)

Actualizar a Render Starter Plan:
- Sin sleep automático
- Más CPU y RAM
- Mejor rendimiento para Demucs

---

## 🎯 Recomendación

**Para uso personal**: UptimeRobot (gratis, fácil, confiable)

**Para producción**: Render Paid Plan o Koyeb

---

## 📊 Verificar que Funciona

Después de configurar cualquier opción:

1. Espera 20 minutos sin usar la app
2. Visita: `https://youtube-steams-backend.onrender.com/health`
3. Debería responder inmediatamente (no en 30 segundos)

Si responde rápido, ¡el keep-alive está funcionando! ✅

---

## 🔧 Endpoint de Health Check

El backend ya tiene un endpoint `/health` que responde:

```json
{
  "status": "healthy",
  "timestamp": "2024-11-22T11:42:00",
  "service": "youtube-steams-backend"
}
```

Este endpoint es ligero y no consume recursos significativos.
