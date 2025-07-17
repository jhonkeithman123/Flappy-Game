#!/bin/bash

echo "Cleaning previous build artifacts..."

sanitize_path() {
    echo "$1" | sed 's|\.\./||g'
}

DIST_PATH=$(realpath dist)
BUILD_PATH=$(realpath build)
SPEC_PATH=$(realpath main.spec)
ASSETS_PATH=$(realpath assets)
GAME_PATH=$(sanitize_path "game")

rm -rf "$DIST_PATH" "$BUILD_PATH" "$SPEC_PATH"

echo "Building the compiled game...."

python -m PyInstaller --onefile --windowed --name "FlappyGame" --add-data "$ASSETS_PATH:assets" \
 --add-data "$GAME_PATH:game" game/main.py

# shellcheck disable=SC2181
if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
else
  echo "Build succeeded!"
fi

# shellcheck disable=SC2162
read -p "Press Enter to continue..."