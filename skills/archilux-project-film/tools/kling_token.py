#!/usr/bin/env python3
"""在【你自己的电脑】上运行，把可灵的 Access Key + Secret Key 签成一个长效令牌（JWT）。
签好的令牌填进 Claude 弹出的安全卡片里，不要贴进聊天。

用法:
  pip install pyjwt
  python3 kling_token.py            # 按提示输入 AK、SK（输入时不显示）
  python3 kling_token.py --days 30  # 有效天数，默认 30
"""
import time, argparse, getpass
import jwt  # pip install pyjwt

ap = argparse.ArgumentParser(); ap.add_argument("--days", type=int, default=30); a = ap.parse_args()
ak = input("Access Key: ").strip()
sk = getpass.getpass("Secret Key（输入时不显示）: ").strip()
now = int(time.time())
token = jwt.encode({"iss": ak, "exp": now + a.days * 86400, "nbf": now - 5}, sk,
                   algorithm="HS256", headers={"alg": "HS256", "typ": "JWT"})
print("\n复制下面这一整行（只有两个点号分隔的三段），填进 Claude 的卡片：\n")
print(token)
