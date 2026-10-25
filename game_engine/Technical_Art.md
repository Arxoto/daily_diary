# 游戏技术

## 2D 基础美术

https://www.bilibili.com/video/BV1Z1B5BaEGE/ or https://www.youtube.com/watch?v=au9pce-xg5s

- 景深 DepthOfField （背景模糊强调主角）
- 粒子 Particles （尘埃、树叶、光晕）
- 泛光 Bloom （后处理更有质感）

如何去除色彩断层（颜色变化不平滑，类似于 Jpeg 图片压缩）

1. 保证材质本身无色彩断层
1. 像素抖动（如仅黑白像素，通过调整像素分布方式来模拟不同的灰度）
   - Bayer 抖动（经典的风格化抖动，修复色彩断层效果较差，适合给游戏做风格化艺术处理）
   - Floyd-Steinberg 抖动（计算成本过高）
   - InterleavedGradientNoise IGN 交错梯度噪声（配合模糊一起使用）
     - shader `ign = frac(52.9829189 * frac(Screen_xy * <0.06711056, 0.00583715>))`

不同的抖动算法 see https://blog.demofox.org/2022/01/01/interleaved-gradient-noise-a-different-kind-of-low-discrepancy-sequence/

## 3D 植被-草&树

https://www.bilibili.com/video/BV1TeBrBREyA/

草

- 一株草是一片贴图
- 一堆草是多片贴图的组合，这里描述如何进行批量组合

1. 草的法线统一向上，光照更柔和（塞尔达传说里面的草）
1. 随机旋转、位置、适当提高密度
1. 着色器
   - 使用噪点图映射到灰度图使草具有多种随机的颜色
   - 风吹效果则使用滚动的纹理（并且用它来驱动顶点位移，纹理图必须平滑无缝）
1. LOD 远处模型替换低细节版本

树

- 复数的树叶是一片贴图
- 一棵树的树叶是多个交错的树叶贴图

1. 树叶的法线背离树冠中心向外（内部不会有错乱光影）
1. 隐形物体投影阴影，关闭树叶本身阴影（光照更平滑）
1. 树叶开启双面渲染（更茂盛，一般多面体的背面是不可见的，因为看不到）
1. 计算叶片和镜头夹角，制作淡出（侧视角下去除生硬边缘）
