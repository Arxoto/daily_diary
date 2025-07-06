# Godot 4 教程《勇者传说》

from https://www.bilibili.com/video/BV1Z94y1V74m

基于 Godot v4.4 的一个像素风横板动作游戏制作指南

## 基础项目、测试场景、简单人物

像素风游戏的常用配置（画面放大三倍）

- 左上角-项目-项目设置
- 打开右上角高级设置，显示-窗口
  1. 窗口宽度高度覆盖调整至视口大小
  1. 视口大小调整至原来的 1/3 （直接在后面输入/3能自动计算）
  1. 拉伸-模式 选择 canvas_items
  1. 置顶
- 渲染-纹理-默认纹理过滤-【Nearest】（像素风的清晰化）
- 左上角-编辑器-编辑器设置-文本编辑器-补全-启动【添加类型提示】

添加世界

- 场景-创建根节点处，创建【2D场景】，重命名为【World】
- 添加子节点，类型【TileMap】
  - 新版 TileMap 被弃用，使用 TileMapLayer 代替
- 右侧检查器 TileMapLayer-TileSet 新建 TileSet
- 点击刚刚创建的【TileSet】展开
- 展开【PhysicsLayers】，点击添加元素
- 底部【TileSet】面板
- 将图片资源拖入面板里的【图块源】
- 若有弹框提示：施放自动在不透明纹理区域创建图块，选择否
- 在基础图块中选择想要使用的图块（设置工具）
- 工作区中间的绘制工具-绘制属性【物理层0】-涂抹对应图块标识物理碰撞
- 底部【TileMap】面板可选中图块在上面画布中绘画地图（左键绘制、右键擦除、Shift画直线、Ctrl画布中获取图块）

添加人物

- 上方添加新场景-根节点选择其他节点-【CharacterBody2D】-改名Player
- 添加子节点【Sprite2D】用来显示图像
  - 将人物动作关键帧的图片（一般所有动作在一个图中）拖入右侧【Texture】
  - 左上角-项目-项目设置-渲染-纹理-默认纹理过滤-【Nearest】（像素风的清晰化）
  - 右侧检查器-Region-Enabled（将一个图划分成多个区域）-编辑区域
  - 左上角吸附模式-栅格吸附-调整步长-将一连串动作帧选中
  - 右侧检查器-Animation-Hframes（水平帧）调整对应值使其显示为一个动作帧（之后就可以使用Frame属性自动显示对应帧了）
- 添加子节点【CollisionShape2D】用来定义碰撞形状
  - 右侧检查器-Shape-选择【新建RectangleShape2D】创建矩形碰撞箱
- 添加子节点【AnimationPlayer】用来定义动画（用来控制其他子节点的各项属性如何根据时间轴改变）
  - 下方工作区-动画-创建新动画
  - 工作区的上方右侧调整总长度和打开循环
  - 切换到【Sprite2D】节点，将一下属性新建轨道并插入关键帧
    - Region-Rect 因为不同动画的区域范围可能会不一样
    - Animation-Hframes 因为不同的动画（动作集）的Hframes可能会不一样
    - Frame 需要将对应动作帧依次加入，注意工作区的下面【吸附】调整对应的每帧时间，像素游戏可以0.1秒1帧
    - 注意要保持所有动画的轨道一致，不然会有状态残留导致各种BUG
- 根节点添加脚本自定义控制逻辑
  - 注意物理引擎相关的逻辑写在 _physics_process 方法中
  - 根据重力下降
  - 根据输入移动 
    - 项目-项目设置-输入映射页签
    - 添加自定义的输入按键和对应的动作名称
    - 右侧加号配置监听的按键事件
    - 脚本中使用 Input 类的方法获取输入
    - 左右移动可使用 Input.get_axis 方法根据两个按键自动得到正负一的值
    - 使用默认方法 is_zero_approx 判断值是否为零
    - 使用 move_and_slide 自动根据速度和碰撞计算位置
  - 若要脚本中控制对应子节点
    - 拖动对应子节点
    - 摁住 Ctrl 然后松开鼠标左键，能自动为节点创建变量
    - 如使用 AnimationPlayer 的 play 方法播放动画
      - 每帧都可以调用，应该内部维护了一个状态，不会重复播放相同的内容
    - 如控制 Sprite2D 的 flip_h 属性控制水平翻转
- 在世界根节点上实例化子场景-选择player添加实例

## 相机

此时看到的画面不会随人物移动，测试场景较大的情况下，人物会跑出画面，因此需要设置相机

- 世界中的Player节点-添加子节点-Camera2D（因为要让相机跟随人物移动）
- 拖动相机框的准心调整相对位置（Ctrl键方便对齐）
- 右侧检查器-Drag-启动【Horizontal】和【Vertical】打开水平垂直拖拽效果
- 右侧检查器-PositionSmoothing-启用位置平滑
- 为防止相机看到场景以外的空白，可设置【Limit】属性，并打开【Smoothed】平滑效果
- 也可以在World根节点的脚本 `_ready` 里根据TileMap的矩形框的范围动态设定限制
  - 注意单位是像素和TileSet元素个数的单位转换
  - 注意方法的生命周期，在 `_ready` 里设置 limit 的时候若相机已经超出了限制区域，会场景开始时就触发平滑移动
  - 可在方法最后使用 `reset_smoothing()` 方法在一帧内快速达到平滑移动的目的地

注意：

- 若启用相机平滑后，人物移动出现模糊抖动，解决办法有两个
  - Camera2D 的 ProcessCallback 属性设为 Physics
  - 打开物理插值，但缺点是下面的功能：代码控制相机限制时设定初始位置瞬移会不生效
    - 并且有警告 Camera2D 覆盖了 physics_process 由于使用了物理插值（解决办法是同时使用另一个方法）

```
	var used_rect := tile_map_layer.get_used_rect().grow(-1) # 缩小一格
	var tile_size := tile_map_layer.tile_set.tile_size
	
	camera_2d.limit_top = used_rect.position.y * tile_size.y
	camera_2d.limit_bottom = used_rect.end.y * tile_size.y
	camera_2d.limit_left = used_rect.position.x * tile_size.x
	camera_2d.limit_right = used_rect.end.x * tile_size.x
	
	camera_2d.reset_smoothing()
```

## 地形编辑

此时测试环境较为简略，本章简单介绍了几种 TileMap 使用方式，搭建较为完整的场景

- 在下方工作区 TileSet 选中要使用的各个元素（设置工具）
- 若元素向边缘有拓展
  - 中间的选择工具，选中对应图块，使用四周的小圆圈进行拓展
  - 配置中心位置（图块的中心）：选择工具-渲染-纹理原点
  - 配置中心位置（批量方式）：绘制工具-绘制属性【渲染】-纹理原点-调整后拖动即可

此时基本具备绘制场景的能力，但需要手动选择对应图块，效率很低，可以使用地形工具

地形能根据图块所在的相对位置自动选择显示哪种图块

- 右边检查器-【TileSet】展开-【TerrainSets】-添加元素添加一个地形集
- 选择【MatchCorners】即根据角落进行匹配
- 【Terrains】-添加元素添加一个实际地形
- 【Name】命名一个有意义的名称（大地/树干/岩浆等等）
- 工作区-【TileSet】-绘制工具-【绘制属性】地形-【地形集】选择刚刚创建的地形集
- Ctrl+Shift 进行拖动，将对应图块添加到地形中
- 绘制工具-【地形】选择刚刚创建的地形名称-为每个图块设置临界图块的匹配规则
- Ctrl+Shift 进行拖动，批量设置规则
- 工作区-【TileMap】-地形页签-选中对应的地形名称
- 可在地形编辑器中批量绘制 Ctrl+Shift 多个方块进行组合绘制
- 地形图块默认每个图块出现的比例是相同的，想要定制概率
  - 工作区-【TileSet】-绘制工具-【绘制属性】概率

图块进阶

- 若想在几个图块中随机选中图块进行绘制
  - 图块中 Shift 同时选中多个图块
  - 工作区上方的骰子点亮即可
- 若想批量操作，让选中的图块中随机选择几个图块进行绘制
  - 调整散布属性（图块默认概率为1，散布的值即为空白的概率
  - 如：散布值为2，那么空白:图块1:图块2:...=2:1:1:...）
- 若想调整图块与扩展图块间的优先级，可使用 TileMap 的图层功能
  - 新版 TileMap 因性能原因被弃用了，直接控制 TileMapLayer 节点树上的顺序即可（越下面的越靠前）
  - 检查器-Layers-添加元素为各个图层命名
  - 工作区上方右边选择对应图层
  - 切换对应图层即在地形编辑器的对应图层中绘制（所以叫做 TileMap 的图层功能）
  - 一般图层至少分为：背景、物理碰撞层、前景

## 视差背景

给予立体感的背景

- 在 World 根节点添加子节点 【ParallaxBackground】
- 在 【ParallaxBackground】 节点下添加子节点 【ParallaxLayer】 （即一个图层）
- 添加大背景（天空）
  - 摁住 Ctrl 键拖动图片至画布中，即将图片作为子节点添加到当前选中节点
  - 设置 【ParallaxLayer】 的相对移动速度，检查器 【Motion】 下的 【Scale】 属性
  - 此时仍然是一张图作为背景，可在 【Mirroring】 属性中编辑，即可在对应轴长度后自动进行拼接（无限长）
- 添加独立元素（树林）
  - 将图片拖入画布，若想取图片中的部分，如下
  - 打开 【Region】 属性，点击 【编辑区域】
  - 在 【区域编辑器】 中，吸附模式修改为 【栅格吸附】 ，将对应部分选中，拖动到想要的位置
  - 选中对应图片，摁住 Ctrl+D 进行复制，直至能将屏幕沾满（或者到你想要的长度）
  - 同上配置镜像效果，注意 【Scale】 属性配置稍大值（小于1）
  - BUG修复（截止至 Godot v4.4.1 仍未修复）：
    - 因为启用了图片【Sprite】节点的纹理区域(【Region】)
    - 目前版本这个功能与相机【Camera2D】的平滑移动有冲突
    - 会导致相机移动时在拼接处偶尔闪过白线
    - 规避方法是手动提取图片不使用区域功能，或者不要进行无缝拼接
- 若想添加前景
  - 将 【ParallaxBackground】 中 【CanvasLayer】 的 【Layer】 属性设置一个较大值（默认图层在0层，大于即可）
  - 将 【ParallaxLayer】 的 【Scale】 属性设置为大于1的值（比相机快）
- 配置好前景后景后，若不想误触
  - （可选）将前景后景放到一个节点下
  - 选中该节点，在画布上方工具栏中，激活【锁】和【编组】
  - 需要编辑时将【编组】取消即可选中

## 角色运动控制

编程控制角色运动

- 瞬时输入的（攻击、跳跃）放入 _unhandled_input
- 持续并且物理相关（移动）放入 _physics_process
- 非物理的操作（暂停、UI）放入 _process
- 逻辑实现流程（状态机）
  1. 获取输入 `want` （将输入视为意图），可以有不同入口
      - 设计时必须考虑清楚意图表达于输入之间的映射（摁下、激活、抬起、释放），后期修改影响面较大
  1. 状态更新（ `update_state()` ）
      - 状态的进入退出条件，优先用客观条件判断（根据自身的“状态”来判断处于何种状态）
  1. 状态的行为效果（ `tick()` ），使用意图条件判断是否增加额外的效果，可能会引起下一帧的状态更新
      - 效果：具体的影响，如修改移速、修改朝向等
      - 这里建议不根据情景各自实现，仅通过控制参数大小来作区分，意图与结果一致
  1. 状态的行为表现（ `play()` ），优先用客观条件判断
      - 表现：实际渲染的结果，播放的动画
      - 这里可根据不同情景做出较大差异化区分，并允许细分，如两个动作之间的过渡、不同速度奔跑等
  1. 物理计算（ `move_and_slide()` ）
      - 一帧仅有一次物理计算发生，若其所处中间位置，会导致分层状态机执行的逻辑歧义
      - 为了保证逻辑自洽，放至最后，效果和动画可能会有一帧延迟
- 编码规范：
  - 仅在 `_physics_process()` 中进行物理反应（ `move_and_slide()` ）
  - 速度的修改尽量平滑，使用 `move_toward(velocity.x, direction * speed, delta * acceleration)` 
  - want 判断放在主体内（ Player 类中）
  - can 判断放在状态内部
  - 状态下也可挂载状态机（分层状态机），若不分层则使用 `if` 语句，判断条件参考状态机


插入一些操作优化（参考 <https://www.youtube.com/watch?v=2S3g8CgBG1g> ）

- 快速下降：上升的重力加速度较小，下降时较大 `if (v < 0) { a -= v; }`
- 跳跃高度可控：
  - 松开时速度减少一半
  - 摁住松开时的重力加速度不同
- 限制最大下降速度
- 蹬墙跳
- 跳跃时子弹时间
- 额外滞空（竖直速度在+-0.1时重力减半）
- 峰值奖励（竖直速度在+-0.1时水平速度加速度增加）
- 视觉效果，动画拉伸，特效
- 跳跃力量（？）
- grace time (CoyoteTime)

- 部分动画允许打断操作会更流畅
- 空中的加速度 acceleration 可以较地面稍微大点，阻力 resistance 可以稍微小点
- 相似行为不同表现（不同速度奔跑、不同高度落下的过渡动画和后摇）
- CoyoteTime 郊狼时间（离开地面的一小段时间内仍然可以跳跃）
  - 注意：若容错时间在几帧内完成，可自己实现，这里认为自己实现代码会比较内聚
    - 因为 Timer 的准确度取决于渲染帧率或物理帧率，一般不建议设置小于 0.05s 的时间
    - 容错时间参考 60 帧，每帧 0.016s ，人平均反应速度在 220-240ms 之间，实测 0.1 左右是比较好的
  - 在 Player 节点下添加 Timer 节点
  - 检查器中 【WaitTime】 修改成较小值 如 0.1s
  - 启用 【OneShot】 令其只倒计时一次
  - 代码中触发条件为在 move_and_slide 前后对比 is_on_floor 函数的值是否改变，注意排除主动跳跃的情况
    - 侧面说明 is_on_floor 是一个实时计算的结果，在同一帧中可以实时计算
- 允许到地面前的一小段时间内摁下跳跃键，在接触地面后直接跳跃
  - 在 _unhandled_input 方法中启动计时
- 通过跳跃键的摁住时长控制跳跃高度
  - 在 _unhandled_input 方法中
  - 松开按键时提前设置垂直速度为跳跃速度的一半（正常是重力逐渐改变）
  - 注意与上面的计时器联动易产生BUG：松开时需要停止计时器（面向过程编码时容易遇到这种问题）
- 滑行加速但是转向慢，需要松开加速才能快速转向
- 连招
  - 在脚本中添加导出变量 can_combo
  - 动画播放器中将该变量加入关键帧

动画状态机，可能需要根据环境来判断播放哪种动画，如手部脚部碰撞检测

- 因为手部方向与人物方向是耦合的，因此把 【Sprite2D】 节点挂在单独的节点下
  - 节点树的 【Sprite2D】 节点右键 【重设父节点为新节点】 新建 【Node2D】 节点，命名 Graphics
  - 代码逻辑中控制 【Graphics】 节点的翻转来控制人物的朝向翻转
- 在 【Graphics】 节点下新增子节点 【RayCast2D】 节点，射线碰撞检测
- 脚本中使用方法 `ray_cast.is_colliding()` 判断是否有物理碰撞

## 敌人AI

- 大部分逻辑与角色控制相同
- 玩家检测同样可用 【RayCast2D】 节点进行碰撞检测
  - 需要注意碰撞属性，同时建议配置不同碰撞层的名称
    - 【CollosionLayer】 配置物体位于哪个碰撞层上（被碰撞检测）
    - 【CollosionMask】 配置物体能与哪个碰撞层的物体碰撞
  - 需要注意脚本中进行翻转后 `ray_cast.is_colliding()` 方法返回的仍然为之前的值
    - 可能是引擎做的缓存，也可能是此时仅仅设置了翻转属性实际还未生效
    - 使用方法 `ray_cast.force_raycast_update()` 强制在一帧内刷新
  - 一般模拟视线检测需要同时判断环境层和玩家层两个碰撞层，然后通过 is 关键字来判断看到的是墙还是玩家

## 攻击判定

攻击判定框 Hitbox 受击判定框 Hurtbox

- 脚本类判定框继承自 Area2D 节点
- Hitbox 中有信号 `signal hit(hurtbox)`
- Hurtbox 总有信号 `signal hurt(hitbox)`
- 在自定义方法中使用 `signal.emit(xx)` 发送信号
- 在初始化方法 `_init()` 中使用 `area_entered.connect(func)`
  - 将自定义方法作为信号回调方法链接至 area_entered 信号
- 在敌人玩家 【Graphics】 节点下添加攻击框和受击框类
  - 配置 Hitbox 对应的碰撞层（参考配置：不位于任何层，检测受击层；玩家和敌人的层可以分开，看业务逻辑）
  - 配置 Hurtbox 的碰撞层，与上面参考配置相反
  - 在 Hitbox 节点下添加 CollisionShape2D 节点来实际进行碰撞检测（可以添加多个来组成复杂形状）
  - 连招场景下需要配置多个攻击框，通过 CollisionShape2D 节点的 Disabled 属性控制是否碰撞
    - 编辑攻击框形状时可能会影响其他攻击框
      - CollisionShape2D 的 Shape 属性是 RectangleShape2D 资源，而资源在复制节点时仍然是共享的
      - 属性右侧下拉框，选择【唯一化】即可
- 处理受伤信号（连接信号的另一种方法）
  - 点击 Hurtbox 在右侧选中节点页签
  - 在信号中双击 hurt 信号
  - 将信号连接至角色的主节点（自动在脚本里创建接收方法）

## 受伤和死亡

- 创建新类 Stats ，继承自 Node
- 将属性 max_health 设置为 @export 允许导出给节点设置
- 将属性 health 设置为 @onready 将该属性的初始化延后到 @export 之后
- 可选：给 health 变量配置 `set(v)` 方法 `v = clampi(v, 0, max_health)` 限制 health 变量的上限
  - 注意函数里面的 i 是 int 的意思
- 在受伤信号回调方法中，进行扣血计算，最后调用 `queue_free()` 将节点删除
- 受伤动画中修改 Hitbox 的 Area2D 下的 Monitoring 属性，临时取消攻击效果
- 死亡动画中修改 Hurtbox 的 Area2D 下的 Monitorable 属性，取消受伤效果
- 死亡动画可用 CanvasItem 的 Visibility 下的 Modulate 属性达到淡出效果
- 可选：死亡动画最后调用方法清理节点
  - 动画添加轨道，选择【方法调用】，选择对应角色
  - 在最后添加关键帧，选择对应 `die()` 方法

若在受伤信号回调方法中直接修改状态，则状态机的功能不够聚焦，建议回调方法中仅记录收到伤害

- 创建新类 Damage ，继承自 RefCounted （更底层的就需要手动管理内存了）
- 属性 `amount: int` 意味收到的伤害，属性 `source: Node2D` 记录伤害来源
- 角色脚本添加属性 `pending_damage: Damage` 记录待处理属性，也可以改造成数组

## 状态面板

- 创建空场景
- 根节点创建为 HBoxContainer 是一个将子控件横向排列的容器
- 可选：修改 Control 下的 Transform 的 Size 为 0 ，让内容将他撑起来
- 头像
  - 增加 TextureRect 节点显示头像
  - 将 Texture 设置为 AtlasTexture 图集纹理
    - 允许将图片视为图集然后从中选择区域，因为该节点原生不支持区域选择
  - 从人物动作中将头像裁剪
  - 将 TextureRect 【重设父节点为新节点】为 PanelContainer 是专门为控件提供背景的容器
  - 将 Control 下的 ThemeOverrides-Styles-Panel 设置 StyleBoxTexture
  - 展开并拖入素材 HUD
  - 编辑子区域
  - 现在已经有了基础的效果，但是背景和头像的像素大小不对应
    - 因为根节点的内容还是被头像撑起的，然后才是背景根据大小自动缩放
  - 手动将 PanelContainer 的 Layout 下的 CustomMinimumSize 调整为和头像像素一致
  - 现在背景将根节点撑大，但是同时导致头像也被放大了
  - 调整 TextureRect 的 StretchMode 为 KeepAspectCentered ，保持长宽比缩放并居中
  - 调整 PanelContainer 的 ThemeOverrides-Styles-Panel 中的 ContentMargins 设置容器与内容的间距
- 血条
  - 根节点新建子节点 TextureProgressBar
  - 属性 Textures 下的 Under 可用作背景、 Over 用作边框、 Progress 用作进度条
    - ProgressOffset 设定偏移量用于边框等对齐
  - 同样选择 AtlasTexture 设置素材
  - 修改 Range 下的 Value 使其显示
    - 将 MaxValue 设为 1 ，将 Step 设为 0 ，这样 Value 可设置为浮点数，较为丝滑
  - 调整 TextureProgressBar 的 Control 的 Layout-ContainerSizing-Vertical 为【居中收缩】
  - 编写脚本 `@export var stats: Stats` 用于让外界传入
  - 在 Stats 类中增加信号，每次修改时发送信号
  - 在血条脚本中 `_ready()` 方法中对信号进行连接
- 血条扣血动画
  - 复制血条设为原来的子节点，命名 EasedHealthBar
  - 调整 Progress 唯一化并选择另一个素材
  - 使用画布工具栏靠右的【锚点预设】选择【整个矩形】，这样就能以其父节点进行定位
  - 调整 CancasItem 下的 Visibility-ShowBehindParent 让其在父节点后面绘制
  - 脚本中的血量更新方法中进行补间动画
    - `create_tween().tween_property(eased_health_bar, "value", percentage, 0.3)`
    - 其中 `percentage` 是目标值，即扣血后的血量
- 角色挂载状态面板
  - 实例化子场景，在检查器指定刚刚导出的变量 stats 为对应的属性
  - 现在面板会跟随玩家角色移动（敌人的血条也可以类似操作）
- 若想让面板固定在屏幕左上角
  - 选定面板子场景右键【重设父节点为新节点】选择 CanvasLayer
  - 在画布上调整位置即可