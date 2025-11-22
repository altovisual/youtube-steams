@echo off
echo ========================================
echo  Instalando Demucs para separacion de stems
echo ========================================
echo.

cd backend
call venv\Scripts\activate

echo Instalando Demucs...
pip install demucs

echo.
echo ========================================
echo  Instalacion completada!
echo ========================================
echo.
echo Demucs ha sido instalado correctamente.
echo Ahora puedes usar la funcion de separacion de stems.
echo.
pause
