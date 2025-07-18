#!/bin/bash

echo "Cleaning previous build artifacts..."

SCRIPT_DIR="$(cd -- "$(dirname "$0")" && pwd)"

DIST_PATH=$SCRIPT_DIR/../dist
BUILD_PATH=$SCRIPT_DIR/../build
SPEC_PATH=$SCRIPT_DIR/../main.spec
ASSETS_PATH=$SCRIPT_DIR/../assets
GAME_PATH=$SCRIPT_DIR/../game

rm -rf "$DIST_PATH/FlappyGame.exe" "$BUILD_PATH" "$SPEC_PATH"

echo "Building the compiled game...."

python -m PyInstaller --onefile --windowed --name "FlappyGame.exe" --add-data "$ASSETS_PATH:assets" \
 --add-data "$GAME_PATH:game" $GAME_PATH/main.py

if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
else
  echo "Build succeeded!"
  echo "Done! You can find the compiled game in the 'dist' directory."
fi

read -p "Press Enter to continue..."
