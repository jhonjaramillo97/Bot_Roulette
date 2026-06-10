@echo off
echo Building React Dashboard...
cd /d "%~dp0"

call npm run build

echo.
echo Copying build to Flask static directory...

set FLASK_STATIC=..\backend\dashboard\static

if not exist "%FLASK_STATIC%\assets" mkdir "%FLASK_STATIC%\assets"

copy /Y "dist\index.html" "%FLASK_STATIC%\index.html"
copy /Y "dist\assets\*" "%FLASK_STATIC%\assets\"

echo.
echo Copying original static assets that need to be preserved...
if not exist "%FLASK_STATIC%\logo.png" echo WARNING: logo.png not found in static dir
if not exist "%FLASK_STATIC%\favicon.ico" echo WARNING: favicon.ico not found in static dir

echo.
echo Done! React dashboard built and deployed to Flask static dir.
echo Original Flask files (logo.png, favicon.ico) are preserved.