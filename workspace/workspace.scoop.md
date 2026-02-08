
# [scoop]

```shell
scoop export > '.\workspace\workspace.scoop.json'
scoop import '.\workspace\workspace.scoop.json'
```

## choose dir (admin)

可选 修改 scoop 目录【一般来说没必要手动修改安装目录】

```shell
$env:SCOOP='D:\develop\scoop'
$env:SCOOP_GLOBAL='D:\develop\scoop\GlobalScoopApps'
#by_default $env:SCOOP='C:\Users\<user>\scoop'
#by_default $env:SCOOP_GLOBAL='C:\ProgramData\scoop'
[Environment]::SetEnvironmentVariable('SCOOP', $env:SCOOP, 'User')
[Environment]::SetEnvironmentVariable('SCOOP_GLOBAL', $env:SCOOP_GLOBAL, 'Machine')
mkdir $env:SCOOP_GLOBAL
```

## install scoop

安装 scoop

```shell
# (maybe) Set-ExecutionPolicy RemoteSigned -scope CurrentUser
iwr -useb get.scoop.sh | iex
# (or) Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh')
```

配置代理（先自行安装 clash-verge-rev ）

```shell
scoop config proxy localhost:7898

# git and 7z
scoop install git
# set proxy for git
git config --global http.proxy 'socks5://localhost:7898'
git config --global https.proxy 'socks5://localhost:7898'
```

配置应用库

```shell
scoop bucket add extras
scoop bucket add java
scoop bucket add versions
scoop bucket add nerd-fonts
scoop bucket add nonportable
scoop bucket add dorado https://github.com/chawyehsu/dorado
```

## configuration environment

tools 基础必备的工具（或是被依赖的工具）

```shell
scoop checkup

# main/
scoop install lessmsi innounp dark nssm # dark 即 WiX Toolset 均是解析安装文件、管理服务的工具
scoop install sudo gsudo curl
```

develop environment 开发环境和游戏环境

```shell
# main/
scoop install gcc mingw msys2 cmake ninja rustup-msvc python uv go nodejs pnpm
# GCC GNU_Compiler_Collection GNU 编译器
# MinGW Minimalist_GNU_for_Windows GNU 的 Windows 移植版
# MSYS2 基于 MinGW-w64 的增强工具集，包含包管理器（pacman）
# Cygwin Unix 环境模拟层（若想直接执行 Linux Shell ，简单场景使用 git-bash 复杂场景使用 WSL2 ）
# CMake 作为构建前端（生成 Makefile 来执行 Make）
# Ninja 作为构建后端
# rustup 管理 rust & cargo
# uv 是一个 python 的包管理工具
# pnpm 是一个 nodejs 的包管理工具

# java/
scoop install openjdk17 # openjdk8-redhat
# versions/
# scoop install python27

# dotnet
# scoop install main/dotnet-sdk
# scoop install dorado/dotnet-desktop-runtime

# game
# extras/
gsudo scoop install vcredist2005 vcredist2008 vcredist2010 vcredist2012 vcredist2013 vcredist2022
```

## install app

系统体验增强

or just use 'export/import'

```shell
# system clean program
# extras/
scoop install dismplusplus driverstoreexplorer geekuninstaller
scoop install freemove wiztree # spacesniffer
scoop install memreduct hasher

# download
# main/
scoop install n-m3u8dl-cli
# extras/
scoop install qbittorrent-enhanced motrix aria-ng-gui neatdownloadmanager # emule

# proxy
# main
scoop install sing-box mihomo v2ray xray
# extras/
scoop install clash-nyanpasu flclash clash-party v2rayn
# clash-nyanpasu 12k stars
# clash-party    19k stars
# flclash        29k stars
# v2rayn         94k stars
scoop install telegram # discord use https://discord.com/app

# book picture
# extras/
scoop install neeview # sumatrapdf
scoop install imageglass exifglass
# imageglass    Star 7K CSharp
# jpegview-fork Star 2k Cpp
# qview         Star 2k Cpp
# picview       Star 1k CSharp 使用体验不是很好 官网说和7z配合能实现压缩包看图 但实际有问题？

# video
# main/
scoop install yt-dlp # ffmpeg youtube-dl
# extras/
scoop install youtube-dl-gui mpv # mpv.net k-lite-codec-pack-full-np vlc
# nonportable
scoop install icaros-np
# potplayer
# scoop install potplayer madvr nonportable/lav-filters-megamix-np

# fonts
# nerd-fonts/
scoop install SarasaGothic-SC Maple-Mono-NF-CN UbuntuMono-NF-Propo # 中文等宽字体，个人安装
```

常用的软件

```shell
# start_with_os
# extras/
scoop install everything wizfile # translucenttb eartrumpet quicklook
# extras/
scoop install snipaste # trafficmonitor

# extras/
scoop install screentogif sharex
scoop install cheat-engine
# dorado/
scoop install steampp

# 串流
scoop install moonlight sunshine
# 录屏直播
scoop install obs-studio
# 按键显示
scoop install keyviz

# Android
# main/
scoop install adb scrcpy
# extras/
scoop install qtscrcpy
```

玩具

```shell
# extras/

# 图像
scoop install inkscape gimp krita
# inkscape 矢量图处理，类似 Illustrator
# gimp     位图处理，类似 Photoshop ，定位图片合成
# krita    位图、矢量图、动画都能做，定位绘画创作
# 像素绘画（也可直接使用 krita 绘制）
# pixelorama 是使用 Godot 制作的免费开源 2D 精灵编辑器
# libresprite 是 Aseprite 的免费开源分支

# 视频音频
scoop install shotcut audacity

# 音频宿主软件 DAW
scoop install lmms
# Ardour 另外一个开源软件 https://ardour.org/ 更偏重于混音和后期
# Reaper 另外一个商用软件 https://www.reaper.fm/ 小巧专业且售价不高（相比于其他的商业 DAW 来说）

# 3D建模
scoop install blender

# 2D动画
# scoop install opentoonz # enve找不到

# 游戏引擎
scoop install godot
```

## hold version

```shell
# scoop hold nodejs pnpm
# scoop hold gcc mingw rustup-msvc go # dotnet-sdk dotnet-desktop-runtime
scoop hold vcredist2005 vcredist2008 vcredist2010 vcredist2012 vcredist2013 vcredist2022
# scoop hold lav-filters-megamix-np madvr
scoop hold SarasaGothic-SC Maple-Mono-NF-CN UbuntuMono-NF-Propo

# if update
scoop unhold vcredist2022
scoop update vcredist2022
scoop hold vcredist2022
# restart

scoop unhold SarasaGothic-SC Maple-Mono-NF-CN UbuntuMono-NF-Propo
scoop update SarasaGothic-SC Maple-Mono-NF-CN UbuntuMono-NF-Propo
scoop hold SarasaGothic-SC Maple-Mono-NF-CN UbuntuMono-NF-Propo
```

## check and restart

```shell
scoop checkup # Check for potential problems
scoop status  # Show status and check for new app versions
```

```shell
shutdown -r -t 0
```

## clear old version and download cache

```shell
scoop cleanup * # Cleanup apps by removing old versions
scoop cache show # Show or clear the download cache
scoop cache rm *
```
