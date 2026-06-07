@echo off
echo ============================================
echo   BUILD PRODUCCION - botstake.shop
echo ============================================
echo.
echo Este .exe usara el dominio permanente botstake.shop
echo (token Cloudflare built-in ofuscado)
echo.
echo Si quieres build de PRUEBA (tunel temporal), usa:
echo   python scripts/build_exe.py
echo.
set USE_RANDOM_TUNNEL=false
python scripts/build_exe.py
echo.
echo Build completado. .exe en scripts\dist\
pause
