# 制作随从（基础版）

1.  控制台 `showracemenu` 捏脸并导出头模 （顺带记录头发hair/眼睛eyes/眉毛brow的编号名称）
1.  控制台 `SavePcFace XXX` 或 `spf xxx` 生成 "xxx.npc" 文件 （应该是CK里会用到，这里不涉及）
1.  新建mod文件夹，将导出内容放入对应路径 (meshes/textures) 
    - 头模在 SKSE\Plugins\CharGen\ 下有 nif/dds 文件
    - 独立身形也要把身形文件放进去 参考 meshes\actors\character\character assets\
    - 若使用其他模组的头发、眼睛、眉毛，也要把对应文件复制进去
1.  使用 SseEdit 打开 ESP 批量复制记录并修改
    - 身体在 Armor 中，会引用多个 Armor_Addon
    - 头在 Head_Part 中
    - 贴图在 Texture_Set 中，头身均要修改成自身贴图引用
1.  使用 SseEdit 进行 NPC 自定义 AI 技能等
1.  使用 SseEdit 右键 EPS "Clean Masters" 清楚无效引用
1.  使用 SseEdit 新增 "Relationship" （右键“添加” ） 详见 [SseEdit Relationship](#sseedit-relationship)
1.  使用 SseEdit 将 NPC 放入世界 详见 [SseEdit Cell](#sseedit-cell)
1.  使用 SseEdit 右键 EPS "Check for Errors" 检查错误
1.  使用 NifSkope 打开头模、身形等，修改对应贴图路径，注意不同贴图类型不要对应错
    - 叶子节点 名称 "BSShaderTextureSet"
    - 或者反过来，通过模型里的路径找到对应文件进行提取再修改路径也行
    - 虽然不提取修改路径暂时也没问题，但是换个模组环境可能就丢失了，所以建议提取打包
    - 若头发等存在物理(xml)，nif的根节点有"NiStringExtraData"，将其"String Data"修改为xml文件路径
1.  使用 NifSkope 修改节点值 "Name" 右键编辑字符串索引 将其改为 ESP 中的名词
1.  保存 ESP 和头模后完成

## SseEdit NPC

```
ACBS - Configuration
    Flags (sorted)        标志 参考如下
        Female
        Essential        标记为不死
        Auto-calc stats
        Unique
        PC Level Mult

Factions (sorted)    派系
    SNAM - Faction
        Faction     PotentialFollowerFaction [FACT:0005C84D]  【必选】潜在的随从
        Rank        0
    SNAM - Faction
        Faction     CurrentFollowerFaction [FACT:0005C84E]    【必选】当前随从 值必须-1 否则无法离队
        Rank        -1
    SNAM - Faction
        Faction     PlayerFollowerFaction [FACT:00084D1B]     不知有何用
        Rank        0
    SNAM - Faction
        Faction     JobMerchantFaction [FACT:00051596]        商人
        Rank        0
    SNAM - Faction
        Faction     PotentialMarriageFaction [FACT:00019809]  潜在结婚对象
        Rank        0
    SNAM - Faction
        Faction     PlayerMarriedFaction [FACT:000C6472]      已与玩家结婚
        Rank        0

VTCK - Voice        FemaleYoungEager [VTYP:00013ADC]

Actor Effects (sorted)    增加技能
    SPLO - Actor Effect   增加技能

WNAM - Worn Armor       【美化相关】身形记录
ANAM - Far away model   【美化相关】身形记录

Perks (sorted)  增加Perk
    PRKR - Perk
        Perk    增加Perk
        Rank    1

Items               --------------------------------          持有物品，自己添加

AIDI - AI Data
    Aggression      侵略性    Aggressive 潜行时也攻击 Unaggressive 潜行时不攻击
    Confidence      自信      Foolhardy 鲁莽 / Average 一般
    Energy Level    等级      50
    Responsibility  是否犯罪  "Any crime" / "No crime"
    Mood            表情      Neutral 中立 / Happy 开心
    Assistance      援助      Helps Friends and Alies （必选帮助盟友Alies）
    Aggro
        Aggro Radius Behavior  False
        Warn                   0
        Warn/Attack            0
        Attack                 0

Packages              定义行为 可不选 由随从管理框架取代
    PKID - Package    DefaultSandboxCurrentLocation1024 [PACK:000BFB6B]   当前区域默认互动（坐下等）
    PKID - Package    PlayerFollowerSayDismissPackage [PACK:00101006]
    PKID - Package    PlayerFollowerCombatOverridePackage [PACK:0005C851]
    PKID - Package    PlayerFollowerCombatOverridePackageExterior [PACK:00109124]

CNAM - Class   战斗风格
    CombatMageConjurer "召唤法师" [CLAS:0001CE14]

DNAM - Player Skills  增加对应流派熟练度

Head Parts (sorted)     【美化相关】头模记录
HCLF - Hair Color       【美化相关】发色

ZNAM - Combat Style  战斗风格

NAM6 - Height           【美化相关】身高
NAM7 - Weight           【美化相关】体重

DOFT - Default outfit   【美化相关】默认服装

FTST - Head texture     【美化相关】头材质
QNAM - Texture lighting 【美化相关】身材质
NAM9 - Face morph       【美化相关】脸部数据
NAMA - Face parts       【美化相关】脸部数据
Tint - Layers (sorted)  【美化相关】着色器数据
```

## SseEdit Relationship

```
DATA - Data
    Parent    选择制作的NPC
    Child     选择Player 00000007
    Rank      Ally 盟友
    Unknown   00
    Flags     保持空
    Association Type    保持 NULL
```

## SseEdit Cell

左边 ESP record list

```
Cell
    Block 0
        Sub-Block 9
            000133C6    沉睡巨人旅店   覆盖记录不要修改，右键新增 "Placed NPC"
```

右边 record 详情

```
Name - Base  选择制作的NPC

DATA - Position/Rotation    具体位置可以从ck中选择来生成
    Position
        X    -494.065308
        Y    -123.119308
        Z    0
    Rotation
        X    0
        Y    0
        Z    0
```
