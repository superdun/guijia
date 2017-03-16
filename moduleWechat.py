# -*- coding: utf-8 -*-
from wechat_sdk import WechatBasic, WechatConf
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, ImageMessage)
from moduleCache import cache
from moduleFaceSet import FaceSet
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
        face = FaceSet(app.config.get('FACE_SECRET'), app.config.get('FACE_API_KEY'))
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

                    if searchResult.has_key('error'):
                        if searchResult['error']=='noface':
                            title = u'对不起'
                            description = u'请上传更清晰的图片'
                            url=app.config.get('HOST')
                        else:
                            title = u'对不起服务器正忙'
                            description = u'请上传更清晰的图片'
                            url = app.config.get('HOST')
                    elif searchResult['status'] == 0:
                        title = u'对不起,没有匹配到合适的图片'
                        description = u'感谢您的爱心，请在5分钟内回复此图片的拍摄地点，我们将把信息上传至数据库，如之后有匹配成功会及时通知您'
                        url = app.config.get('HOST')
                    elif searchResult['status'] == 1:
                        title = u'找到一张相似度%d的照片'%searchResult['confidence']
                        description = u'我们会立刻处理此信息，请在5分钟内回复此图片的[拍摄地点,您的联系方式]，我们将推送给您给您详细匹配信息'
                    elif searchResult['status'] == 2:
                        title = u'找到一张相似度%d的照片，相似度比较高'%searchResult['confidence']
                        description = u'我们会立刻处理此信息，请立刻回复此图片的[拍摄地点,您的联系方式]，我们将推送给您给您详细匹配信息'
                    elif searchResult['status'] == 3:
                        title = u'找到一张相似度%d的照片！！！，相似度非常高'%searchResult['confidence']
                        description = u'这种情况十分重要，我们会立刻处理此信息，请立刻回复此图片的[拍摄地点,您的联系方式]，我们将推送给您给您详细匹配信息，或直接与13061938526联系'




            else:
                return 0

        else:
            return 0
