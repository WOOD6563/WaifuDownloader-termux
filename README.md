## Location
- [About WaifuDownloader](#waifudownloader-for-native-termux)
- [Features](#features-roadmap)
- [Installation](#installation)
- [Credits](#credits)

---
<br>

## WaifuDownloader for native Termux
A GTK4 application that downloads images of waifu based on https://docs.waifu.im/

A fork of [Nyarch Linux](https://github.com/NyarchLinux)'s [WaifuDownloader](https://github.com/NyarchLinux/WaifuDownloader) project, more specifically for native Termux, no PRoot or Chroot needed.

![waifudownloader-screenshots](https://github.com/NyarchLinux/WaifuDownloader/assets/67018178/b7d7bb3f-c5f1-4b54-9e49-1c6cbd807d31)

## Features roadmap
- [x] Allow NSFW images
- [ ] Any other

<br>

## Installation 
**There are 2 methonds to install it, use one of them**:

### A: Script installation 
1. Run the following commands:
```
apt update
apt install -y wget
```
2. Install the WaifuDownloader script:
```
cd ~
wget https://raw.githubusercontent.com/WOOD6563/WaifuDownloader-termux/refs/heads/master/Install.sh
```
3. Give execute permission to the script and run it:
```
chmod +x install.sh
./install.sh
```
And you are done! Make sure to check the verbose.

### B: Package installation
1. Check **[Releases](https://github.com/WOOD6563/WaifuDownloader-termux/releases)** page and download the latest package there
2. Locate where you downloaded and run the following commands to install:
```
apt update
apt install ./file.deb
```
> [!NOTE]
> Change the `file.deb` into the actual package name including the extension.

<br>

## Credts and their Licenses (if available) <a name=credits></a>
- [WaifuDownloader](https://github.com/NyarchLinux/WaifuDownloader): [GPL-3.0 license](https://github.com/NyarchLinux/WaifuDownloader/blob/master/LICENSE)
- [CatgirlDownloader](https://github.com/NyarchLinux/CatgirlDownloader): [GPL-3.0 license](https://github.com/NyarchLinux/CatgirlDownloader/blob/master/LICENSE)


