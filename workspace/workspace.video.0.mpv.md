# MPV

https://mpv.io/manual/master/
https://hooke007.github.io/unofficial/mpv_start.html

## 基础配置

mpv.exe 旁边新建一个 portable_config 文件夹，该目录具有最高级的优先级，一旦存在此文件夹，其它所有的设置目录都会被忽略。

新建 ./portable_config/mpv.conf 确保文本编码为 UTF-8

```conf
#hwdec=auto-safe                         # 默认值 no 为软解 建议仅软解慢时手动切换 see https://mpv.io/manual/master/#options-hwdec
#vo=gpu                                  # <gpu|gpu-next> 视频输出驱动 默认值 gpu 具有最高普适性和完成度
#profile=fast                            # 性能优先的渲染预设 (for --vo=<gpu|gpu-next> only)
#profile=high-quality                    # 质量优先的渲染预设 (for --vo=<gpu|gpu-next> only)
#gpu-api=d3d11                           # 指定使用的图像 API 的优先级列表
#gpu-context=d3d11                       # 指定使用的 GPU 上下文优先级列表
#d3d11-adapter=NV                        # 指定 D3D11 适配器进行渲染 值可以前缀匹配 可用于双显卡笔记本 (for --gpu-api=d3d11 only)
#vulkan-device=                          # 指定 Vulkan 设备进行渲染 值必须为完整设备名 见任务管理器 (for --gpu-api=vulkan only)

no-input-builtin-bindings               # 屏蔽全部内建的原始快捷键预设
#no-input-default-bindings               # 进一步屏蔽外置脚本内的静态若绑定预设
save-position-on-quit=yes               # 退出时保存当前播放状态
keep-open=yes                           # 播完列表暂停
watch-later-options=start,vid,aid,sid   # 指定保存播放状态的属性列表（播放位置、视频、音频、字幕轨号）
audio-file-auto=fuzzy                   # 自动加载同名外置音轨
sub-auto=fuzzy                          # 自动加载同名外置字幕
icc-cache-dir="~~/icc_cache"            # 保存缓存加速启动
gpu-shader-cache-dir="~~/shaders_cache" # 保存缓存加速启动
screenshot-directory="~~desktop/"       # 截图输出在桌面
#log-file="~~desktop/mpv.log"            # 输出log日志在桌面
```

新建 ./portable_config/input.conf 确保文本编码为 UTF-8

```conf
MBTN_LEFT      ignore               # <无操作> [左键-单击]
MBTN_LEFT_DBL  cycle fullscreen     # 切换 全屏状态 [左键-双击]
MBTN_RIGHT     cycle pause          # 切换 暂停/播放状态 [右键-单击]
WHEEL_UP       add volume  2        # 音量 +
WHEEL_DOWN     add volume -2        # 音量 -
SPACE          cycle pause          # 切换 暂停/播放状态 [空格键]
ENTER          cycle fullscreen     # 切换 全屏状态 [回车键]
ESC            set fullscreen no    # 退出 全屏状态 [ESC]

UP             add volume  2        # 音量 +
DOWN           add volume -2        # 音量 -
LEFT           seek -5              # 后退 5s
RIGHT          seek  5              # 前进 5s
-              add speed -0.5       # 播放速度 -（最小0.01）
=              add speed  0.5       # 播放速度 +（最大100）
BS             set speed  1.0       # 重置播放速度 [退格键]
[              frame-back-step      # （暂停）帧步退
]              frame-step           # （暂停）帧步进
l              ab-loop              # 设置/清除 A-B循环点

# add audio-delay -0.1         # 音频同步 提前100ms
# add audio-delay  0.1         # 音频同步 滞后100ms
# set audio-delay  0           # 重置音频同步
# add sub-delay   -0.1         # 字幕同步 提前100ms
# add sub-delay    0.1         # 字幕同步 滞后100ms
# set sub-delay    0           # 重置字幕同步

ctrl+h    cycle-values hwdec "no" "auto-safe"  # 切换硬解
`         script-binding console/enable        # 打开控制台 ESC退出
i         script-binding stats/display-stats
I         script-binding stats/display-stats-toggle
```

## 内置脚本

新建 ./portable_config/script-opts/script_name.conf 为同名脚本的配置

### 控制台 console.lua

- 快捷键 ` 唤起控制台
- 快捷键 ESC 关闭

官方手册定位： https://mpv.io/manual/master/#console

### 数据统计 stats.lua

- 快捷键 i 短暂显示
- 快捷键 I 常态显示

官方手册定位： https://mpv.io/manual/master/#stats

## 脚本插件

新建 ./portable_config/scripts/script_name.lua

对应配置 ./portable_config/script-opts/script_name.conf

https://github.com/mpv-player/mpv/wiki/User-Scripts#lua-scripts

- autoload.lua：自动载入播放列表
- playlistmanager.lua：播放列表显示

