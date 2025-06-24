import os
import pyotp
import time


def test():
    # 生成一个密钥（base32 编码）
    secret_key = pyotp.random_base32()

    # 使用密钥和时间间隔（默认为 30 秒）创建一个 TOTP 对象
    totp = pyotp.TOTP(secret_key)

    # 生成当前的 OTP
    current_otp = totp.now()
    print(f"当前 OTP: {current_otp}")

    # 验证 OTP（为演示目的，我们使用刚生成的 OTP）
    is_valid = totp.verify(current_otp)
    print(f"OTP 是否有效？ {is_valid}")

    # 为了演示 OTP 有效性窗口，等待下一个时间间隔
    print("等待超时 31秒")
    time.sleep(31)

    # 再次尝试验证 OTP（由于时间窗口已过，应该无效）
    is_valid = totp.verify(current_otp)
    print(f"OTP 仍然有效吗？ {is_valid}")


def main():
    current_dir = os.path.dirname(__file__)
    key_path = os.path.join(current_dir, "../0private_0rigin/0_github_2FA_key")
    if not os.path.isfile(key_path):
        raise Exception("has no github_2FA_key")

    with open(key_path, "r", encoding="utf-8") as f:
        secret_key = f.read()
        totp = pyotp.TOTP(secret_key)
        print(totp.now())


if __name__ == "__main__":
    # test()
    main()
