#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "qrcode[pil]",
#     "zeroconf>=0.136.2",
# ]
# ///

import random
import string
import sys

import qrcode


def print_qr(ss: str):
    qr = qrcode.QRCode()
    qr.add_data(ss)
    qr.print_ascii(invert=True)


def generate_pair_info() -> tuple[str, str, str]:
    """生成 Android 无线调试配对字符串，返回 (完整QR字符串, 服务名, 配对密码)"""
    # 生成随机服务名
    service_name = "adb-" + "".join(
        random.choices(string.ascii_lowercase + string.digits, k=9)
    )
    # 生成随机配对密码
    pairing_password = "".join(random.choices(string.digits, k=6))

    qr_string = f"WIFI:T:ADB;S:{service_name};P:{pairing_password};;"
    return qr_string, service_name, pairing_password


def do_qr_pair_connect():
    pass


def print_title(title: str):
    print(end="\n" * 2)
    print("=" * 60)
    for line in title.splitlines():
        print(" ", line)
    print("=" * 60)


def main():
    qr_pair_arg = "qr"
    if len(sys.argv) > 1 and sys.argv[1] == qr_pair_arg:
        do_qr_pair_connect()
        return

    print_title("准备工作")
    print(
        """
1. 手机开启开发者选项：【设置】-【关于手机】-连续点击【版本号】7次
2. 电脑安装 adb 和 scrcpy
3. 电脑和手机在同一 Wi-Fi 网络
""",
        end="",
    )

    print_title("首次通过 USB 连接")
    print(
        """
1. 通过 USB 连接
  手机开启 USB 调试：【设置】-【系统】-【开发者选项】-开启【开发者选项】和【USB调试】
  用 USB 数据线连接手机和电脑，并允许 USB 调试
  执行以下命令，显示手机设备序列号则表示连接成功
    adb devices
  执行以下命令，让手机的 ADB 调试监听 TCP/IP 端口，默认 5555
    adb tcpip 5555
  执行成功后，可以拔掉 USB 数据线，进行无线连接（始终监听该端口，直至手机重启）
""",
        """
2. 后续通过无线连接
  获取手机 IP 地址：【设置】-【系统】-【开发者选项】-开启并进入【无线调试】-【 IP 地址和端口】
  执行以下命令，进行无线连接（若连接失败，说明没有监听默认端口，重复上面步骤）
    adb connect ip
  可通过以下命令手动停止 ADB 监听端口
    adb usb
""",
        sep="",
        end="",
    )

    print_title("首次使用【配对码】进行无线连接")
    print(
        """
1. 使用【配对码】进行首次连接
  开启配对码配对：【设置】-【系统】-【开发者选项】-开启并进入【无线调试】-点击【使用配对码配对设备】保持打开
  执行以下命令，完成配对（端口是配对码的端口）
    adb pair ip:port # 并输入配对码
""",
        """
2. 后续通过无线连接
  获取手机 IP 地址和端口：【设置】-【系统】-【开发者选项】-开启并进入【无线调试】-【 IP 地址和端口】
  执行以下命令，进行无线连接
    adb connect ip:port
""",
        sep="",
        end="",
    )

    print_title("首次使用【二维码配对】进行无线连接")
    print(
        f"""
使用此脚本
  {sys.argv[0]} {qr_pair_arg}
""",
        end="",
    )

    print_title("adb 连接完成后，启动 scrcpy")
    print(
        """
执行以下命令，确认连接状态
  adb devices
执行以下命令，启动 scrcpy
  scrcpy
若想在退出后关闭电脑后台的 adb 服务
  adb kill-server
""",
        end="",
    )


if __name__ == "__main__":
    main()
