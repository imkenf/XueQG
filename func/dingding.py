import time
import hmac
import hashlib
import base64
import urllib.parse
import requests, json

class DingDingHandler:
    def __init__(self, token, secret):
        self.token = token
        self.secret = secret

    def get_url(self):
        timestamp = round(time.time() * 1000)
        secret_enc = self.secret.encode("utf-8")
        string_to_sign = "{}\n{}".format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode("utf-8")
        hmac_code = hmac.new(
            secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
        ).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

        # 完整的url
        api_url = "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}".format(
            self.token, timestamp, sign
        )
        #print("钉钉机器人url: ", api_url)
        return api_url

    def ddmsgsend(self, msg, mode = "QR", QRID = 0):
        headers = {"Content-Type": "application/json"}  # 定义数据类型
        if mode == "QR":
            data = {
                 "msgtype": "markdown",
                 "markdown": {
                     "title":"学习强国扫码登录",
                     "text": "#### 学习强国登录学习\n > ![](" + msg + ")\n > ###### 二维码生成时间" + \
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n > ###### 二维码ID:" + str(QRID)
                 }
            }
        else:
            data = {
                 "msgtype": "markdown",
                 "markdown": {
                     "title":"学习情况",
                     "text": msg
                 }
            }
        try:
            res = requests.post(self.get_url(), data=json.dumps(data), headers=headers)
            print("已通过钉钉机器人发送成功")
        except Exception as e:
            input("发送失败. 错误信息: " + str(e))
