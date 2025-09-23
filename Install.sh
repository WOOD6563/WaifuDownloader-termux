#!/bin/bash
set -e

echo "[*] Updating Termux packages..."
apt update -y && apt upgrade -y

echo "[*] Installing required packages..."
pkg install -y python git ninja pkg-config gtk3 libxml2-utils gettext

echo "[*] Installing Python GTK3 bindings..."
pip install --upgrade pip
pip install PyGObject meson

mkdir -p ~/projects
cd ~/projects

echo "[*] Cloning WaifuDownloader repository..."
if [ ! -d "WaifuDownloader" ]; then
    git clone https://github.com/WOOD6563/WaifuDownloader
fi
cd WaifuDownloader

echo "[*] Setting up build directory with Meson..."
meson setup builddir --prefix=$HOME/.local || echo "[!] Build directory already exists, continuing..."

echo "[*] Compiling the project..."
meson compile -C builddir

echo "[*] Installing the project locally..."
meson install -C builddir

if [ -f "$HOME/.local/bin/applications/waifudownloader" ]; then
    mv "$HOME/.local/bin/waifudownloader" "$PREFIX/bin/" || echo "[!] Could not move binary, check permissions."
fi

echo "[*] Setup complete!"
echo "To run WaifuDownloader, execute:"
echo "  termux-x11"
echo "  export DISPLAY=:0"
echo "  waifudownloader"
