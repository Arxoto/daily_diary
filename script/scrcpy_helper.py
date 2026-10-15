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
import threading
from collections.abc import Callable

import qrcode
from zeroconf import ServiceBrowser, ServiceListener, Zeroconf

PAIRING_TYPE = "_adb-tls-pairing._tcp.local."
CONNECT_TYPE = "_adb-tls-connect._tcp.local."


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

    qr_payload = f"WIFI:T:ADB;S:{service_name};P:{pairing_password};;"
    return qr_payload, service_name, pairing_password


class PairingListener(ServiceListener):
    def __init__(self, on_found: Callable[[str], None]):
        self._on_found = on_found

    def add_service(self, zc, type_, name):
        info = zc.get_service_info(type_, name)
        if not info or not info.parsed_addresses():
            return
        host = info.parsed_addresses()[0]
        target = f"{host}:{info.port}"
        self._on_found(target)

    def update_service(self, zc, type_, name):
        self.add_service(zc, type_, name)

    def remove_service(self, zc, type_, name):
        pass


def do_qr_pair_connect():
    [qr_payload, _adb_service_name, adb_pair_pwd] = generate_pair_info()

    # 结果接收
    def new_found_target() -> tuple[
        threading.Event, Callable[[str], None], Callable[[], str]
    ]:
        found = threading.Event()
        target_holder = ""

        def on_found(target: str):
            if found.is_set():
                return
            nonlocal target_holder
            target_holder = target
            found.set()

        def get_target() -> str:
            return target_holder

        return (found, on_found, get_target)

    def new_browser(
        type_: str,
    ) -> tuple[threading.Event, Callable[[], str], Zeroconf, ServiceBrowser]:
        (found, on_found, get_target) = new_found_target()
        zc = Zeroconf()
        listener = PairingListener(on_found)
        browser = ServiceBrowser(zc, type_, listener)
        return (found, get_target, zc, browser)

    # 启动 mDNS 监听
    (pairing_found, pairing_get, pairing_zc, _pairing_browser) = new_browser(
        PAIRING_TYPE
    )
    (connect_found, connect_get, connect_zc, _connect_browser) = new_browser(
        CONNECT_TYPE
    )

    # 打印二维码
    print_qr(qr_payload)

    try:
        while not pairing_found.wait(timeout=0.5):
            pass
        print("执行以下命令完成配对：")
        print(f"    adb pair {pairing_get()} {adb_pair_pwd}")
        while not connect_found.wait(timeout=0.5):
            pass
        print("执行以下命令完成连接：")
        print(f"    adb connect {connect_get()}")
    except KeyboardInterrupt:
        print("[!] 已取消")

    finally:
        pairing_zc.close()
        connect_zc.close()


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
