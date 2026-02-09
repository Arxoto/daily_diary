# 字体

## 引擎渲染逻辑

同一个字体家族下的不同样式(Styles)（由渲染引擎自动选择）

- 字重
  - extralight
  - light
  - regular 默认样式
  - semibold
  - bold
- 意大利体/斜体
  - italic/Oblique

> - 存储格式：
>   - 一个字体家族分多个 ttf 文件，分别对应不同样式
>   - 每个字体文件中包含 cmap (Character Code Mapping) 表，其描述了这个样式所支持的字符
>
> - 渲染逻辑，假设引擎需要渲染某字体家族的 Bold 样式：
>   1. 样式定位，找到 XXX-Bold.ttf 文件
>       - 若存在，则进行下一步
>       - 若不存在，则触发【样式回退】，尝试使用 XXX-Regular.ttf 进行下一步（成功后由渲染引擎生成“伪样式”显示）
>   1. 码点映射，在对应 ttf 文件的 cmap 中找到该字符
>       - 若成功则进行渲染（或生成“伪样式”渲染）
>       - 若失败，则触发【字体回退】，使用字体列表的下一个字体家族重新尝试
> 
> 注意：若 XXX-Bold.ttf 的 cmap 不支持该字符，无论 XXX-Regular.ttf 是否支持，都会触发【字体回退】，
> 因此要保证 Regular 样式支持的字符在其他样式里都支持，
> 或是直接不提供 XXX-Bold.ttf 强制让其根据 XXX-Regular.ttf 渲染

## 推荐字体

- `Sarasa Mono SC` 紧凑等距字体，破折号 **全角** 、引号半角，支持连字
  - `scoop install SarasaGothic-SC`
- `Maple Mono NF CN` **宽松** 等距字体，破折号半角、引号半角，支持连字
  - `scoop install Maple-Mono-NF-CN`
- `UbuntuMono Nerd Font Propo` 紧凑等距字体，破折号半角、引号半角， **不支持连字**
  - `scoop install UbuntuMono-NF-Propo`

### 更纱黑体 (Star 11.8k)

[SarasaGothic](https://github.com/be5invis/Sarasa-Gothic/)

`scoop install SarasaGothic-SC` 同时安装多个字型（多个字体家族）

字型(Variant)

```
        等距    弯引号  破折号  连字
Gothic  no      全宽    全宽    no
UI      no      半宽    全宽    no
Mono    yes     半宽    全宽    yes
Term    yes     半宽    半宽    yes
Fixed   yes     半宽    半宽    no

衬线(Slab)      粗衬线体，类似于顿笔
连字(Ligature)  特定连续字符会组合显示
```

地区语言(Variant)

```
SC  Simplified Chinese  简体中文
TC  Traditional Chinese 台湾繁体中文
HC  HongKong Chinese    香港繁体中文
CL  Classical           传统旧字形
J   Japaness            日文
K   Korean              韩文
```

### Maple (Star 23.4k)

[Maple](https://github.com/subframe7536/Maple-font)

`scoop install Maple-Mono-NF-CN` 仅安装一个字体家族

Features

- Ligature: Default version with ligatures (`Maple Mono`)
- No-Ligature: Default version without ligatures (`Maple Mono NL`)
- Normal-Ligature: --normal preset with ligatures (`Maple Mono Normal`) （看起来不那么“主观”）
- Normal-No-Ligature: --normal preset without ligatures (`Maple Mono Normal NL`) （看起来不那么“主观”）

Format and Glyph Set

- TTF: Minimal version, ttf format [Recommend!]
- NF: Nerd-Font patched version, add icons for terminal (With `-NF` suffix)
- CN: Chinese version, embed with Chinese and Japanese glyphs (With `-CN` suffix)
- NF-CN: Full version, embed with icons, Chinese and Japanese glyphs (With `-NF-CN` suffix)
- others...

Font Hint

- Hinted font is used for low resolution screen(<=1080P) to have better render effect.
  - In this case, you can choose `MapleMono-TTF-AutoHint` / `MapleMono-NF` / `MapleMono-NF-CN`, etc.
- Unhinted font is used for high resolution screen.
  - In this case, you can choose `MapleMono-OTF` / `MapleMono-TTF` / `MapleMono-NF-unhinted` / `MapleMono-NF-CN-unhinted`, etc.

## 字体显示测试

```
e.g.

等距字体、字母辨识度
|aa|ss|dd|
|阿|松|大|
|  1iIl  |
|  0oOQ  |
|  8BCD  |

标点符号（一般都应该是等距的）
EN |, . : ; ? ! \ | () | [] | <> | $_ |
CN |，。：；？！、|（）|【】|《》| ￥ |

标点符号（《通用规范汉字表》中规定应该是全角的，大部分字体也处理成全角）
    破折号 省略号
EN |  --  |  ^^  |
CN | —— | …… |

标点符号（《通用规范汉字表》中规定应该是全角的，大部分字体出于编程考虑一般处理成半角）
    双引号 单引号 反引号
EN |  ""  |  ''  |  ``  |
CN | “” | ‘’ | ·· |

连字
<> <-> -> <- --> <-- <= >= == === ---
@ # % ^ & * / \ - + _ =
```

## 自定义修改字体

可以使用 fontforge https://fontforge.org/ 按照自己的习惯定制化的修改字体
1. 打开字体文件：字体家族 "Sarasa Mono SC" 默认字体对应 SarasaMonoSC-Regular ；
1. 找到全角引号的码点(U+201C/U+201D)；
1. 调整它们的 Advance Width （前进宽度），将其从 500 增加到 1000 ；
    - 字体家族 "Maple Mono NF CN" 则为 600 到 1200 ；
1. 重新导出。这样你就得到了一个“标点全角化”的专属更纱黑体。

或者见 [fontforge脚本](../script/font_fix_punctuations/font_fix_punctuations.py) 

注：脚本仅调整宽度、侧边对齐、修改元数据信息，因此需要使用破折号和省略号本身即为全角的字体为模板生成，否则会有大量的空白

```shell
# 注意工作目录要在字体文件下
fontforge -script font_fix_punctuations.py
~/scoop/apps/fontforge/current/fontforge.bat -script ./font_fix_punctuations.py

# or
~/scoop/apps/fontforge/current/bin/ffpython.exe
# 然后运行脚本（注意路径）
```
