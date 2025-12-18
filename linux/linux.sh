#!/bin/bash

echo "Cleaning previous build artifacts..."

sanitize_path() {
    echo "$1" | sed 's|\.\./||g'
}

SCRIPT_DIR="$(cd -- "$(dirname "$0")" && pwd)"

DIST_PATH=$SCRIPT_DIR/../dist
BUILD_PATH=$SCRIPT_DIR/../build
SPEC_PATH=$SCRIPT_DIR/../main.spec
ASSETS_PATH=$SCRIPT_DIR/../assets
GAME_PATH=$SCRIPT_DIR/../game
RUN_SCRIPT="$SCRIPT_DIR/../run.sh"

rm -rf "$DIST_PATH/FlappyGame" "$BUILD_PATH" "$SPEC_PATH" "$RUN_SCRIPT"

echo "Building the compiled game...."

python -m PyInstaller --onefile --windowed --name "FlappyGame" --add-data "$ASSETS_PATH:assets" \
 --add-data "$GAME_PATH:game" game/main.py

# shellcheck disable=SC2181
if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
else
  echo "Build succeeded!"
  echo "Allowing execution permissions for the compiled game..."
  chmod +x $DIST_PATH/FlappyGame

  echo "Creating run.sh helper script..."
  cat > "$RUN_SCRIPT" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd -- "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/dist/FlappyGame"
EOF
  chmod +x "$RUN_SCRIPT"
  
  echo "Done!"
  echo "You can run the game with: ./run.sh"
fi

# shellcheck disable=SC2162
read -p "Press Enter to continue..."