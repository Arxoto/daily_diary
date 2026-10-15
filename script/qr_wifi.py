#!/usr/bin/env python

# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "qrcode[pil]>=8.2",
# ]
#
# [[tool.uv.index]]
# url = "https://mirrors.ustc.edu.cn/pypi/simple"
# default = true
# ///

import os
from enum import StrEnum

import qrcode


def print_qr(ss: str):
    qr = qrcode.QRCode()
    qr.add_data(ss)
    qr.print_ascii(invert=True)


class Wifi:
    class SecurityType(StrEnum):
        """
        加密类型
        """

        WPA = "WPA"
        WEP = "WEP"
        NOT = "nopass"

    def __init__(
        self,
        ssid_name: str,
        password: str,
        security_type=SecurityType.WPA,
        hidden: bool | None = None,
    ):
        self.ssid_name = ssid_name
        self.password = password
        self.security_type = security_type
        self.hidden = hidden

    def __str__(self) -> str:
        ssid = self.special_characters_format(self.ssid_name)
        pwd = self.special_characters_format(self.password)

        if self.hidden is None:
            hidden_field = ""
        else:
            hidden_value = "true" if self.hidden else "false"
            hidden_field = f"H:{hidden_value}"

        wifi_desc = f"WIFI:T:{self.security_type};S:{ssid};P:{pwd};{hidden_field};"

        return wifi_desc

    @staticmethod
    def special_characters_format(string: str):
        return (
            string.replace("\\", "\\\\")
            .replace(":", "\\:")
            .replace(";", "\\;")
            .replace(",", "\\,")
            .replace('"', '\\"')
        )


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "../0private_origin/0_wifi.sh")

    wifi_name = ""
    wifi_pwd = ""

    with open(file_path, "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line and (not wifi_name or not wifi_pwd):
                raise Exception("error reading wifi")  # noqa: TRY002
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
    print(wifi)

    print_qr(str(wifi))
    # 获取wifi名称： netsh wlan show profiles
    # 获取wifi配置： netsh wlan show profile key=clear name="你的WiFi名称"
