#!/bin/bash
APPID="moe.nyarchlinux.waifudownloader"
BUNDLENAME="waifudownloader.flatpak"
flatpak-builder --install --user --force-clean flatpak-app "$APPID".json

if [ "$1" = "bundle" ]; then
	flatpak build-bundle ~/.local/share/flatpak/repo "$BUNDLENAME" "$APPID"
fi