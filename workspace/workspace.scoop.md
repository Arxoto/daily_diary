
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
scoop install gcc mingw msys2 cmake ninja rustup-msvc go uv fnm
# GCC GNU_Compiler_Collection GNU 编译器
# MinGW Minimalist_GNU_for_Windows GNU 的 Windows 移植版
# MSYS2 基于 MinGW-w64 的增强工具集，包含包管理器（pacman）
# Cygwin Unix 环境模拟层（若想直接执行 Linux Shell ，简单场景使用 git-bash 复杂场景使用 WSL2 ）
# CMake 作为构建前端（生成 Makefile 来执行 Make）
# Ninja 作为构建后端

# rustup 管理 rust & cargo
# go 自带管理工具（一般也不需要切换）
# uv 是一个 python 的包管理工具，同时一站式支持：虚拟环境创建、依赖安装

# nodejs 管理复杂：
# fnm 用于管理 nodejs 版本，兼容 nvm （不要用 scoop 直接管理 nodejs 会有全局包冲突的问题）
#    P.S.安装后提示配置终端打开时自动执行 `fnm env --use-on-cd | Out-String | Invoke-Expression` 不建议实施，会覆盖 cd 命令，每次 cd 后都会尝试切换 nodejs 版本
#    P.S.每次使用前需要使用 `fnm env` 临时添加环境变量，之后的第一次 `fnm use` 会根据环境变量去生成软连接指向对应的 nodejs 安装目录，再之后的 `fnm use` 仅修改软连接
# Volta 用于管理 nodejs 版本和管理包管理器 (npm/yarn/pnpm) ，但对 pnpm 支持不佳（不支持全局安装和自动迁移），且不兼容 nvm 
#    P.S.相比于 Corepack （官方的包管理器，内置于 nodejs ）， Volta 不依赖 nodejs 版本，他们都是基于 shim 实现的
#        其中 Corepack `corepack enable` 执行后，会在 corepack 同目录下生成 npm/yarn/pnpm 的 shim
#    P.S.相比于 fnm 污染基础命令， Volta 更优雅基于 shim 代理，执行 node 命令实际执行 ~/.volta/bin/node 一个简单的执行文件，自动确定版本和路径并执行真正的 node 命令
#        但是其 shim 实现上存在共享状态的情况（如锁文件防止下载同版本、临时文件进行通信等），极端情况可能会出问题，在快速切换目录时可能因为目录缓存更新不及时导致版本出错
#    P.S.Volta 在 shim 中禁止了 pnpm 的全局安装，因为 pnpm 会直接操作文件系统（软连接等），相反对于 npm/yarn 的全局安装能完全接管，实际安装在 Volta 中
#    P.S.Volta 说的 pnpm 无法自动迁移，指的是老版本中对 pnpm 只是作为一个普通的 npm 包被 Volta 管理，新版需要设置环境变量并手动重新安装
#
# 最佳实践
# - fnm 会污染 cd 命令， volta 对 pnpm 支持不佳，二者都有缺点，综合考虑使用 fnm 手动切换 nodejs 版本、使用 corepack 自动管理包管理器
# - 尽量避免全局安装包；若必须则先 `fnm use {version}` 再安装到 fnm 下的 nodejs 里
# - 每次 fnm 安装新 nodejs 后，执行 `corepack enable` 让其接管包管理器，其 shim 在 fnm 下的 nodejs 中，不会污染外部环境（todo）
#   - 或提前执行 `fnm env --corepack-enabled | Out-String | Invoke-Expression` ，让 fnm 安装后自动执行 `corepack enable`
#   - 若 nodejs 版本较老不支持 corepack 则手动管理，若新版非内置 corepack 则全局安装后手动执行 `corepack enable`
# - 进入项目路径手动执行 `fnm use` 切换对应 nodejs （如果没配置自动执行刷新环境变量则手动刷一下）
#   - 若安装包依赖有问题：尝试 npx 临时指定包管理器的版本，对应的版本会下载到全局统一的缓存目录里
# - 如何识别项目本身使用的管理器
#   - 项目使用 Volta ______ package.json 中有 volta 字段
#   - 项目使用 fnm ________ 根目录有 .nvmrc 或 .node-version 文件
#   - 项目使用 Corepack ___ package.json 中有 packageManager 字段
#   - 项目使用 npm ________ 根目录有 package-lock.json 文件
#   - 项目使用 yarn _______ 根目录有 yarn.lock 文件
#   - 项目使用 pnpm _______ 根目录有 pnpm-lock.yaml 文件

# java/
scoop install openjdk17 # openjdk8-redhat

# game
# extras/
gsudo scoop install vcredist2005 vcredist2008 vcredist2010 vcredist2012 vcredist2013 vcredist2022
```

uv 镜像配置（环境变量）

```powershell
$env:UV_PYTHON_INSTALL_MIRROR = "https://mirror.nju.edu.cn/github-release/astral-sh/python-build-standalone/"
$env:UV_DEFAULT_INDEX = "https://mirrors.ustc.edu.cn/pypi/simple"
```

fnm 镜像配置（环境变量）

```powershell
$env:FNM_NODE_DIST_MIRROR = "https://npmmirror.com/mirrors/node/"
npm config set registry "https://registry.npmmirror.com/"
yarn config set registry "https://registry.npmmirror.com/"
pnpm config set registry "https://registry.npmmirror.com/"
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
