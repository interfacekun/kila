# -*- coding: utf-8 -*-
# filename: basic.py
import urllib
import time
import json

class Basic():
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0
    def __real_get_access_token(self):
        appId = "wxdfdb576ac4daccd9"
        appSecret = "c9c7bfa262bbe13c2c5a1e3644eb1407"

        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
               "client_credential&appid=%s&secret=%s" % (appId, appSecret))
        urlResp = urllib.urlopen(postUrl)
        urlResp = json.loads(urlResp.read())
        
        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']

    def get_access_token(self):
        nowTime = time.time()
        if nowTime - self.__leftTime > 1*3600:
            self.__real_get_access_token()
            self.__leftTime = nowTime
        return self.__accessToken