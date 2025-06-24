# switch emulator

- Yuzu 柚子（被正义制裁）
  - from the creators of Citra and written in C++
  - https://github.com/yuzu-emu/
  - https://yuzu-mirror.github.io/

- Yuzu 分支（秽土转生版）
  - Sudachi 【推荐】实测帧率稳定一点
    - https://sudachi-emu.com/
    - https://sudachi.emuplace.app/
    - https://github.com/sudachi-emu/sudachi
  - Suyu 开发组不稳定
    - https://suyu.dev/
    - https://github.com/suyu-emu/suyu
  - Torzu
    - https://github.com/litucks/torzu

- Ryujinx 龙神
  - created by gdkchan and written in C#
  - https://ryujinx.org/
  - https://github.com/Ryujinx/Ryujinx

## Firmware and Prod Keys

固件和key从这个网站上下载 
- https://prodkeys.net/dl/
- key: 文件 - 打开suyu文件夹 - keys - prod.keys & title.keys
- firmware: 工具 - 安装固件 - Firmware-Unzipped-Folder

P.S. 固件也可以从这里获取 https://github.com/THZoria/NX_Firmware/releases

## Game

download from
- https://www.gamer520.com/

基础设置
- 图形
  - API  ( Vulkan )
  - Resolution 分辨率  ( 1X )  画质性能影响较大 自己取舍
  - WindowAdaptingFilter 窗口滤镜  ( Bilinear 双线性 | AMD_FidelityFX )  对画质影响自己测试
- 图形高级
  - ASTC_RecompressionMethod 纹理重压缩  ( BC3 )  经测试对画质影响不大 性能自信可以选中不压缩
- 每个游戏右键可打开着色器缓存 玩的越久缓存越多越流畅
  - vulkan.bin 文件可替换 不随环境改变 PC、模拟器版本、模拟器设置等 实测还是要替换的 可能是跨大版本了
  - vulkan_pipelines.bin 文件 每次更新版本或设置后需要删除重建

mods and cheats
- 前提 游戏版本 金手指版本/mod版本 要一致
- 模拟器中右键游戏 打开 MOD 目录
- mod 直接解压在该目录即可
- 金手指路径参考 yuzu\load\id\可自定义的金手指名称\cheats\txt
  - txt 有多个文件的话一般是多个版本号一起打包的 仅保留一个（最开头有初始化代码的话需要保留）
  - 文件内容可根据需要进行修改、拆分
  - 模拟器中右键游戏 属性 勾选需要的金手指
- sudachi 实测好像金手指不生效 不知是否是配置导致
- 龙神金手指使用方法
  - 关闭着色器缓存 options>settings>system>enable pptc
  - 在每一个需要的代码前面加上 `580F0000 04616BF8` （其他生效的项的第一行代码）

amiibo
- 可选 模拟-设置-控制-高级-其他-RandomAmiiboId
- amiibo bin 文件直接拖入模拟器中

联机
- 模拟-设置-系统-网络-选择对应的连接方式（ wifi 为 WLAN ）
- 多人游戏-公共房间
- 修改昵称
- 选择一个房间（高亮选中即可）后关闭该窗口
- 开始游戏

## Game Pack

包处理工具
- https://github.com/julesontheroad/NSC_BUILDER
- fill prod.keys in NSCB\ztools\keys.txt
- 如果不需要每次自动更新 NUT DB 可以解压 NSCB\zconfig\zconfig_no_update.7z 文件到当前目录，覆盖文件
- 如果想手动更新 NUT DB 可以打开 NSCB\zconfig\NUT_DB_URL.txt 下载 https://**.json 然后修改对应后缀放入 NSCB\zconfig\DB\
- 上一条实测原址已经下不到了 从镜像下载 备份见本项目的 NSCB_DB\
- 执行 NSCB.exe 输出文件在 NSCB\NSCB_output\

```
输入 "1"  单文件处理   （ XCI/NSP互转 【常用功能】 ）
输入 "2"  多文件处理   （ XCI整合用 【常用功能】 ）
输入 "3"  文件拆分     （ XCI/NSP拆包 【常用功能】 ）
输入 "4"  文件信息查询 （ 游戏版本信息等 【常用功能】 ）
输入 "5"  数据库构建   （ 重建游戏文件数据库 ）
输入 "6"  高级选项     （ 修补链接账户要求等 【常用功能】 ）
输入 "7"  合并模式     （ 文件合并 ）
输入 "8"  压缩/解压    （ XCI转XCZ/NSP转NSZ 【常用功能】 ）
输入 "9"  文件还原     （ 从备份文件恢复原始包 ）
输入 "10" 文件管理     （ 暂无功能 ）
输入 "0"  配置选项     （ 设置程序配置 ）
```
