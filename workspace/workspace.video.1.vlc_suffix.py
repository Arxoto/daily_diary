suffix_str = """
aac
ac3
flac
m4a
m4p
mp1
mp2
mp3
wav
wma
f4v
flv
mkv
mov
mp2v
mp4
mp4v
rmvb
wmv
m3u
m3u8
ts
VOB
vlc
"""

suffix_list = [f".{l}" for l in suffix_str.splitlines() if l]

video_app_path = R"D:\develop\scoop\apps\vlc\current\vlc.exe".replace("\\", "\\\\")

video_app_name = "CustomVideoPlayer"


# potplayer_uninstall 待补全 可用 Microsoft Store 中的 CCleaner 清理注册表 （实测 FileExts 没法清理）
# HKEY_CLASSES_ROOT\Applications\xxx.exe  不知道有什么用
# HKEY_CLASSES_ROOT\potplayer  默认启动方式
# HKEY_CLASSES_ROOT\PotPlayerMini64.MKV  对特定后缀的启动方式
# HKEY_CLASSES_ROOT\.mkv
#     <default> -> PotPlayerMini64.MKV
# HKEY_LOCAL_MACHINE\SOFTWARE\Clients\Media\PotPlayerMini64  不知道有什么用
# HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Clients\Media\PotPlayerMini64  不知道有什么用
# HKEY_LOCAL_MACHINE\SOFTWARE\Classes\PotPlayerMini64.MKV  对特定后缀的启动方式
# HKEY_LOCAL_MACHINE\SOFTWARE\Classes\.mkv
#     <default> -> PotPlayerMini64.MKV
# HKEY_CURRENT_USER\Software\Classes\.mkv
#     <default> -> PotPlayerMini64.MKV
# HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\ApplicationAssociationToasts  这里有多个app关联到后缀 应该不是通过这里来默认启动的
#     PotPlayerMini64.MKV_.mkv -> 0
# HKEY_CURRENT_USER\Software\xxx  图标和安装目录信息

# regedit
# 默认启动方式强相关
# HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.mp4\xxx


# head
print("Windows Registry Editor Version 5.00")
print()

# default open mode
print(R"[HKEY_CLASSES_ROOT\{}\shell\open\command]".format(video_app_name))
print(R'@="\"{}\" \"%1\""'.format(video_app_path))
print()
for l in suffix_list:
    print(R"[HKEY_CLASSES_ROOT\{}]".format(l))
    print('@="{}"'.format(video_app_name))
    print()

print(R"[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\{}\shell\open\command]".format(video_app_name))
print(R'@="\"{}\" \"%1\""'.format(video_app_path))
print()
for l in suffix_list:
    print(R"[HKEY_LOCAL_MACHINE\Software\Classes\{}]".format(l))
    print('@="{}"'.format(video_app_name))
    print()

# supported types
print(R"[HKEY_CLASSES_ROOT\Applications\{}\shell\open\command]".format(video_app_name))
print(R'@="\"{}\" \"%1\""'.format(video_app_path))
print()
print(R"[HKEY_CLASSES_ROOT\Applications\{}\SupportedTypes]".format(video_app_name))
for l in suffix_list:
    print('"{}"=""'.format(l))
print()
