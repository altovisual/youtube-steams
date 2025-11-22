# 📁 Estructura del Proyecto

```
youtube-descarga/
│
├── 📂 backend/                    # Backend Python/FastAPI
│   ├── main.py                    # Servidor principal con API endpoints
│   ├── config.py                  # Configuración centralizada
│   ├── requirements.txt           # Dependencias Python
│   ├── downloads/                 # Archivos de audio descargados (auto-creado)
│   └── stems/                     # Stems separados (auto-creado)
│
├── 📂 frontend/                   # Frontend React/Vite
│   ├── 📂 src/
│   │   ├── 📂 components/
│   │   │   ├── UrlInput.jsx       # Input para URL de YouTube
│   │   │   ├── VideoCard.jsx      # Card con info y acciones
│   │   │   └── 📂 ui/
│   │   │       └── Button.jsx     # Componente de botón reutilizable
│   │   ├── 📂 lib/
│   │   │   └── utils.js           # Utilidades (cn, formatters)
│   │   ├── App.jsx                # Componente principal
│   │   ├── main.jsx               # Entry point
│   │   └── index.css              # Estilos globales con Tailwind
│   │
│   ├── index.html                 # HTML base
│   ├── package.json               # Dependencias Node
│   ├── vite.config.js             # Configuración Vite
│   ├── tailwind.config.js         # Configuración Tailwind
│   ├── postcss.config.js          # Configuración PostCSS
│   └── .eslintrc.cjs              # Configuración ESLint
│
├── 📄 README.md                   # Documentación completa
├── 📄 INSTRUCCIONES.md            # Guía rápida de instalación
├── 📄 ESTRUCTURA.md               # Este archivo
├── 📄 .gitignore                  # Archivos ignorados por Git
├── 🔧 install.bat                 # Script de instalación automática
└── 🚀 start.bat                   # Script para iniciar la app

```

## 🎯 Flujo de Datos

```
Usuario ingresa URL
       ↓
[UrlInput.jsx] → POST /api/video-info
       ↓
[Backend] → yt-dlp extrae metadata
       ↓
[VideoCard.jsx] muestra info + cover
       ↓
Usuario hace clic en "Descargar"
       ↓
[VideoCard.jsx] → POST /api/download
       ↓
[Backend] → yt-dlp descarga audio MP3
       ↓
Usuario hace clic en "Separar Stems"
       ↓
[VideoCard.jsx] → POST /api/separate-stems
       ↓
[Backend] → Demucs separa en 4 stems
       ↓
[VideoCard.jsx] muestra botones de descarga
       ↓
Usuario descarga stems individuales
```

## 🎨 Componentes UI

### **App.jsx**
- Componente raíz
- Maneja estado global de videoInfo
- Layout principal con gradiente

### **UrlInput.jsx**
- Input con búsqueda
- Validación de URL
- Manejo de errores
- Loading state

### **VideoCard.jsx**
- Muestra thumbnail + metadata
- Botones de acción (descargar, separar)
- Lista de stems disponibles
- Estados de loading/success

### **Button.jsx**
- Componente reutilizable
- 3 variantes: primary, secondary, success
- Animaciones hover/disabled

## 🔌 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/video-info` | Obtiene metadata del video |
| POST | `/api/download` | Descarga audio MP3 |
| POST | `/api/separate-stems` | Separa audio en stems |
| GET | `/api/download-file/{id}` | Descarga archivo completo |
| GET | `/api/download-stem/{id}/{name}` | Descarga stem específico |

## 🎨 Paleta de Colores

- **Gradiente Principal**: Azul → Púrpura → Rosa
- **Cards**: Blanco con transparencia (glassmorphism)
- **Botones Primary**: Azul → Púrpura
- **Botones Secondary**: Púrpura → Rosa
- **Success**: Verde → Esmeralda

## 📦 Tecnologías Clave

### Backend
- **FastAPI**: Framework web async
- **yt-dlp**: Descarga de YouTube
- **Demucs**: Separación de stems con IA
- **PyTorch**: Backend de Demucs
- **Uvicorn**: Servidor ASGI

### Frontend
- **React 18**: UI library
- **Vite**: Build tool
- **TailwindCSS**: Utility-first CSS
- **Lucide React**: Iconos
- **Axios**: HTTP client
- **clsx + tailwind-merge**: Utilidades CSS

## 🚀 Scripts Disponibles

### Backend
```bash
python main.py              # Inicia servidor
```

### Frontend
```bash
npm run dev                 # Modo desarrollo
npm run build               # Build producción
npm run preview             # Preview build
```

### Automatizados
```bash
install.bat                 # Instala todo
start.bat                   # Inicia backend + frontend
```

## 📊 Tamaño Aproximado

- **Backend**: ~500 MB (con PyTorch)
- **Frontend**: ~240 paquetes npm
- **Archivos descargados**: Variable (depende del uso)
- **Stems**: ~4x tamaño del audio original

## 🔐 Seguridad

- CORS configurado para localhost
- Sin autenticación (uso local)
- Archivos temporales en carpetas locales
- No se almacenan URLs ni metadata de usuarios

## 🎯 Próximas Mejoras Posibles

- [ ] Historial de descargas
- [ ] Cola de procesamiento
- [ ] Soporte para playlists
- [ ] Conversión a otros formatos
- [ ] Limpieza automática de archivos antiguos
- [ ] Modo oscuro
- [ ] Visualizador de audio
- [ ] Edición básica de stems

---

Estructura creada para máxima claridad y mantenibilidad 🚀
