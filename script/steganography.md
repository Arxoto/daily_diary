# Steganography 隐写术

定义：将秘密信息隐藏在其他载体中的技术，如图片中隐藏的水印等，高级点的还能抵抗压缩、裁剪、旋转等变形操作

## 数据直接嵌入图片文件的末尾

```cmd
copy /b "图片.jpg" + "压缩包.zip" "生成目标.jpg"
```

一般用视频文件比较合适，因为一般视频文件较大，推荐的伪装视频时长如下

```
400-500 MB -> 15-30 min
1-3 GB -> 1h
3-4 GB -> 2h
```

## 现成项目

https://github.com/rippod/apate/blob/main/apate/Program.cs

