
# [scoop]

```pwsh
scoop export > .\workspace\workspace.scoop.json
scoop import .\workspace\workspace.scoop.json
```

## choose dir (admin)

可选 修改 scoop 目录

```
$env:SCOOP='D:\develop\scoop'
$env:SCOOP_GLOBAL='D:\develop\scoop\GlobalScoopApps'
$env:SCOOP='C:\develop\Scoop'
$env:SCOOP_GLOBAL='C:\develop\Scoop\GlobalScoopApps'
[Environment]::SetEnvironmentVariable('SCOOP', $env:SCOOP, 'User')
[Environment]::SetEnvironmentVariable('SCOOP_GLOBAL', $env:SCOOP_GLOBAL, 'Machine')
mkdir $env:SCOOP_GLOBAL
```

## install scoop

安装 scoop

```
# (maybe) Set-ExecutionPolicy RemoteSigned -scope CurrentUser
iwr -useb get.scoop.sh | iex
# (or) Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh')
```

配置代理

```
scoop config proxy localhost:7898

# git and 7z
scoop install git
# set proxy for git
git config --global http.proxy 'socks5://localhost:7898'
git config --global https.proxy 'socks5://localhost:7898'
```

配置应用库

```
scoop bucket add extras
scoop bucket add java
scoop bucket add versions
scoop bucket add nerd-fonts
scoop bucket add nonportable
scoop bucket add dorado https://github.com/chawyehsu/dorado
```

## configuration environment

tools 基础必备的工具（或是被依赖的工具）

```
scoop checkup

# main/
scoop install lessmsi innounp dark nssm # dark 即 WiX Toolset 均是解析安装文件、管理服务的工具
scoop install sudo gsudo curl
```

develop environment 开发环境和游戏环境

```
# main/
scoop install gcc mingw cmake ninja rustup-msvc python go nodejs pnpm # 由 rustup 管理 rust & cargo
# java/
scoop install openjdk17 # openjdk8-redhat
# versions/
# scoop install python27

# dotnet
# scoop install main/dotnet-sdk
# scoop install dorado/dotnet-desktop-runtime

# game
# extras/
sudo scoop install vcredist2005 vcredist2008 vcredist2010 vcredist2012 vcredist2013 vcredist2022
```

## install app

系统体验增强

or just use 'export/import'

```
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
scoop install sing-box v2ray xray
# extras/
scoop install clash-nyanpasu clash-verge-rev v2rayn telegram discord # or https://discord.com/app

# book picture
# extras/
scoop install neeview # sumatrapdf
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
sudo scoop install -g SarasaGothic-SC UbuntuMono-NF-Propo # 优雅中文字体和中文等宽字体
```

常用的软件

```
# start_with_os
# extras/
scoop install everything # translucenttb eartrumpet quicklook
# dorado/
scoop install snipaste-beta # trafficmonitor

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

```
# extras/
# 绘图 矢量 位图
scoop install inkscape krita pixelorama
# pixelorama 是使用 Godot 制作的免费开源 2D 精灵编辑器
# libresprite 是 Aseprite 的免费开源分支
# 视频音频
scoop install shotcut audacity
# 3D建模
scoop install blender
# 2D动画
scoop install opentoonz # enve找不到
# 游戏引擎
scoop install godot
```

## hold version

```
scoop hold nodejs pnpm
# scoop hold gcc mingw rustup-msvc go # dotnet-sdk dotnet-desktop-runtime
scoop hold vcredist2005 vcredist2008 vcredist2010 vcredist2012 vcredist2013 vcredist2022
# scoop hold lav-filters-megamix-np madvr
sudo scoop hold -g SarasaGothic-SC UbuntuMono-NF-Propo
```

## check and restart

```
scoop checkup
scoop status
```

```
shutdown -r -t 0
```
