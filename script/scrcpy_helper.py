#!/usr/bin/env python3
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "qrcode",
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

INPUT_QUIT = ["q", "quit"]
INPUT_HELP = ["h", "help"]
INPUT_GUIDE = ["g", "guide"]
INPUT_QR_PAIRING = ["qr", "p", "pairing_browser"]
INPUT_AUTO_CONNECT = ["c", "connect_browser"]

PAIRING_TYPE = "_adb-tls-pairing._tcp.local."
CONNECT_TYPE = "_adb-tls-connect._tcp.local."


def help_input_keyword(kws: list[str]) -> str:
    return "[ " + " / ".join(kws) + " ]"


class GlobalContext:
    def __init__(self) -> None:
        self._zc: Zeroconf | None = None
        self.connect_browser: ServiceBrowser | None = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.connect_browser is not None:
            try:
                self.connect_browser.cancel()
            except Exception:  # noqa: BLE001, S110
                pass
        if self._zc is not None:
            try:
                self._zc.close()
            except Exception:  # noqa: BLE001, S110
                pass

    def use_zc(self) -> Zeroconf:
        if self._zc is None:
            self._zc = Zeroconf()
        return self._zc


def print_qr(ss: str):
    qr = qrcode.QRCode(border=1)
    qr.add_data(ss)
    qr.print_ascii(invert=True, tty=sys.stdout.isatty())


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


class AdbServiceListener(ServiceListener):
    def __init__(
        self, on_found: Callable[[str], None], expected_service_name: str | None = None
    ):
        self._on_found = on_found
        self._expected_service_name = expected_service_name

    def _handle(self, zc: Zeroconf, type_: str, name: str):
        info = zc.get_service_info(type_, name)
        if not info:
            return

        if self._expected_service_name:
            instance = info.name.split(".", 1)[0]
            if instance != self._expected_service_name:
                return

        addresses = info.parsed_addresses()
        if not addresses:
            return

        ipv4 = [a for a in addresses if ":" not in a]
        host = ipv4[0] if ipv4 else addresses[0]
        is_ipv6 = ":" in host
        target = f"[{host}]:{info.port}" if is_ipv6 else f"{host}:{info.port}"

        self._on_found(target)

    def add_service(self, zc, type_, name):
        self._handle(zc, type_, name)

    def update_service(self, zc, type_, name):
        self._handle(zc, type_, name)

    def remove_service(self, zc, type_, name):
        pass


def start_connect_browser(ctx: GlobalContext):
    if ctx.connect_browser is not None:
        print("[INFO] 已启动自动连接服务")
        return

    def on_found(target: str) -> None:
        print(f"执行以下命令完成连接：\n    adb connect {target}")
        print("执行以下命令启动 scrcpy\n    scrcpy")

    zc = ctx.use_zc()
    listener = AdbServiceListener(on_found)
    browser = ServiceBrowser(zc, CONNECT_TYPE, listener)
    ctx.connect_browser = browser
    print("[INFO] 成功启动自动连接服务")


def do_qr_pairing(ctx: GlobalContext):
    start_connect_browser(ctx)

    qr_payload, adb_service_name, adb_pair_pwd = generate_pair_info()

    found, on_found, get_target = _found_target_once()

    zc = ctx.use_zc()
    listener = AdbServiceListener(on_found, expected_service_name=adb_service_name)
    browser = ServiceBrowser(zc, PAIRING_TYPE, listener)

    try:
        print_qr(qr_payload)
        print(
            "手机：【设置】-【系统】-【开发者选项】-开启并进入【无线调试】-点击【使用二维码配对设备】并扫描"
        )

        # 等待手机扫描二维码
        while not found.wait(timeout=0.5):
            pass

        print(f"执行以下命令完成配对：\n    adb pair {get_target()} {adb_pair_pwd}")
        print("执行以下命令确认是否自动连接：\n    adb devices")
    except KeyboardInterrupt:
        print("[WARN] 已中止【二维码配对】")
    finally:
        browser.cancel()


def _found_target_once() -> tuple[
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

    return found, on_found, get_target


def print_title(title: str):
    print("\n")
    print("=" * 60)
    for line in title.splitlines():
        print(" ", line)
    print("=" * 60)


def print_guide():
    print_title("准备工作")
    print(
        """
1. 手机开启开发者选项：【设置】-【关于手机】-连续点击【版本号】7次
2. 电脑安装 adb 和 scrcpy
3. 电脑和手机在同一 Wi-Fi 网络
""",
        end="",
    )

    print_title("通过 USB 连接，完成初次连接")
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

    print_title("使用【配对码】，完成初次无线连接")
    print(
        """
1. 使用【配对码】进行初次连接
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

    print_title("使用【二维码配对】，完成初次无线连接")
    print(
        """
需要启动服务，根据下面的输入提示完成操作
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


def print_help():
    print_title("输入说明")
    print(
        f"""
输入 {help_input_keyword(INPUT_QR_PAIRING)} 进行【二维码配对】（同时拉起 mDNS 服务）
输入 {help_input_keyword(INPUT_AUTO_CONNECT)} 拉起 mDNS 服务以自动进行无线连接
输入 {help_input_keyword(INPUT_GUIDE)} 打印 adb scrcpy 连接指导
输入 {help_input_keyword(INPUT_HELP)} 打印输入说明
输入 {help_input_keyword(INPUT_QUIT)} 退出
""",
        end="",
    )


def main():
    with GlobalContext() as ctx:
        print_guide()
        print_help()
        while True:
            # divider_line
            text = input("\n" + "-" * 60 + "\n\n输入命令: ").strip().lower()
            if text in INPUT_QUIT:
                break
            elif text in INPUT_HELP:
                print_help()
            elif text in INPUT_GUIDE:
                print_guide()
            elif text in INPUT_QR_PAIRING:
                do_qr_pairing(ctx)
            elif text in INPUT_AUTO_CONNECT:
                start_connect_browser(ctx)
            elif text:
                print("[ERROR] 未知命令")
                print_help()


if __name__ == "__main__":
    main()
