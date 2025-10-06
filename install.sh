#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "Starting WaifuDownloader setup in Termux..."

echo "Updating packages..."
apt update -y && apt upgrade -y
echo "Packages updated!"

echo "Installing required packages..."
pkg install -y python git ninja pkg-config gtk3 libxml2-utils gettext
echo "Packages installed!"

echo "Installing Python GTK3 bindings..."
pip install PyGObject meson
echo "Bindings installed!" 

echo "Cloning WaifuDownloader..."
if [ ! -d "WaifuDownloader" ]; then
    git clone https://github.com/WOOD6563/WaifuDownloader
fi

cd WaifuDownloader

echo "Setting up build directory..."
meson setup builddir --prefix=$HOME/.local || true

echo "Compiling..."
meson compile -C builddir

echo "Installing..."
meson install -C builddir

# Move binary if it exists
if [ -f "$HOME/.local/bin/waifudownloader" ]; then
    mv "$HOME/.local/bin/waifudownloader" "$PREFIX/bin/" || true
fi

# Cleanup
rm -rf WaifuDownloader

echo "Setup complete!"
echo "Run WaifuDownloader with:"
echo "  termux-x11"
echo "  export DISPLAY=:0"
echo "  waifudownloader"