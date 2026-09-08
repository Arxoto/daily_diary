
# [scoop]

```shell
scoop export > '.\workspace\workspace.scoop.json'
scoop import '.\workspace\workspace.scoop.json'
```

## clear old version and download cache

```shell
scoop cleanup * # Cleanup apps by removing old versions
scoop cache show # Show or clear the download cache
scoop cache rm *
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
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
# iwr -useb get.scoop.sh | iex
```

配置代理

```shell
scoop config proxy localhost:7898

# git and 7z
scoop install 7zip git
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

必备工具

```shell
scoop checkup

# main/
scoop install lessmsi innounp dark nssm # dark 即 WiX Toolset 均是解析安装文件、管理服务的工具
scoop install sudo gsudo
```

## configuration environment

develop environment 开发环境和游戏环境

```shell
# main/
scoop install mingw cmake ninja rustup-msvc go uv fnm # gcc msys2
# GCC(GNU_Compiler_Collection) GNU 编译器本体
# MinGW(Minimalist_GNU_for_Windows) 包含 GCC 并附带完整工具链
# MSYS2 给 Windows 提供 Linux 风格的开发工具，以编译出原生 Windows 软件
#   包含以下三个组件
#     MSYS2 子系统，是一个 Cygwin 运行时的分支版本，兼容性更好
#     MinGW-w64 工具链，调用 Windows API 编译出二进制文件
#     pacman 包管理器（移植自 Arch Linux ），统一管理子系统的库和工具
#   环境
#     MSYS 工具链 MSYS 自带的 GCC ，编译产物非原生 Windows 软件，主要为底层实现
#     MINGW64 工具链 MinGW-w64 ，运行时库 msvcrt.dll ，是曾经的主流
#     UCRT64 工具链 MinGW-w64 ，运行时库 ucrtbase.dll ，官方现在首推的默认环境
#     CLANG64 工具链 LLVM/Clang ，运行时库 ucrtbase.dll ，主要提供另一种编译器选择
# Cygwin 是 POSIX 兼容层实现，主要用于运行 Unix 应用，但是简单场景 git-bash ，复杂场景不如直接 WSL2 （原生性能）
# CMake 作为构建前端，为编译工具生成对应的构建脚本（生成 Makefile 来执行 Make ）
# Ninja 作为构建后端，是构建执行器，相比于 Make 性能更好
# 手写 CMakeLists.txt -> cmake 生成 Makefile/build.ninja -> make/ninja 编译（命令行调用 MinGW 编译工具）

# rustup 管理 rust & cargo
# go 自带管理工具（一般也不需要切换）
# uv 是一个 python 的包管理工具，同时一站式支持：虚拟环境创建、依赖安装

# nodejs 管理复杂：
# fnm 用于管理 nodejs 版本，兼容 nvm （不要用 scoop 直接管理 nodejs 会有全局包冲突的问题）
#    原理是在终端会话的 `PATH` 变量前插入一个临时目录，切换 nodejs 版本时在临时目录里创建软连接
#    P.S.安装后提示执行 `fnm env --use-on-cd | Out-String | Invoke-Expression` 以每次 `cd` 自动执行 `fnm use` ，这里不建议实施，会污染 cd 命令
#    P.S.因此建议手动 `fnm env | Out-String | Invoke-Expression; fnm use`
# Volta 用于管理 nodejs 版本和管理包管理器 (npm/yarn/pnpm) ，但对 pnpm 支持不佳（不支持全局安装和自动迁移），且不兼容 nvm
#    原理是基于 shim 代理，执行 node 命令实际执行 ~/.volta/bin/node 一个代理执行文件，里面自动确定版本和路径并执行真正的 node 命令
#    P.S.相比于 fnm 的污染基础命令， Volta 更优雅，但是历史出现过快速切换目录时版本切换出错的情况
#    P.S.Volta 在 shim 中禁止了 pnpm 的全局安装，因为 pnpm 会直接操作文件系统（软连接等），相反对于 npm/yarn 的全局安装能完全接管，实际安装在 Volta 中
# Corepack 是“包管理器的版本管理器”，曾经随着 nodejs 一同分发（但是 pnpm 官方明确表示 v12 版本不兼容 Corepack ）
#    原理也是基于 shim 垫片，去自动执行对应版本的 npm/yarn 命令
#
# 最佳实践
# - 使用 fnm 管理 nodejs
#   - 进入项目路径手动执行 `fnm env | Out-String | Invoke-Expression; fnm use` 切换对应 nodejs
# - 使用原生安装的 pnpm 管理包依赖
#   - 若想使用 yarn ，官方仍然建议通过 Corepack 管理
#   - 先 fnm 切换到对应 nodejs 版本，然后执行 `corepack enable yarn` 生成 yarn 的垫片
# - 尽量避免全局安装包；若必须全局安装，则参考如下：
#   - 长期使用的工具安装用 `pnpm add -g <pkg>` ，不要用 npm/yarn 进行全局安装
#   - 临时工具或项目工具用 `npx <pkg>`
# - 如何识别项目本身使用的管理器
#   - 项目使用 Volta ______ package.json 中有 volta 字段
#   - 项目使用 fnm ________ 根目录有 .nvmrc 或 .node-version 文件
#   - 项目使用 Corepack ___ package.json 中有 packageManager 字段
#   - 项目使用 npm ________ 根目录有 package-lock.json 文件
#   - 项目使用 yarn _______ 根目录有 yarn.lock 文件
#   - 项目使用 pnpm _______ 根目录有 pnpm-lock.yaml 文件

# 类 nodejs
scoop install deno # bun
# Deno 由 rust 实现，对 nodejs 包兼容性好
# Bun 由 zig 实现，相比于 Deno 更关注性能
#   但是有内存泄漏问题，且被 Anthropic 使用 ai 基于 rust 重写，有待观望

# java/
scoop install openjdk17 openjdk21 # openjdk8-redhat

# 开发常用工具
# main/
scoop install curl openssl ffmpeg

# game
# extras/
gsudo scoop install vcredist2005 vcredist2008 vcredist2010 vcredist2012 vcredist2013 vcredist2022
scoop hold vcredist2005 vcredist2008 vcredist2010 vcredist2012 vcredist2013 vcredist2022
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

推荐软件

```shell
# start_with_os
# extras/
scoop install everything # translucenttb eartrumpet quicklook
# extras/
scoop install snipaste # trafficmonitor
# system clean program
# extras/
scoop install dismplusplus driverstoreexplorer
scoop install bulk-crap-uninstaller hibit-uninstaller # geekuninstaller
scoop install wizfile wiztree # spacesniffer freemove （不如直接软连接）
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
scoop install clash-nyanpasu flclash clash-party v2rayn gui-for-singbox
# gui-for-singbox 8k stars
# clash-nyanpasu 12k stars
# clash-party    19k stars
# flclash        29k stars
# v2rayn         94k stars
scoop install spotube
scoop install telegram # discord use https://discord.com/app

# book picture
# extras/
scoop install marktext neeview sumatrapdf
scoop install imageglass exifglass exiftool
# imageglass    Star 14K CSharp
# picview       Star 3.5k CSharp
# qview         Star 3.5k Cpp 轻量快速
# jpegview-fork Star 3.0k Cpp 小巧快速
# nomacs        Star 3.2k Cpp 主要为图片对比，可同步缩放平移

# video
# main/
scoop install yt-dlp youtube-dl
# extras/
scoop install youtube-dl-gui mpv # mpv.net k-lite-codec-pack-full-np vlc
scoop install magpie # 轻量级的窗口超分辨率工具
# nonportable
scoop install icaros-np
# potplayer
# scoop install potplayer madvr nonportable/lav-filters-megamix-np

# fonts
# extras/
scoop install fontforge # 开源字体编辑器
# nerd-fonts/
scoop install SarasaGothic-SC Maple-Mono-NF-CN UbuntuMono-NF-Propo # 中文等宽字体，个人安装
scoop hold SarasaGothic-SC Maple-Mono-NF-CN UbuntuMono-NF-Propo
```

常用的软件

```shell

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
scoop install inkscape gimp krita pixelorama
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
scoop install godot gdsdecomp
```

## check and restart

```shell
scoop checkup # Check for potential problems
scoop status  # Show status and check for new app versions
```

```shell
shutdown -r -t 0
```
