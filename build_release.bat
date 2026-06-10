@echo off
echo ============================================
echo   BUILD PRODUCCION - botstake.shop
echo ============================================
echo.
echo Cambiando DEV_MODE=False en tunnel.py...
powershell -Command "(gc backend\notifier\tunnel.py) -replace 'DEV_MODE = True', 'DEV_MODE = False' | sc backend\notifier\tunnel.py"
echo.
echo Compilando .exe...
python scripts/build_exe.py
echo.
echo Restaurando DEV_MODE=True...
powershell -Command "(gc backend\notifier\tunnel.py) -replace 'DEV_MODE = False', 'DEV_MODE = True' | sc backend\notifier\tunnel.py"
echo.
echo ============================================
echo   .exe listo en scripts\dist\
echo   El cliente usara botstake.shop automaticamente
echo ============================================
pause
