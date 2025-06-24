# 上古卷轴5 天际

参考 https://fkmods.freeflarum.com/d/9/5

参考 https://api.xiaoheihe.cn/v3/bbs/app/api/web/share?link_id=129162560

## Mod Organizer

模组管理工具，基于虚拟文件系统极大优化了各种模组的覆盖冲突问题

https://www.nexusmods.com/skyrimspecialedition/mods/6194

https://github.com/ModOrganizer2/modorganizer

也可以用 Vortex https://www.nexusmods.com/about/vortex/

N网 联合 MO 作者一起开发的新模组管理器，底层基于硬链接实现模组本体解耦合

优点是支持游戏更多，性能更好（理论上、实际基本忽略不计），模组之间的文件覆盖更加灵活，fnis和bodysilde等使用起来相对简单

缺点是还是会一定程度上污染本体，有bsa打包文件的模组文件覆盖是根据esp来的、而不是MO那样的根据目录顺序（早期的认识、近期没了解过）

由于使用MO习惯了，且网上早期吐槽Vortex使用不友好，建议先主用MO，感兴趣可体验Vortex

## ENB

ENBSeries is 3d graphic modification for games like TES Skyrim, TES Oblivion, Fallout, GTA, Deus Ex, and others.

It work by modifying render functions calls of the games and applying additional effects.

ENB 核心 下载

- http://enbdev.com/download.html
- http://enbdev.com/download_mod_tesskyrimse.html

ENB 预设下载

- N网 分类 Presets - ENB and ReShade
- https://www.nexusmods.com/skyrimspecialedition/mods/categories/97/

区别于普通Mod，安装在本体根目录下，故单独列出

## Community Shaders

https://www.nexusmods.com/skyrimspecialedition/mods/86492

社区着色器，与 ENB 不兼容，区别如下

- ENB 较为成熟，社区有大量预设，画面表现好，性能优化差
- 社区着色器 有革命性的独门技术突破，更新活跃，画面表现稍欠、性能优化好（目前来说），结构上是普通模组方便管理

## SKSE

The Skyrim Script Extender (SKSE) is a tool used by many Skyrim mods that expands scripting capabilities and adds additional functionality to the game.

在MO中用skse64_loader.exe启动游戏

https://www.nexusmods.com/skyrimspecialedition/mods/30379

区别于普通Mod，安装在本体根目录下，故单独列出

## 整合包

直接说整合包吧，模组前置数量庞大，这里暂不写，一般整合包都提供本体并附带了ENB和SKSE

- 烽火整合及其原创模组 https://magicskyrim.net/
  - 基础稳定，特色是其原创和魔改的战斗系统
- 绝伦整合X5 https://www.bilibili.com/video/BV19MUFY7Ew8/
  - 新东西较多，特色是整合了最前沿的各种战斗框架
  - 不直接分享成品包，仅提供modlist等，建议参考其自己配置

## SSE Edit

ESP 编辑器

在 MO 中打开建议在“参数”中填写 " -cp:utf-8" （注意前面有空格）以支持中文正常显示

详见 file://./SseEdit/SseEdit.md

## NifSkope

NIF 网格模型编辑器

详见 file://./NifSkope/NifSkope.md
