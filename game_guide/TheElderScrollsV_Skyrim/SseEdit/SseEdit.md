# SSE Edit

https://www.nexusmods.com/skyrimspecialedition/mods/164

摁住 Ctrl 可以打开多个 record 方便拖拽复制（仅同一个ESP内）

## 安装方式

see https://magicskyrim.net/archives/5764

1. 解压SSEedit至任意位置
1. MO2左侧新建一个空MOD文件夹，名叫 SseEditOutput
1. MO2可执行程序里指定 SSEEdit.exe 位置
1. “参数”里填入 " -cp:utf-8"（注意前面有空格）
1. “在MOD中创建文件夹代替overwrite中”指定为刚刚新建的 SseEditOutput

## Magic Effect 魔法效果

see https://ck.uesp.net/wiki/Magic_Effect

```
Record Header
EDID - Editor ID                唯一标识 根据 ESP 排序前几位可能改变 后几位在内部固定
VMAD - Virtual Machine Adapter
FULL - Name                     显示名称
MDOB - Menu Display Object      菜单显示效果
KSIZ - Keyword Count            关键字数量
KWDA - Keywords                 关键字，不做任何事，用于条件函数和调用游戏系统赋予的效果
Magic Effect Data               效果
    DATA - Data
        Flags (sorted)  标签，用于特殊逻辑
            Hostile  被敌对，恢复术不要点
            Detrimental  取负值，恢复术点了会扣血
            Recover  效果结束时返回初始状态，数值修改器和峰值修改器会在开始时修改、结束时改回，即对恢复术来说，选中是buff，不选是治疗
            FX Persist  视觉效果持续到结束，不选只有一次
            Snap to Navmesh  选中此项将会在使用 Aimed 或 Target_Location 时把效果附在 Navmesh 上（此处你可以理解为地面上），一般用于召唤物
            No Recast  选中时此效果时在效果结束前不能在目标上再次释放
            No Hit Effect  不会出现命中时的视觉效果
            No Death Dispel  如果目标已死亡效果也仍然触发
            No Duration  没有持续时间，瞬时触发
            No Hit Event  不会触发命中事件，主要用于潜行系技能
            No Magnitude  效果不使用 Magnitude 字段（效果力度，如作为伤害参数）
            No Area  取消区域判定
            Painless  无痛，如果同时选中 Hostile 则目标不会喊疼，如果目标是玩家不会出现视觉模糊和呻吟
            Gory Visuals  没有使用，没效果
            Hide in UI  魔法效果将不会出现在法术描述和魔法效果那一栏里
            Power Affects Magnitude  在wiki中没有解释
        Base Cost  法术消耗的乘数，不影响自动计算的法术消耗（https://ck.uesp.net/wiki/Spell#Notes）
        Assoc. Item  与Effect_Archetype有关
        Magic Skill  受哪一系法术perk影响，并为其提供经验
        Resist Value  受抗性影响
        Counter Effect count
        Casting Light  蓄力时手中光效
        Taper Weight  持续时间结束后，效果保留一段时间但强度减弱，称为锥度持续时间，这是锥度权重
        Hit Shader  命中时shader（理解为光效）
        Enchant Shader  附魔时的光效
        Minimum Skill Level  NPC使用效果的最低要求，同时影响法术等级，0新手、25学徒、50熟练、75专家、100大师
        Spellmaking  Magnitude/Duration perk影响范围还是持续时间
            Area  效果影响面积？
            Casting Time  施法时间？
        Taper Curve  锥度曲线，控制效果减弱的速度
            - 当前大小 = 效果大小 * 锥度权重 * (1-时间/锥度持续时间)^锥度曲线
            - magnitude = effect magnitude * Taper Weight * (1 - taper time / Taper Duration)Taper Curve
            - 总大小（仅当锥度曲线>-1） = 效果大小 * 锥度权重 * 锥度持续时间 / (锥度曲线+1)
            - magnitude = effect magnitude * Taper Weight * Taper Duration / (Taper Curve + 1)
            - 锥度曲线=0 效果保持不变
            - 锥度曲线=1 效果线性递减
            - 锥度曲线越大 下降越快 负数意味着增加 但不建议小于-1
        Taper Duration  锥度持续时间
        Second AV Weight
        Archtype  在wiki中没解释 应该是修改类型 参考 "Peak Value Modifier"
        Actor Value  在wiki中没解释 应该是角色属性修改 参考 
            - 强化生命[MGEF:000493AA]  强化体力[MGEF:00049507]  强化法力[MGEF:00049504]
            - "Health"                 "Stamina"                "Magicka"                 属性值上限
            - "Heal Rate"              "Stamina Rate"           "Magicka Rate"            属性恢复速度（设为10，每秒恢复10%）
            - "Heal Rate Mult"         "Stamina Rate Mult"      "Magicka Rate Mult"       属性恢复速度提升（设为100，每秒恢复翻倍）
            - 强化负重[MGEF:0007A0F4]
            - "Carry Weight" 负重上限
            - 强化龙吼[MGEF:0008850D]  龙吼计时[MGEF:0401DF9A]
            - "Shout Recovery Mult" 龙吼恢复速率 建议为 20% 倍数（大多冷却时间为5的倍数）
        Projectile  飞行物，子弹，若添加了多个则只生效第一个
        Explosion  子弹命中时产生的爆炸物
        Casting Type  如何触发
            - Concentration 按住持续施放
            - Fire_and_Forget 蓄力后施放
            - Constant_Effects 恒定效果
            - 法术或结界的所有效果必须具有相同的施法类型
        Delivery  效果如何传递到目标
            - Self 施法者自身
            - Contact 接触，通过命中触发，只能用于武器，一般用于附魔
            - Aimed 瞄准，将效果附加在Projectile（子弹）上，命中时触发效果，如大火球爆炸
            - Target_Actor 目标角色，立刻作用于准星上的角色，第三人称时不好用
            - Target_Location 目标物体景观，同上，无Projectile，如寒霜符文
            - 法术或结界的所有效果必须具有相同的传递类型
        Second Actor Value
        Casting Art  蓄力时手中特效
        Hit Effect Art  命中时特效
        Impact Data  子弹击中物体时使用哪些贴花
        Skill Usage Multiplier  收获经验的乘数
        Dual Casting
            Art  双手施法时的特效
            Scale  双手施法时的范围
        Enchant Art  附魔时的特效
        Unknown
        Unknown
        Equip Ability  效果被装备时的行为（？），不可链式触发
        Image Space Modifier  效果触发时的图像空间（也是特效）
        Perk to Apply  仅为玩家使用，触发效果时添加perk
        Casting Sound Level  在wiki中没有解释，猜测是蓄力时的声音，影响潜行被发现
        Script Effect Al  敌人AI
            Score  越大使用越频繁
            Delay Time  冷却
Counter Effects                不使用
SNDD - Sounds
DNAM - Magic Item Description  描述 <mag> 效果大小（增幅） <dur> 持续时间 <area> 范围
Conditions
```

## Spell 法术

```
MDOB - Menu Display Object  菜单显示效果
ETYP - Equipment Type       装备类型
DESC - Description
SPIT - Data
    Base Cost       基础消耗
    Flags
    Type
    Charge Time     蓄力时间
    Cast Type       消耗类型  参考 Magic_Effect 的 Casting Type  如 Fire_and_Forget
    Target Type     目标类型  参考 Magic_Effect 的 Delivery      如 Target_Location
    Cast Duration
    Range
    Half-cost Perk
Effects             造成的魔法效果 可以有多个 且魔法效果内设定条件 达到根据不同条件施放不同效果
    Effect
        EFID - Base Effect  对应魔法效果ID
        EFIT- EFIT
            Magnitude       效果力度
            Area            效果范围
            Duration        持续时间
        Conditions          生效条件
```

## Object Effect 附魔

```
ENIT - Effect Data
    Enchantment Cost     附魔消耗
    Flags
    Cast Type            消耗类型  参考 Magic_Effect 的 Casting Type
    Enchantment Amount   附魔数量
    Target Type          目标类型  参考 Magic_Effect 的 Delivery
    Enchant Type         附魔类型
    Charge Time          充能时长
    Base Enchantment     基础附魔
    Worn Restrictions    破坏限制  武器类设为空 盔甲类影响可附魔部位
Effects
    Effect
    EFID - Base Effect  对应 Magic_Effect ID
    EFIT- EFIT
        Magnitude       效果力度
        Area            效果范围
        Duration        持续时间
    Conditions          生效条件
        Condition
```

## Weapon 武器

todo

## Armor Addon 盔甲插件

盔甲对应模型，男性女性、第一人称第三人称

一个身体对应多个 Armor_Addon 足、手、身

## Armor 盔甲 同时身体也属于这里

```
KWDA - Keywords
    种类 ArmorLight轻甲 ArmorHeavy重甲
    材质 ArmorMaterialXxx
    部件 ArmorBoots足 ArmorCuirass身 ArmorGauntlets手 ArmorHelmet头
    贩卖 VendorItemXxx
Armature
    MODL - Model FileName  对应 ArmorAddon ID
```

## Constructible Object 可锻造物品

```
Items (sorted)        消耗材料 可以有多种
    Item
        CNTO - Item
            Item      消耗材料
            Count     消耗数量
        COED - Extra Data
Conditions            强化已附魔装备的条件 可以有多个
    Condition
        CTDA - CTDA
            Type
            Comparison Value - Float
            Function
            xxxx
        CIS 1 - Parameter #1
        CIS2 - Parameter #2
CNAM - Created Object        锻造产品
BNAM - Workbench Keyword     锻造台关键字
NAMI - Created Object Count  锻造产品数量
```

## ESM ESP ESL 转换

插件分类

- ESM Elder_Scrolls_Master
- ESP Elder_Scrolls_Plugin
- ESL Elder_Scrolls_Light_Plugin

引擎插件使用 FormID 标记不同记录 record

FormID 格式为 8位 16进制数，一个 record 表示一个最基本的游戏组成元素，如魔法效果、法术、武器、装备、套装、NPC等等，且能相互引用

对于ESM、ESP，将其前两位作为插件的ID，随着插件的排序而改变，插件必须排在其依赖插件的后面，若记录有覆盖，则后面的生效

因此引擎允许256个插槽（00-FF，16^2），实际能够加载插件数需减去官方的本体和DLC等

同时一个插件允许内部有 16^(8-2) 个记录，绝大多数模组，包括官方本体DLC都用不完这么多，因此存在浪费并且限制了插件加载数量

特殊的，FE加载顺序槽是专为ESL保留的，ESL在使用后面3位做ESL的排序，即最多允许加载 4096(16^3) 个 ESL ，而每个 ESL 内最多定义 4096 个记录

综上所述，ESM+ESP不能超过254(FD)，FE是ESL插件共用的一个排序位置，而FF则是临时引用需要占用的，游戏里随机事件刷出来的人物用控制台点击就可以看到FF开头。

此外，对于排序来说，ESM必须在最前面，而后是ESP，最后是ESL。

特殊的，ESP可被标记为ESM/ESL（不冲突可同时标记，同理ESL也可标记为ESM），当ESP标记为ESM时，加载顺序等同ESM，当ESP标记为ESL时（ESPFE），记录上限等同ESL。

### 使用 SSE Edit 将 ESP 转换为 ESL

本质上是将 ESP 标记为 ESL

1. MO 中 SseEdit “参数”添加" -PseudoESL"（实测不加好像也行，但教程都这么说，这里也记录着）
1. 待 SseEdit 加载完成
1. 右键 ESP 选择 "compact form id for esl" （注意！会导致 FormID 变更，存档损坏，且依赖该ESP的其他插件可能受影响，也许一起加载会自动处理，但没验证过）
1. 选择 Header - RecordFlags - 勾选"ESL"

