@echo off
echo Cleaning previous build artifacts...

REM Set up paths
set SCRIPT_DIR=%~dp0
set DIST_PATH=%SCRIPT_DIR%..\dist
set BUILD_PATH=%SCRIPT_DIR%..\build
set SPEC_PATH=%SCRIPT_DIR%..\main.spec
set ASSETS_PATH=%SCRIPT_DIR%..\assets
set GAME_PATH=%SCRIPT_DIR%..\game

REM Remove old build artifacts
del /f /q "%DIST_PATH%\FlappyGame.exe"
rmdir /s /q "%BUILD_PATH%"
del /f /q "%SPEC_PATH%"

echo Building the compiled game...

REM Run PyInstaller to build the .exe
pyinstaller --onefile --windowed --name "FlappyGame.exe" ^
  --add-data "%ASSETS_PATH%;assets" ^
  --add-data "%GAME_PATH%;game" "%GAME_PATH%\main.py"

REM Check for build success
if %errorlevel% neq 0 (
    echo Build failed!
    exit /b 1
) else (
    echo Build succeeded!
    echo Done! You can find the compiled game in the 'dist' directory.
)

pause