# -*- coding: utf-8 -*-
from wechat_sdk import WechatBasic, WechatConf
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, ImageMessage)
from moduleCache import cache
from moduleFaceSet import Face,searchResultHandle
from dbORM import Findingchildren
import requests
from moduleGlobal import app
import json


class Wechat(object):
    def __init__(self, token='', appid='', appsecret='', encoding_aes_key='', encrypt_mode='', signature='',
                 timestamp='', nonce=''):
        self.token = token
        self.appid = appid
        self.appsecret = appsecret
        self.encoding_aes_key = encoding_aes_key
        self.encrypt_mode = encrypt_mode
        self.signature = signature
        self.timestamp = timestamp
        self.nonce = nonce
        conf = WechatConf(token=token, appid=appid, appsecret=appsecret,
                          encoding_aes_key=encoding_aes_key, encrypt_mode=encrypt_mode)
        self.wechat = WechatBasic(conf=conf)

    def getResponse(self, body_text):
        face = Face
        wechat = self.wechat
        if wechat.check_signature(self.signature, self.timestamp, self.nonce):
            try:
                self.wechat.parse_data(body_text)

            except ParseError:
                return 0
            id = wechat.message.id
            target = wechat.message.target
            source = wechat.message.source
            time = wechat.message.time
            type = wechat.message.type
            raw = wechat.message.raw
            if isinstance(wechat.message, TextMessage):
                content = wechat.message.content
            elif isinstance(wechat.message, ImageMessage):
                if cache.get('wechat_' + source):
                    #too fast
                    title = u'对不起'
                    description = u'请不要过于频繁发送图片'
                    url = app.config.get('HOST')
                else:
                    picurl = wechat.message.picurl
                    media_id = wechat.message.media_id
                    searchResult = face.search(picurl, 'missingchildren')
                    searchResultHandle(searchResult)




            else:
                return 0

        else:
            return 0
