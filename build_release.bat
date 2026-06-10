@echo off
echo ============================================
echo   BUILD PRODUCCION - botstake.shop
echo ============================================
echo.
echo Compilando .exe con --production...
python scripts/build_exe.py --production
echo.
echo ============================================
echo   .exe listo en dist\
echo   El cliente usara botstake.shop automaticamente
echo ============================================
pause