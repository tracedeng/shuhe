# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.core.cache import cache
import httplib
import json
import time
import uuid
from hashlib import sha1, md5
from xmltodict import parse, unparse


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


def curl_wrapper_post(url, domain="api.weixin.qq.com", params=None, headers=None):
    """
    wechat api 请求，
    :param url:
    :param domain:
    :return: 失败&返回错误／None，成功／返回dict结果
    """
    try:
        conn = httplib.HTTPSConnection(domain)
        conn.request("POST", url, params, headers)
        res = conn.getresponse()
        if res.status == 200:
            result = parse(res.read())
            return result['xml']
        else:
            return None
    except Exception as e:
        return None


class Wechat:
    def __init__(self):
        self.appid = "wxe577b89ef194f974"
        self.secret = "22c12dfc8ab1f4717238e8a909947748"

    def openid(self, code):
        """
        后去openid
        :param code: 菜单跳转带的code
        :return: 获取失败/None, 获取成功/“openid”
        """
        # https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE
        #       &grant_type=authorization_code
        url = "/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" \
              % (self.appid, self.secret, code)
        result = curl_wrapper(url)
        if result:
            openid = result.get("openid", None)
        else:
            openid = None

        return openid

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

            return {"noncestr": noncestr, "timestamp": timestamp, "signature": signature, "appid": self.appid}

        return None

    def signature2(self, d, key):
        """
        统一下单签名
        :param d:
        :param key:
        :return: 签名
        """
        plain = "&".join(["%s=%s" % (v, d[v]) for v in sorted(d.keys())])
        plain = "%s&key=%s" % (plain, key)

        return md5(plain).hexdigest().upper()

    def unified_order(self, activity_name, out_trade_no, total_fee, spbill_create_ip, openid):
        """
        统一下单
        https://api.mch.weixin.qq.com/pay/unifiedorder
        :param activity_name:活动标题
        :param out_trade_no:商品订单号
        :param total_fee:金额
        :param spbill_create_ip:支付端ip
        :param openid:用户在商户下唯一标识
        :return:
        """
        url = "/pay/unifiedorder"
        notify_url = "http://www.shuhe-home.com/notice"
        pay_key = "gmgm201607292034gmgm201607292034"
        nonce = str(uuid.uuid1())[0:16]
        d = {"appid": self.appid, "mch_id": "1362765402", "device_info": "WEB", "nonce_str": nonce,
             "body": activity_name, "out_trade_no": out_trade_no, "total_fee": total_fee, "openid": openid,
             "spbill_create_ip": spbill_create_ip, "notify_url": notify_url, "trade_type": "JSAPI"}
        d["sign"] = self.signature2(d, pay_key)
        params = unparse({"xml": d}).split("\n")[1]  # json2xml
        headers = {"Content-Type": "text/xml"}
        result = curl_wrapper_post(url, domain="api.mch.weixin.qq.com", params=params, headers=headers)
        prepay_id = None
        if result and "SUCCESS" == result.get("return_code", "FAIL") and "SUCCESS" == result.get("result_code", "FAIL"):
            prepay_id = result.get("prepay_id", None)

        if prepay_id:
            timestamp = int(time.time())
            pay_sign = self.signature2({"nonceStr": nonce, "signType": "MD5", "package": "prepay_id=%s" % (prepay_id,),
                                        "timestamp": timestamp}, pay_key)
            return {"prepay_id": prepay_id, "nonce_str": nonce, "sign": pay_sign, "timestamp": timestamp}
        else:
            return None

    def notice(self, data):
        """
        异步通知，
        :param data: 通知post
        :return: 成功/out_trade_no，失败/None
        """
        result = parse(data)
        result = result['xml']
        if result and "SUCCESS" == result.get("return_code", "FAIL"):
            out_trade_no = result.get("out_trade_no", None)
            return out_trade_no

        return None


if "__main__" == __name__:
    wechat = Wechat()
    # signature = wechat.signature("http://www.shuhe-home.com/m")
    # print(signature)
    wechat.unified_order("hello", "2123", "100", "192.168.1.1", "jifwfwefwef")
