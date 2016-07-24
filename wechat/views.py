# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.core.cache import cache
import httplib
import json
import time
import uuid
from hashlib import sha1

# appid = "wxe577b89ef194f974"
# mch_id = "1304196401"
device_info = "WEB"
notify_url = "http://www.shuhe-home.com/notice"
trade_type = "JSAPI"
# pay_key = "ytgikJDanShIlinO1tgikJDnShIlin10"


def curl_wrapper(url, domain="api.weixin.qq.com"):
    """
    wechat api 请求，
    :param url:
    :param domain:
    :return: 失败&返回错误／None，成功／返回dict结果
    """
    try:
        conn = httplib.HTTPSConnection(domain)
        conn.request("GET", url)
        res = conn.getresponse()
        if res.status == 200:
            result = json.loads(res.read())
            if "errcode" in result:
                if result["errcode"] == 0:
                    return result
                return None
            return result
        else:
            return None
    except Exception as e:
        return None


class Wechat:
    def __init__(self):
        self.appid = "wxe577b89ef194f974"
        self.secret = "22c12dfc8ab1f4717238e8a909947748"

    def access_token(self):
        """
        获取access_token
        :return: 获取失败/None, 获取成功/“token”
        """
        # https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
        # token = cache.get('token')
        token = None
        if not token:
            url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (self.appid, self.secret)
            result = curl_wrapper(url)
            if result:
                token = result["access_token"]
                # cache.set("token", token, 7200)
            else:
                token = None

        return token

    def jsapi_ticket(self):
        """
        获取jaspi ticket
        :return: 获取失败/None, 获取成功/“ticket”
        """
        # https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=ACCESS_TOKEN&type=jsapi
        token = self.access_token()
        ticket = None
        if token:
            url = "/cgi-bin/ticket/getticket?access_token=%s&type=jsapi" % token
            result = curl_wrapper(url)
            if result:
                ticket = result["ticket"]
            else:
                ticket = None

        return ticket

    def signature(self, url):
        """
        调用js时config配置参数
        jsapi_ticket=sM4AOVdWfPE4DxkXGEs8VMCPGGVi4C3VM0P37wVUCFvkVAy_90u5h9nbSlYy3-Sl-HhTdfl2fzFy1AOcHKP7qg
        &noncestr=Wm3WZYTPz0wzccnW&timestamp=1414587457&url=http://mp.weixin.qq.com?params=value
        :param url:
        :return: 失败/None, 成功/{"noncestr": noncestr, "timestamp": timestamp, "signature": signature}
        """
        ticket = self.jsapi_ticket()
        # print(ticket)
        if ticket:
            timestamp = int(time.time())
            noncestr = str(uuid.uuid1())[0:16]
            raw = "jsapi_ticket=%s&noncestr=%s&timestamp=%d&url=%s" % (ticket, noncestr, timestamp, url)
            signature = sha1(raw).hexdigest()

            return {"noncestr": noncestr, "timestamp": timestamp, "signature": signature}

        return None


if "__main__" == __name__:
    wechat = Wechat()
    signature = wechat.signature("http://www.shuhe-home.com/m")
    print(signature)