#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "qrcode[pil]",
# ]
# ///

import random
import string

import qrcode


def print_title(title: str):
    print(end="\n" * 2)
    print("=" * 60)
    for line in title.splitlines():
        print(" ", line)
    print("=" * 60)


def main():
    print_title("准备工作")
    print("""
1. 手机开启开发者选项：【设置】-【关于手机】-连续点击【版本号】7次
2. 电脑安装 adb 和 scrcpy
3. 电脑和手机在同一 Wi-Fi 网络
""", end="")

    print_title("首次通过 USB 连接")
    print("""
1. 通过 USB 连接
  手机开启 USB 调试：【设置】-【系统】-【开发者选项】-开启【开发者选项】和【USB调试】
  用 USB 数据线连接手机和电脑，并允许 USB 调试
  执行以下命令，显示手机设备序列号则表示连接成功
    adb devices
  执行以下命令，让手机的 ADB 调试监听 TCP/IP 端口，默认 5555
    adb tcpip 5555
  执行成功后，可以拔掉 USB 数据线，进行无线连接（始终监听该端口，直至手机重启）
""", end="")
    print("""
2. 后续通过无线连接
  获取手机 IP 地址：【设置】-【系统】-【开发者选项】-开启并进入【无线调试】-【 IP 地址和端口】
  执行以下命令，进行无线连接（若连接失败，重复上面步骤）
    adb connect ip
  可通过以下命令手动停止 ADB 监听端口
    adb usb
""", end="")

    print_title("首次使用【配对码】进行无线连接")
    print("""
手机端：【设置】-【系统】-【开发者选项】-开启并进入【无线调试】-点击【使用配对码配对设备】保持打开
电脑端执行以下命令
  adb pair ip:port # 并输入配对码
""", end="")
    print("""
配对完成后可能会自动连接，执行命令查看连接状态
  adb devices
若没有自动连接，可以手动连接（无线调试的端口，而非配对端口）
  adb connect ip:port
""", end="")

    print_title("首次使用【二维码配对】进行无线连接")
    print("""
""", end="")

    print_title("adb 连接完成后，启动 scrcpy")
    print("""
执行以下命令，启动 scrcpy
  scrcpy
若想在退出后关闭电脑后台的 adb 服务
  adb kill-server
""", end="")


if __name__ == "__main__":
    main()
