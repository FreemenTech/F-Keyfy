#!/usr/bin/env bash
# ============================================
#  F-Keyfy — Linux / macOS Build Script
#  Run from the project root:  ./build.sh
# ============================================

set -e  # stop on first error

echo ""
echo "  === F-Keyfy Build ==="
echo ""

# 1. Create virtual environment
if [ ! -d "venv" ]; then
    echo "[1/4] Creating virtual environment..."
    python3 -m venv venv
else
    echo "[1/4] Virtual environment already exists."
fi

# 2. Activate and install dependencies
echo "[2/4] Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
pip install pyinstaller -q

# 3. Build
echo "[3/4] Building executable..."
pyinstaller F-Keyfy.spec --noconfirm

# 4. Make executable (Linux)
chmod +x dist/F-Keyfy/F-Keyfy 2>/dev/null || true

# 5. macOS: create .app bundle if on Darwin
if [ "$(uname)" = "Darwin" ]; then
    echo "[+] macOS detected — creating .app bundle..."

    APP_DIR="dist/F-Keyfy.app/Contents"
    mkdir -p "$APP_DIR/MacOS"
    mkdir -p "$APP_DIR/Resources"

    # Copy the built binary and data into the .app
    cp -R dist/F-Keyfy/* "$APP_DIR/MacOS/"

    # Create Info.plist
    cat > "$APP_DIR/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>F-Keyfy</string>
    <key>CFBundleDisplayName</key>
    <string>F-Keyfy</string>
    <key>CFBundleIdentifier</key>
    <string>com.freementech.f-keyfy</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleExecutable</key>
    <string>F-Keyfy</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
PLIST

    echo "  .app bundle created at: dist/F-Keyfy.app"
fi

echo ""
echo "[4/4] Build complete!"
echo ""

if [ "$(uname)" = "Darwin" ]; then
    echo "  macOS:  dist/F-Keyfy.app  (drag to Applications)"
    echo "          or run: dist/F-Keyfy/F-Keyfy"
else
    echo "  Linux:  dist/F-Keyfy/F-Keyfy"
    echo "          To distribute: tar czf F-Keyfy-linux.tar.gz -C dist F-Keyfy"
fi
echo ""
