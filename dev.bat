@echo off
chcp 65001 >nul 2>&1
title Roulette Sniper Pro - Dev Mode

echo.
echo  =========================================================
echo   🎰 ROULETTE SNIPER PRO - Modo Desarrollo 🎰
echo  =========================================================
echo.

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

:: Check Node.js
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo  ❌ Node.js no esta instalado.
    pause
    exit /b 1
)

:: Step 1: Install deps if needed
if not exist "%PROJECT_DIR%frontend\node_modules" (
    echo  📦 Instalando dependencias React...
    cd /d "%PROJECT_DIR%frontend"
    call npm install
)

:: Step 2: Start Flask in background
echo  [1/2] 🐍 Iniciando Flask (puerto 5050)...
start /b "Flask Dashboard" python -m backend.dashboard.app

:: Wait for Flask to start
timeout /t 3 /nobreak >nul

:: Step 3: Start Vite dev server
echo  [2/2] ⚡ Iniciando Vite dev server (puerto 5173)...
echo.
echo  =========================================================
echo   Dashboard Dev:    http://localhost:5173
echo   Flask API:        http://127.0.0.1:5050
echo   Dashboard Prod:   http://127.0.0.1:5050
echo  =========================================================
echo.
echo  Presiona Ctrl+C para cerrar Vite. Cierra Flask manualmente.
echo.

cd /d "%PROJECT_DIR%frontend"
call npm run dev