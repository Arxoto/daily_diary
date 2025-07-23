#!/usr/bin/env python
# -*- coding:utf-8 -*-

from enum import Enum
import os


def showQrImg(ss: str):
    """
    pip install qrcode
    pip install pillow
    or just
    pip install "qrcode[pil]"
    """
    # import qrcode

    # im = qrcode.make(ss)
    # im.show()  # need pillow

    from qrcode.main import QRCode

    qr = QRCode()
    qr.add_data(ss)
    qr.print_ascii(invert=True)


class Wifi:

    class SECURITY_TYPE(str, Enum):
        WPA = "WPA"
        WEP = "WEP"
        NOT = "nopass"

    class SS_ID_VISIBLE(str, Enum):
        HIDE = "H:true"
        SHOW = "H:false"

    def __init__(
        self,
        name: str,
        password: str,
        security_type=SECURITY_TYPE.WPA,
        hide_SSID=True,
    ):
        self.SSID = name
        self.password = password
        self.security_type = security_type
        self.hide_SSID = hide_SSID

    def __str__(self) -> str:
        return "WIFI:T:{};S:{};P:{};{};".format(
            self.security_type,
            self.special_characters_format(self.SSID),
            self.special_characters_format(self.password),
            self.SS_ID_VISIBLE.HIDE if self.hide_SSID else self.SS_ID_VISIBLE.SHOW,
        )

    @staticmethod
    def special_characters_format(string: str):
        return string.replace(":", "\\:").replace(";", "\\;").replace("\\", "\\\\")


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "../0private_origin/0_wifi.sh")

    wifi_name = ""
    wifi_pwd = ""

    with open(file_path, "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                if not wifi_name or not wifi_pwd:
                    raise Exception("error reading wifi")
            if line.startswith("#") or line.isspace():
                continue
            content = line.strip()
            if not wifi_name:
                wifi_name = content
                continue
            if not wifi_pwd:
                wifi_pwd = content
                break

    # 支付宝扫码连接WIFI
    wifi = Wifi(wifi_name, wifi_pwd)
    print("name", wifi_name, "pwd", wifi_pwd)
    # print(wifi)

    showQrImg(str(wifi))
    # 获取wifi名称：netsh wlan show profile
    # 获取wifi配置文件：netsh wlan export profile folder=C:\ key=clear
