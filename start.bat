@echo off
chcp 65001 >nul 2>&1
title Roulette Sniper Pro - Launcher

:: Fix PATH for Node.js and Python (winget installations)
set "PATH=C:\Program Files\nodejs;%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python313;%PATH%"

echo.
echo  =========================================================
echo    ROULETTE SNIPER PRO - Launcher
echo  =========================================================
echo.

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

:: Check Node.js
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo  Node.js no encontrado en el PATH.
    echo  Instala con: winget install OpenJS.NodeJS.LTS
    echo  Luego reinicia la terminal.
    pause
    exit /b 1
)

:: Check Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo  Python no encontrado en el PATH.
    echo  Instala con: winget install python
    pause
    exit /b 1
)

echo.
echo  Node.js:  OK
echo  Python:   OK
echo.

:: Step 1: Build React dashboard (if node_modules exists)
echo  [1/3] Compilando dashboard React...
cd /d "%PROJECT_DIR%react-dashboard"

if not exist "node_modules" (
    echo         Instalando dependencias npm...
    call npm install
)

call npm run build
if %ERRORLEVEL% neq 0 (
    echo  Error compilando React. Revise los logs arriba.
    pause
    exit /b 1
)

:: Step 2: Copy build to Flask static
echo  [2/3] Copiando build a Flask...
if not exist "%PROJECT_DIR%bot_ruleta\dashboard\static\assets" mkdir "%PROJECT_DIR%bot_ruleta\dashboard\static\assets"
copy /Y "%PROJECT_DIR%react-dashboard\dist\index.html" "%PROJECT_DIR%bot_ruleta\dashboard\static\index.html" >nul
copy /Y "%PROJECT_DIR%react-dashboard\dist\assets\*" "%PROJECT_DIR%bot_ruleta\dashboard\static\assets\" >nul

:: Step 3: Start bot launcher (includes Flask dashboard)
echo  [3/3] Iniciando bot...
echo.
echo  =========================================================
echo    Dashboard React:   http://127.0.0.1:5050
echo  =========================================================
echo.

cd /d "%PROJECT_DIR%"
python -u bot_ruleta\launcher.py

pause