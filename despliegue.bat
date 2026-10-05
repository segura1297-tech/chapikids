@echo off
REM Script de despliegue para producción
REM Uso: despliegue.bat

echo ========================================
echo  DESPLIEGUE DE CHAPMKIDS PIÑATAS
echo ========================================

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Instalar dependencias
echo.
echo [1/4] Instalando dependencias...
pip install -r requirements.txt

REM Recolectar archivos estáticos
echo.
echo [2/4] Recolectando archivos estáticos...
python manage.py collectstatic --noinput

REM Ejecutar migraciones
echo.
echo [3/4] Ejecutando migraciones...
python manage.py migrate

REM Crear superusuario si no existe
echo.
echo [4/4] Verificando superusuario...
python manage.py createsuperuser --noinput --username admin --email admin@chapikids.com || echo Superusuario ya existe

echo.
echo ========================================
echo  DESPLIEGUE COMPLETADO
echo ========================================
echo.
echo Para iniciar el servidor:
echo   python manage.py runserver
echo.
pause
