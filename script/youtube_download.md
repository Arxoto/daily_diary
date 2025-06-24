# yt-dlp

https://github.com/yt-dlp/yt-dlp

## 最佳实践

登录 https://www.youtube.com/

```
# 最优画质音质下载 推荐登录并使用参数 --cookies-from-browser chrome
yt-dlp --proxy socks5://127.0.0.1:7897 -o "D:\Downloads\%(title)s-%(id)s-%(height)sp.%(ext)s" https://www.youtube.com/watch?v=video_id

# 最优画质音质下载 中文字幕合并
yt-dlp --proxy socks5://127.0.0.1:7897 --write-subs --sub-langs zh --embed-subs -o "D:\Downloads\%(title)s-%(id)s-%(height)sp.%(ext)s" https://www.youtube.com/watch?v=video_id

# 最优画质音质下载 中文字幕分离
yt-dlp --proxy socks5://127.0.0.1:7897 --write-subs --sub-langs zh -P "D:\Downloads" -o "%(title)s-%(id)s-%(height)sp.%(ext)s" -o "subtitle:%(title)s-%(id)s.%(ext)s" https://www.youtube.com/watch?v=video_id

# 手动选择画质和字幕
yt-dlp --proxy socks5://127.0.0.1:7897 --list-formats https://www.youtube.com/watch?v=video_id
yt-dlp --proxy socks5://127.0.0.1:7897 --list-subs https://www.youtube.com/watch?v=video_id
yt-dlp --proxy socks5://127.0.0.1:7897 -f "___ID___+___ID___" --write-subs --sub-langs zh -P "D:\Downloads" -o "%(title)s-%(id)s-%(height)sp.%(ext)s" -o "subtitle:%(title)s-%(id)s.%(ext)s" https://www.youtube.com/watch?v=video_id

```

## 默认下载

默认的格式参数为 `-f "bv*+ba/b"` ，意为下载最佳视频音频组合

```
yt-dlp <video_url>
```

## 手动选择下载

查看可供下载的资源列表

```
yt-dlp --list-formats <video_url>
```

输出

```
ID      EXT   RESOLUTION FPS CH │   FILESIZE   TBR PROTO │ VCODEC          VBR ACODEC      ABR ASR MORE INFO
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
251     webm  audio only      2 │  458.49MiB  110k https │ audio only          opus       110k 48k medium, webm_dash
605     mp4   640x360     30    │ ~  1.96GiB  483k m3u8  │ vp09.00.21.08  483k video only
243     webm  640x360     30    │  378.68MiB   91k https │ vp9             91k video only          360p, webm_dash
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
资源ID        分辨率          ？              码率         视频编码格式        音频编码格式     ？
        扩展名          帧率        文件大小       流媒体协议         视频码率        音频码率
```

手动指定下载资源，其中 `"资源ID"` 可改为 `"资源ID+资源ID"` 的形式下载，并自动选择合适的容器封装技术来存储视频、音频流

```
yt-dlp -f "资源ID" <video_url>
```

常用的优先格式下载

```
# 最佳视频流 和 最佳音频流
yt-dlp -f "bv+ba/b" <video_url>

# 下载指定分辨率的mp4视频
yt-dlp -f "bv[height=720][ext=mp4]+ba[ext=m4a]/b" <video_url>
```

## 格式参数的说明

更多的 `-f` 参数说明，参考 yt-dlp 官方文档： [format-selection-examples](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#format-selection-examples)

不设置 `-f` 时，其默认值是 `-f "bv*+ba/b"` 全称 `"bestvideo*+bestaudio/best"`

> bv*+ba/b 获取「最佳视频流」和「最佳音频流」，合并为最终视频，相比于 "bv+ba/b"，前者不仅限于 Video Only，只要是 Video 就可以，不局限于单一的 “最佳”，在某些情况下会选择一个更合适的流，特别是在不同的编码或容器格式中。
>
> “+” 加号代表单一视频和单一音频下载后合并为一个音视频文件，斜线 “/” 表示 “或”，当前方条件不满足时使用后面的条件进行匹配。
>
> best 表示获取包含音频流的最佳视频，如果仅指定 -f b，那么如果仅有一个 360P 的同时包含视频和音频的视频资源，也会被下载，虽然它跟通常意义上的 “高清” 不沾边儿，通常作为一个 “保底” 的可选参数。

自定义输出，参考 [output-template-examples](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#output-template-examples)

```
-o, --output [TYPES:]TEMPLATE
-o "D:\Downloads\%(title)s-%(id)s-%(height)sp.%(ext)s"
-P "D:\Downloads" -o "%(title)s-%(id)s-%(height)sp.%(ext)s" -o "subtitle:%(title)s-%(id)s.%(ext)s" --write-subs
```

## 字幕

```
yt-dlp --list-subs <video_url>

# 下载特定字幕 不下载视频文件
yt-dlp --write-subs --sub-langs <LANGS> --skip-download <video_url>

# 视频中嵌入字幕(仅mp4, webm和mkv视频)
--embed-subs
```

## 播放列表

 -I, --playlist-items ITEM_SPEC

## 其他常用参数

使用 Cookie 下载，需要先导出 Cookie

```
--cookies cookies.txt https://www.bilibili.com/video/BVxxxxx

# or
# 需先关闭浏览器（任务管理器完全关闭）
# 或者浏览器启动参数（chrome系列） –disable-features=LockProfileCookieDatabase
--cookies-from-browser BROWSER[+KEYRING][:PROFILE][::CONTAINER]

# 提取 Cookie 注意不要泄露
yt-dlp --cookies-from-browser chrome --cookies cookies.txt
```

使用 Socket5 设置代理

```
--proxy socks5://127.0.0.1:7897
```

Output progress bar as new lines

```
--newline
```

Ignore download and postprocessing errors. error occurs (Alias: --no-ignore-errors) and "end" (end URL matching); e.g. --ies with a "-" to exclude it, e.g. --ies a list of extractor names. (Alias: --ies)

```
-i, --ignore-errors
```

Don't load any more configuration files

```
--ignore-config
```

HTTP Live Streaming (HLS) ， GUI 里使用的参数， `--help` 中没有打印，怀疑新版去除，这里记录

```
--hls-prefer-native
```
