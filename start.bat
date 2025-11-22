@echo off
echo ========================================
echo  YouTube Music Downloader
echo ========================================
echo.

echo Iniciando Backend...
start cmd /k "cd backend && venv\Scripts\activate && python main.py"

timeout /t 3 /nobreak > nul

echo Iniciando Frontend...
start cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo  Aplicacion iniciada!
echo  Backend: http://localhost:8000
echo  Frontend: http://localhost:5173
echo ========================================
