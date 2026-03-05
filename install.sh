#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "Setting up build directory..."
meson setup builddir --prefix=$HOME/build || true

echo "Compiling..."
meson compile -C builddir

echo "Installing..."
meson install -C builddir

echo "Setup complete!"
echo "Run WaifuDownloader with:"
echo "  termux-x11"
echo "  export DISPLAY=:0"
echo "  waifudownloader"
