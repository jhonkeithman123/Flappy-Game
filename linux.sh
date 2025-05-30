#!/bin/bash

echo "Cleaning previous build artifacts..."

if [ -d "dist" ]; then
    rm -rf "dist"
fi

if [ -d "build" ]; then
    rm -rf "build"
fi

if [ -f "main.spec" ]; then
    rm -rf "main.spec"
fi

echo "Building the compiled game...."

pyinstaller --onefile --windowed --name "FlappyGame" --add-data "assets:assets" main.py

# shellcheck disable=SC2181
if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
else
  echo "Build succeeded!"
fi

# shellcheck disable=SC2162
read -p "Press Enter to continue..."