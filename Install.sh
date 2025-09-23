#!/bin/bash
# Termux GTK3/Python + WaifuDownloader Setup Script

set -e  # Exit immediately if a command fails

echo "Updating Termux packages..."
apt update -y && pkg upgrade -y

echo "Installing required packages..."
apt install python git  ninja pkg-config gtk3 libxml2-utils gettext 


echo "Installing Python GTK3 bindings..."
pip install PyGObject
pip install meson

# Create a projects directory if it doesn't exist
mkdir -p ~/projects
cd ~/projects

echo "Cloning WaifuDownloader repository..."
git clone https://github.com/WOOD6563/WaifuDownloader
cd WaifuDownloader

echo "Setting up build directory with Meson..."
meson setup builddir --prefix=$HOME/.local

echo "Compiling the project..."
meson compile -C builddir

echo "Installing the project locally..."
meson install -C builddir

mv ~/.local/bin/waifudownloader /data/data/com.termux/files/usr/bin

echo "type 

termux-x11 && export DISPLAY=:0 
waifudownloader""
