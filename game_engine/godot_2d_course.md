# Godot 4 教程《勇者传说》

from https://www.bilibili.com/video/BV1Z94y1V74m

基于 Godot v4.4 的一个像素风横板动作游戏制作指南

todo 总结 [肖老师的Godot实验室](https://gdbook.kidsgame.top/%E7%AC%AC%E5%85%AB%E7%AB%A0/ch08/)

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
  - 工作区的上方右侧调整总长度和打开循环（一般像素风格一帧持续 0.1s ，下方的吸附选择 0.1s ）
  - 切换到【Sprite2D】节点，将一下属性新建轨道并插入关键帧
    - Region-Rect 因为不同动画的区域范围可能会不一样
    - Animation-Hframes 因为不同的动画（动作集）的Hframes可能会不一样
    - Frame 需要将对应动作帧依次加入，注意工作区的下面【吸附】调整对应的每帧时间，像素游戏可以0.1秒1帧
    - 注意要保持所有动画的轨道一致，不然会有状态残留导致各种BUG
      - 在 4.2+ 的版本中，能开启 AnimationPlayer-AnimationMixer-Deterministic 属性，混合使用确定性算法
      - 开启后，默认使用 "RESET" 动画来对缺少的轨道动画赋值
      - 特别的，对于循环动画， "RESET" 动画不起作用，原因未知，暂手动赋值处理
        - 参考 https://github.com/timothyqiu/godot-animation-resetter/tree/master 解决，但是使用过程中引擎会有绘图相关代码报错，应该是修改了原生界面导致
  - 若想自己实现上半身下半身动画分离
    - 创建两个 Sprite2D 角色，两个 AnimationPlayer 分别挂在其子树下，并分别控制
    - 现成的方案是使用 AnimationTree 还有 AnimationNodeBlendTree
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
    - 如控制 Sprite2D 的 flip_h 属性控制水平翻转 `sprite_2d.flip_h = want_move_direction < 0`
      - 高级点的方法：将一个 Node2D 作为 Sprite2D 的父节点，修改其 Transform-Scale-x 属性控制翻转
      - `body.scale.x = -1.0 if want_move_direction < 0 else 1.0`
      - 注意：修改路径后启动游戏可能会警告 "AnimationMixer couldn't resolve track" ，重启 godot 即可解决
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

- 若启用相机平滑后，人物移动出现模糊抖动，解决办法有两个（建议一起打开，物理插值在新版是推荐的）
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

- 瞬时输入的（攻击、跳跃）放入 _unhandled_input 同一渲染帧中最先执行
- 持续并且物理相关（移动）放入 _physics_process 同一渲染帧中其次执行，并且执行后物理帧加一
- 非物理的操作（暂停、UI）放入 _process         同一渲染帧中最后执行
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
  - 需要注意碰撞属性，同时建议配置不同碰撞层的名称【 CharacterBody2D-CollisionObject2D-Collision 】
    - 【CollosionLayer】 配置物体位于哪个碰撞层上（被碰撞检测）
    - 【CollosionMask】 配置物体能与哪个碰撞层的物体碰撞
    - 建议 1 命名为 Environment ； 2 命名 Player ； 3 命名 Character （中立生物或敌人）; 4 命名 Hurtbox ；
    - 注意物体碰撞和射线检测需要一起调整
  - 需要注意脚本中进行翻转后 `ray_cast.is_colliding()` 方法返回的仍然为之前的值
    - 可能是引擎做的缓存，也可能是此时仅仅设置了翻转属性实际还未生效
    - 使用方法 `ray_cast.force_raycast_update()` 强制在一帧内刷新
  - 一般模拟视线检测需要同时判断环境层和玩家层两个碰撞层，然后通过 is 关键字来判断看到的是墙还是玩家

## 攻击判定

攻击判定框 Hitbox 受击判定框 Hurtbox

- 脚本类判定框继承自 Area2D 节点
- Hitbox 中有信号 `signal hit(hurtbox)`
- Hurtbox 中有信号 `signal hurt(hitbox)`
- 新建自定义方法 `on_area_entered(hurtbox: HurtBox)` 使用 `signal.emit(xx)` 发送信号
- 在初始化方法 `_init()` 中使用 `area_entered.connect(on_area_entered)`
  - 将自定义方法作为信号回调方法链接至 `area_entered` 信号，这样当 Area2D 碰撞时会自动发送 hit/hurt 信号
  - 一般信号发送只在一个里实现，这里仅在 Hitbox 中实现
- 在敌人玩家 【Graphics】 节点下添加攻击框和受击框类
  - 若想实现部位伤害需要同时创建多个判定框，其中仅一个受击框负责处理伤害，其他受击框负责专门处理部位伤害效果
  - 配置 Hitbox 对应的碰撞层（建议攻击框范围较为准确）
  - 配置 Hurtbox 的碰撞层，与上面参考配置相反（建议受击框根据难度调整，如玩家较小、敌人较大）
  - 参考 Hitbox 的 Area2D.Monitorable=false CollisionObject2D.Layer=null CollisionObject2D.Mask=4
  - 参考 Hurtbox 的 Area2D.Monitoring=false CollisionObject2D.Layer=4 CollisionObject2D.Mask=null
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
- 可选：修改 Control-Leyout-Transform 的 Size 为 0 ，让内容将他撑起来
- 头像
  - 增加 TextureRect 节点显示头像
  - 将 Texture 设置为 AtlasTexture 图集纹理
    - 允许将图片视为图集然后从中选择区域，因为该节点原生不支持区域选择
  - 从人物动作中将头像裁剪
  - 将 TextureRect 【重设父节点为新节点】为 PanelContainer 是专门为控件提供背景的容器
  - 将 Control 下的 ThemeOverrides-Styles-Panel 设置 StyleBoxTexture
  - 双击展开并拖入素材 HUD
  - 编辑子区域
  - 现在已经有了基础的效果，但是背景和头像的像素大小不对应
    - 因为根节点的内容还是被头像撑起的，然后才是背景根据大小自动缩放
  - 手动将 PanelContainer 的 Layout 下的 CustomMinimumSize 调整为和头像像素一致
  - 现在背景将根节点撑大，但是同时导致头像也被放大了
  - 调整 TextureRect 的 StretchMode 为 KeepAspectCentered ，保持长宽比缩放并居中
  - 调整 PanelContainer 的 ThemeOverrides-Styles-Panel 中的 ContentMargins 设置容器与内容的间距
  - 分别重命名为 AvatarBox 和 Avatar
- 血条
  - 根节点新建子节点 TextureProgressBar
  - 属性 Textures 下的 Under 可用作背景、 Over 用作边框、 Progress 用作进度条
    - ProgressOffset 设定偏移量用于边框等对齐
  - 同样选择 AtlasTexture 设置素材
  - 修改 Range 下的 Value 使其显示
    - 将 MaxValue 设为 1 ，将 Step 设为 0 ，这样 Value 可设置为浮点数，较为丝滑
  - 调整 TextureProgressBar 的 Control 的 Layout-ContainerSizing-Vertical 为【居中收缩】
  - 将 TextureProgressBar 重命名为 HealthBar
  - 根节点添加脚本，将 HealthBar 拖入， `@export var stats: Stats` 用于让外界传入
  - 新建方法 update 修改 HealthBar 的值为实际值
  - 在 Stats 类中增加信号，每次修改时发送信号
  - 在血条脚本中 `_ready()` 方法中对信号进行连接
- 血条扣血动画
  - 复制血条 HealthBar 设为原来的子节点，命名 EasedHealthBar
  - 调整 Progress 唯一化（右边箭头下拉）并选择另一个素材
  - 使用画布工具栏靠右的【锚点预设】选择【整个矩形】，这样就能以其父节点进行定位
  - 调整 CancasItem 下的 Visibility-ShowBehindParent 让其在父节点后面绘制
  - 脚本中的血量更新方法中进行补间动画
    - 直接在 update 方法中 `create_tween().tween_property(eased_health_bar, "value", percentage, 0.3)`
    - 其中 `percentage` 是目标值，即扣血后的血量
- 能量条
  - 将血条右键，重设父节点为新节点，选择 VBoxContainer 节点，将子节点垂直排列
  - 新增能量条，略
  - 修改 VBoxContainer 的 BoxContainer 下的 Alignment 为 Center 将内容垂直居中
  - 调整 VBoxContainer 的 Control 下的 ThemeOverrides-Constants-Separation 修改内容间距
- 角色挂载状态面板
  - 在角色场景中，实例化子场景，在检查器指定刚刚导出的变量 stats 为对应的属性
  - 现在面板会跟随玩家角色移动（敌人的血条也可以类似操作）
- 若想让面板固定在屏幕左上角
  - 选定面板子场景右键【重设父节点为新节点】选择 CanvasLayer
  - 在画布上调整位置即可

## 可交互对象

- 本质还是区域碰撞，和信号触发，类名称 Interactable 继承自 Area2D
  - 属性 `signal interacted`
  - 方法 `_init()` 中将 collision_layer 和 collision_mask 先置零
  - 然后重新设置碰撞层 `set_collision_mask_value(2, true)` ，碰撞层是位变量，玩家碰撞层在2
  - 方法 `_init()` 中 `body_entered.connect(_on_body_entered)` 和 `body_exited.connect(_on_body_exited)`
  - 进入离开信号的触发函数对应逻辑为将自身注册/注销至玩家交互列表中
  - 玩家交互键时触发交互列表的最后一项，调用 Interactable 类的自定义方法 `interact()`
  - 自定义方法 `interact()` 默认激活信号 `interacted.emit()`
- 交互提示使用 AnimatedSprite2D 节点
  - 在 AnimatedSprite2D 下的 Animation-SpriteFrames 新建 SpriteFrames
  - 在下方动画帧中，工具栏“从精灵表中添加帧”
  - 在案例中，调整区域分布为 16*16 恰好一个按钮一个方格
  - 按照顺序点击对应按钮图标
  - 工具栏左侧的【动画】中，将自动播放打开即可

## 场景切换

- 新建场景切换专用传送类 Teleporter 继承自 Interactable
- 覆盖父类方法 `interact()` 并 `super()` 调用父类方法
  - 切换场景的逻辑 `get_tree().change_scene_to_file(path)`
- 导出变量 `@export_file("*.tscn") var path: String`
- 新建场景，根节点为 Teleporter ，并加入门素材（精灵）、碰撞箱（CollisionShape2D）

此时最简单的场景切换完成，若需指定切换场景后的起始位置，如下操作

- 创建脚本继承自 Marker2D （和 Node2D 类似，但是十字准星较大），类名 EntryPoint
- 方法 `_ready()` 中 `add_to_group("entry_points")` 加入分组方便查找
- 传送类 Teleporter 导出变量 `@export var entry_point: String` ，用于指定世界场景中的 EntryPoint 实例名称
- World 类中添加方法修改玩家角色的位置 `player.global_position = pos` 和 `player.fall_from_y = pos.y`
  - 为防止角色瞬移导致相机移动 `camera_2d.reset_smoothing()` 和 `camera_2d.force_update_scroll()`
- 注意 `change_scene_to_file` 方法是有延后的（先从场景树上摘下，延后销毁），因此不能直接在方法后调用，需要做下面调整
  - （也无法await，因为此时场景已经刷新了，对应的逻辑仍在旧场景内）
- 因此需要专门切换场景的场景
  - 添加场景 Game 根节点 Node （非 Node2D 因为是比较通用的类型）
  - 添加脚本，具体如下

    ```GDScript
    func change_scene(path: String, entry_point: String) -> void:
      var tree := get_tree()
      tree.change_scene_to_file(path)
      await tree.tree_changed # 等待场景切换信号

      for node in tree.get_nodes_in_group("entry_points"):
        if node.name == entry_point:
          tree.current_scene.update_player(node.global_position)
          break
    ```

  - 而后项目设置【自动加载】添加 game.tscn （注意右侧全局变量是启用状态）
  - 修改 Teleporter 类中的 `interact()` 方法 调用刚刚创建的 Game 场景
    - `Game.change_scene(path, entry_point)`
  - 若要调整玩家初始朝向
    - EntryPoint 添加导出变量设置朝向
    - World 脚本内 `await player.ready` 后修改默认朝向
      - (教程中是将朝向作为导出变量，变量的 `set(v)` 方法中直接 `if not is_node_ready(): await ready` 的)
  - 保持玩家状态
    - 将 State 节点粘贴到 Game 中作为全局变量，然后 Player 中对其的引用修改为 `Game.player_stats`
    - 将 StatusPanel 中取消导出变量，也同样使用全局变量
    - 此时刷新场景会有扣血补间动画，在对应的 update 方法中添加默认参数允许跳过补间动画

转场效果，淡入淡出

P.S. 另有一种基于 Shader 的转场，参考 https://www.bilibili.com/video/BV1ka4y1W757/

- Game 场景中添加节点 ColorRect ，上方工具栏调整色块锚点预设为整个屏幕，并调整颜色黑色
- ColorRect 父节点 CanasLayer 并设置 Layer 为 999
- Game 脚本中 ready 方法 `color_rect.color.a = 0`
- Game 脚本中 change_scene 方法

  ```GDScript
  tree.paused = true # 暂停世界

  var tween := create_tween()
  tween.set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)
  tween.tween_property(color_rect, "color:a", 1, 0.2)
  await tween.finished

  # change_scene
  tree.paused = false
  # new tween "color:a" to 0
  ```

## 暂存状态

本质是将部分可保存数据保存在全局变量中

- 在 Game 脚本中添加变量 `world_states` 存放场景名称到具体数据之间的映射
- 获取场景名称 `tree.current_scene.scene_file_path.get_file().get_basename()`
- 在场景脚本，如 World 中，编写方法 `to_dict()` 和 `from_dict()`
- 将所有敌人在 `_ready()` 中 `add_to_group("enemies")` 加入到场景树的分组
- 由于敌人一般是一个独立的场景，也可以在场景的根节点中，右侧检查器旁边“节点”面板的“分组”中添加对应分组名称
- 在 World 脚本 `to_dict()` 中， `get_tree().get_nodes_in_group("enemies")` 并对其进行遍历，其中每个元素是一个节点 node
- 在 World 脚本 `to_dict()` 中， `get_path_to(node) as String` 将节点转换为为路径，用于仍然存活的敌人的标识
- 在 World 脚本 `from_dict()` 中，若敌人不存在则 `node.queue_free()` 从场景树中释放即可

注意，切换场景 `tree.change_scene_to_file(path)` 机制是先从场景树上摘下，延后销毁

在场景树上摘下后但未销毁之间，信号仍然存在，但信号内的执行逻辑可能会失败，需要注意信号“残留”的问题

- 如切换场景时修改玩家血量
- 若完全跟着视频教程来的话，可能在 `_ready()` 方法中 `stats.health_changed.connect(update_health)`
- 由于修改血量的同时会 `create_tween()` 创作扣血的补间动画
  - 依赖场景树，当脱离场景树时返回空，因此会失败
- 为防止这种问题，需要将信号连接断开

  ```GDScript
  # in func _ready()
  tree_exited.connect(func ():
    stats.health_changed.disconnect(update_health)
  )
  ```

## 存档&读档

本质是将上一章节《暂存状态》中的数据进行序列化和反序列化的过程

- 在 Game 脚本中添加变量用作存档文件 `const SAVE_PATH := "user://data.sav"`
- 实现存档函数 `func save_game()` 将 `world_states` （注意先刷新状态）、当前场景路径、玩家状态、玩家朝向和位置存入字典
- 存档逻辑如下

  ```GDScript
  var json := JSON.stringify(data)
  var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
  if not file:
    return
  file.store_string(json)
  ```

- 读档逻辑如下

  ```GDScript
  var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
  if not file:
    return
  var json := file.get_as_text()
  var data := JSON.parse_string(json) as Dictionary
  ```

## 存档点

逻辑上本质就是调用存档方法，这里主要记录存档点的效果制作流程

- 激活状态（已存档）的灯光效果
  - 场景添加 PointLight2D 节点（本质是一个贴图）
  - 在 PointLight2D 的 Texture 属性，新建 GradientTexture2D 并展开
    - 将 Fill 属性修改为 Radial
    - 打开网格吸附，将黑点放至图片中心，将白点放至任意一边的中点
    - 展开 Gradient 属性，点击第一行左下角的按钮，进行黑白的颠倒
    - 如此就完成了模拟灯光的效果
  - 通过调整 PointLight2D 的 TextureScale 调整灯光范围
  - 通过调整 PointLight2D-Light2D 的 Color 和 Energy 属性调整灯光颜色和亮度
- 使用 AnimationPlayer 节点控制存档点的激活/未激活两个动画的播放
  - 激活时动态效果，调整动画循环播放，并将亮度加入关键帧，并修改差值模式为三次方
- 注意，若 AnimationPlayer 修改了物理相关（如对可交互碰撞区域进行开关动作）
  - 需要在 AnimationPlayer-AnimationMixer 下的 CallbackMode-Process 修改为 Physics

P.S. 若想强调灯光效果（环境昏暗），可在场景下添加子节点 CanvasModulate 节点，并将其 Color 属性调暗

这里再补充一个常见的后处理效果（暗角）

- 新建空场景，创建根节点为 CanvasLayer 改名为 Vignette
- 新建子节点 ColorRect ，锚点预设占据整个屏幕
- 在 ColorRect-CanvasItem 下的 Meterial 新建 ShaderMaterial
  - Shader 属性新建着色器
  - 然后可以自己编写着色器，一般可在 <https://godotshaders.com/> 获取现成的（搜索 Vignette ）
  - 在编辑器 Shader 下的 ShaderParameters 修改统一变量 uniform 可自定义效果
- 保存场景在 globals 文件夹下
- 项目设置中，自动加载添加暗角效果（一般无需代码中引用的话取消全局变量）
- 调整场景可见性验证效果
- 调整 Vignette 节点的 CanvasLayer 下的 Layer 将层级调高（一般顺序为 UI -> HUD -> S   hader -> 游戏内容）

## 标题界面

本质是 UI 界面

这里先简单介绍锚点系统

- （试用）项目设置-显示-窗口，将拉伸-比例修改为 expand
  - expand 为等比例缩放，并且宽或长超出部分会自动扩展，而 keep 模式会用黑边遮住
  - 不同的拉伸模式会影响 UI 布局，使用锚点系统（控件节点）能够确定布局
- 在控件节点中 Control 下的 Layout-AnchorsPreset 修改为自定义，会显示三组自定义属性
  - 锚点     AnchorPoints  锚点区域为四个大头针确定的区域，上下左右四个属性为四边在父节点的百分比位置
  - 锚点偏移 AnchorOffsets 根据锚点区域进行偏移，单位像素，确定控件本身的位置
  - 伸长方向 GrowDirection 若锚点和偏移的范围仍然比控件本身小，由此推断控件如何扩展

制作标题界面

- 新建空场景，根节点为 用户界面 ，重命名为 TitleScreen ，场景保存至 ui 文件夹
- 新建子节点 Label ，调整 Text 属性为游戏标题，修改 HorizontalAlignment 为 Center 以居中文字
- 自定义字体
  - 单个控件自定义：在 Label-Control 的 ThemeOverrides-Fonts 将字体文件拖入
  - 跟随父节点主题：在 Label-Control 的 Theme 修改对应主题，最上层为项目设置-GUI-主题-自定义主题
  - 视频教程中使用得意黑 <https://atelier-anchor.com/typefaces/smiley-sans>
- 自行添加各种按钮
  - 若发现无点击效果，打开下方【调试器-其他】，发现点击控件为 Game-ColorRect （后面还有 Vignette 也一样操作）
  - 调整该节点的 Control 下的 Mouse-Filter 为 ignore
- 调整按钮的统一主题
  - 根节点 Control 的 Theme 新建主题，下拉框保存为文件，点击可打开主题编辑器
  - 拖入字体
  - 主题编辑器的右侧添加类型 Button
  - 切换到样式盒选项卡（自己玩一下）
  - 将聚焦样式（键盘控制下的聚焦效果）添加新建 StyleBoxTexture （其余选择 Empty ）
  - 将 HUD 素材拖入并选择区域
    - 若要调整拉伸规则，可关注四条黑白虚线，他们框定的区域控制着如何拉伸（角落不拉伸，边横向纵向拉伸，内部拉伸）
  - 开始时自动键盘聚焦：在根节点添加脚本，开始时自动将某一个按钮 `any_button.grab_focus()`
  - 鼠标移动也显示聚焦：对按钮容器进行遍历 `button.mouse_entered.connect(button.grab_focus)`
  - 按钮功能：在场景树中选中按钮，右侧节点-信号，双击 `pressed()` ，创建连接
    - 退出游戏使用 `get_tree().quit()`

## 音乐和音效

- 使用节点 AudioStreamPlayer 并将音频文件拖入 Stream 属性
- 脚本中使用 `audio_player.play()` 进行播放
- 可使用一个独立的子场景专门管理音效播放
  - 音效：统一放在 SFX 子节点下
  - 背景音乐：使用 BGM 名称的音频播放器去承载，并且在编辑器左侧，“场景”页签的右侧“导入”，启用循环并且重新导入
- 若想世界暂停时，音乐不受影响，可修改 Node 下的 Process-Mode 为 Always （始终进行处理）

音量滑块，音效和音乐独立控制音量

- 下方工作区音频，添加总线，然后多选音效，统一修改属性 Bus 为刚刚新建的总线
- 代码中使用 AudioServer 类去对总线进行管理

  ```GDScript
  func get_volume(bus_index: int) -> float:
    var db := AudioServer.get_bus_volume_db(bus_index)
    return db_to_linear(db) # 分贝的单位非线性，而音量调整一般为线性

  func set_volume(bus_index: int, v: float) -> void:
    var db := linear_to_db(v)
    AudioServer.set_bus_volume_db(bus_index, db)
  ```

- 编写配置项持久化（使用 ini 文件）
  - 使用 `ConfigFile.new()` 和 `config.set_value("section", "key", "value")` 进行赋值
  - 使用 `config.save(path)` 保存配置文件
  - 使用 `config.load(path)` 加载配置文件（可能失败，但是由于 get 方法有默认值，因此无需担心）

## 震屏和顿帧

震动屏幕提升打击感
- 另外可配合镜头缩放 `zoom` 属性

```GDScript
# global
@export var recovery_speed := 16.0
var strength := 0.0

# in camera process/physics_process
offset = Vector2(randf_range(-strength, strength), randf_range(-strength, strength))
strength = move_toward(strength, 0, recovery_speed * delta)

# in camera ready
# 将震动强度关联至一个全局节点的信号
```

减缓游戏世界时间模拟卡肉，提升打击感

```GDScript
Engine.time_scale = 0.01
await get_tree().create_timer(0.5, true, false, true).timeout
Engine.time_scale = 1.0
```

## 导出游戏

### 安装导出模板

左上角：【编辑器】-【管理导出模板】

点击【下载并安装】即可（或者【从文件安装】选择对应tpz文件）

### 导出项目

左上角：【项目】-【导出】

上方【添加】，选择对应平台

（可选）解决下方黄色警告（如想要修改图标则需要设置 rcedit 路径）

下方按钮【导出项目】，注意发布版本取消勾选【使用调试导出】

注意管理产物，保存的路径参考 `./build/windows/xxx.exe`
