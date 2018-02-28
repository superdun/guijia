# -*- coding: utf-8 -*-
from wechat_sdk import WechatBasic, WechatConf
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, ImageMessage)
from moduleCache import cache
from moduleFaceSet import Face,searchResultHandleForWeb
from dbORM import Childrenface,Missingchildren
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
                return wechat.response_text(content)
            elif isinstance(wechat.message, ImageMessage):
                if cache.get('wechat_' + source):
                    #too fast
                    title = u'对不起'
                    description = u'请不要过于频繁发送图片'
                    url = app.config.get('HOST')
                    return  wechat.response_news([{
                        "title": title,
                        "description":description,
                        "url":url
                    }])
                else:
                    picurl = wechat.message.picurl
                    uploadFaceSetResult = Face.uploadFaces([picurl], 'findingchildren')
                    media_id = wechat.message.media_id
                    searchResult = face.search(picurl, 'missingchildren')
                    rawResult = searchResultHandleForWeb(searchResult)
                    if 'token'  not in searchResult:
                        return wechat.response_text(u"服务器正忙")
                    title = rawResult['title']
                    sameChildRecord = Childrenface.query.filter_by(token=searchResult['token']).first()
                    description = rawResult['description']
                    url = app.config.get('HOST')
                    if sameChildRecord:
                        sameChild = Missingchildren.query.filter_by(id=sameChildRecord.childrenId).first()
                        return wechat.response_news([{
                            "title": title,
                            "description": description,
                            "picurl": sameChild.image
                        }])
                    else:
                        return wechat.response_news([{
                            "title": title,
                            "description": description,
                            "url": url
                        }])

            else:
                return wechat.response_text(u"请上传疑似走失者的图片")

        else:
            return wechat.response_text(u"服务器正在修复")
