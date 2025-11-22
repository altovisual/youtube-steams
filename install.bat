@echo off
echo ========================================
echo  Instalando YouTube Music Downloader
echo ========================================
echo.

echo [1/3] Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no esta instalado!
    echo Por favor instala Python 3.9+ desde python.org
    pause
    exit /b 1
)

echo.
echo [2/3] Configurando Backend...
cd backend
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)

echo Activando entorno virtual...
call venv\Scripts\activate

echo Instalando dependencias de Python...
pip install -r requirements.txt

cd ..

echo.
echo [3/3] Configurando Frontend...
cd frontend

echo Instalando dependencias de Node...
call npm install

cd ..

echo.
echo ========================================
echo  Instalacion completada!
echo ========================================
echo.
echo Para iniciar la aplicacion, ejecuta: start.bat
echo.
pause
