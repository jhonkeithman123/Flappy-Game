@echo off
echo Cleaning previous build rtifacts...

rem Remove the dist folder if it exists
if exist "dist" (
    rd /s /q "dist"
)

rem Remove build folder if it exists
if exist "build" (
    rd /s /q "build"
)

rem Remove the spec files if it exists
if exist "main.spec" (
    del /f /q "main.spec"
)

echo Building the executable...

pyinstaller --onefile --windowed --add-data "assets;assets" --add-data "saves;saves" main.py

if %ERRORLEVEL% neq 0 (
    echo Build failed!
    pause
    exit \b %ERRORLEVEL%
) else (
    echo Build succeeded!
)

pause