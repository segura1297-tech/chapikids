@echo off
REM Script para commit y push automático
REM Uso: git_commit.bat "mensaje"

if "%~1"=="" (
    set /p msg="Mensaje del commit: "
) else (
    set msg=%~1
)

git add .
git commit -m "%msg%"
git push origin main

echo.
echo Commit y push completados.
echo Railway deployara automaticamente si esta conectado al repo.
pause
