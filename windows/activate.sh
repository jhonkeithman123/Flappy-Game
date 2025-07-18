#!/bin/bash

SCRIPT_DIR="$(cd -- "$(dirname "$0")" && pwd)"
BUILD_PATH=$(realpath "$SCRIPT_DIR/../windows")

pyinstaller --onefile --windowed --name "FlappyGame.exe" --add-data "$ASSETS_PATH:assets" --add-data "$GAME_PATH:game" "$GAME_PATH/main.py"

