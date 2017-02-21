# -*- coding: utf-8 -*-
from wechat_sdk import WechatBasic, WechatConf
import requests
from moduleGlobal import app
import json


def wechat_resp(token='', appid='', appsecret='', encoding_aes_key='', encrypt_mode='', signature='', timestamp='', nonce='', body_text=''):
    conf = WechatConf(token=token, appid=appid, appsecret=appsecret,
                      encoding_aes_key=encoding_aes_key, encrypt_mode=encrypt_mode)
    global wechat
    wechat = WechatBasic(conf=conf)
    print body_text
    wechat.parse_data(body_text)
    message = wechat.get_message()
    response = None
    if message.type == 'text' and message.content == u'浴室':
        return bathroom()
    elif message.type != 'text':
        return defalut_resp()
    elif message.type == 'text' and message.content == u'加入':
        return join()
    elif message.type == 'text' and message.content == u'详情':
        return defalut_resp()
    elif message.type == 'text' and message.content == u'介绍':
        return introduce()
    else:
        return tuling_robot(message.content, message.source)


def oneNETApi(device=0):
    apiKey = app.config.get('ONENET_API_KEY')
    headers = {'api-key': apiKey}
    r = requests.get(
        'http://api.heclouds.com/devices/%d/datastreams' % device, headers=headers)
    return r.json()


def bathroom():
    deviceId = app.config.get('ONENET_API_DEVICE')['bathroom']
    apiResponse = oneNETApi(deviceId)
    if apiResponse['error'] == "succ":
        response = wechat.response_news([
            {
                'title': u'浴室人数传感统计',
                'description': u'当前浴室人数为%d\n数据更新于%s\n本功能由蓝鑫同学提供\n加入华理创客\n成为创客文化的传道者' % (apiResponse['data'][0]['current_value'], apiResponse['data'][0]['update_at']),
                'url': u'http://ecustmaker.com',
                'picurl': u'http://ecustmaker.com/static/LOGO.jpg'
            }
        ])
        return response
    else:
        response = wechat.response_news([
            {
                'title': u'浴室人数传感统计',
                'description': u'ooops,出了点岔子，程序猿正在全速修复！',
                'url': u'http://ecustmaker.com',
                'picurl': u'http://ecustmaker.com/static/LOGO.jpg'
            }
        ])
        return response


def defalut_resp():
    response = wechat.response_news([
        {
            'title': u'加入华理创客',
            'description': u"""加入我们,变身创客,或是创客文化的传播者！
			--------------------------------------
			回复‘加入’：获取加入我们的方式
			回复‘介绍’：查看华理创客的风采
			--------------------------------------
			伊卡斯特物联网：
			回复‘浴室’：获取当前浴室人数
			回复‘温湿度’：获取校园里温度和湿度
			--------------------------------------
            聊天机器人：
            回复任何你想说的话，天气，菜谱，火车航班等等等
            更多功能等你挖掘！
            """,
            'url': u'http://ecustmaker.com',
            'picurl': u'http://ecustmaker.com/static/LOGO.jpg'
        }
    ])
    return response


def tuling_robot(info, fromUserName):
    tulingAPI = app.config.get('TULING_URL_API')
    tulingKey = app.config.get('TULING_APIKEY')
    tulingSecret = app.config.get('TULING_SECRET')
    postBody = {'key': tulingKey, 'info': info,
                'loc': u'上海市徐汇区华东理工大学', 'userid': fromUserName}
    print postBody
    r = requests.post(tulingAPI, data=postBody)
    responseBody = r.json()
    if responseBody['code'] > 400000:
        response = wechat.response_news([
            {
                'title': u'华理创客空间提示您:',
                'description': u'ooops,出了点岔子，程序猿正在全速修复！',
                'url': u'http://ecustmaker.com',
                'picurl': u'http://ecustmaker.com/static/LOGO.jpg'
            }
        ])
        return response
    elif responseBody['code'] == 100000:
        response = wechat.response_text(responseBody['text'])
        return response
    elif responseBody['code'] == 200000:
        response = wechat.response_news([
            {
                'title': u'华理创客空间提示您：',
                'description': responseBody['text'],
                'url': u'http://ecustmaker.com',
                'picurl': u'http://ecustmaker.com/static/LOGO.jpg'
            }
        ])
        return response

    elif responseBody['code'] == 302000:
        response = wechat.response_news([
            {
                'title': responseBody['list'][0]['article'],
                'description': u'来源' + responseBody['list'][0]['source'] + u'\n点击查看详细',
                'url': responseBody['list'][0]['detailurl'],
                'picurl': responseBody['list'][0]['icon']
            }
        ])
        return response
    elif responseBody['code'] == 308000:
        response = wechat.response_news([
            {
                'title': responseBody['list'][0]['name'],
                'description': u'饿了？我觉得华林的菜比较好吃...\n' + responseBody['list'][0]['info'],
                'url': responseBody['list'][0]['detailurl'],
                'picurl': responseBody['list'][0]['icon']
            }
        ])
        return response


def join():
    response = wechat.response_news([
        {
            'title': u'加入我们！',
            'description': u"""可编辑报名短信"创客＋姓名＋联系电话"发送至18018562619
            或编辑邮件"创客＋姓名＋联系电话"发送至邮箱：Ecust_Maker@163.com
            届时我们将会与您联系！""",
            'url': u'http://ecustmaker.com',
            'picurl': u'http://mp.weixin.qq.com/mp/qrcode?scene=10000004&size=102&__biz=MzA5NDMzOTU1Nw=='
        }
    ])
    return response


def introduce():
    response = wechat.response_news([
        {
            'title': u'加入我们！',
            'description': u"""华理创客空间"是一个以创客为主题，集科技创作、技术实践与分享交流的创客空间
            面向华理学子，提供一个创作作品与交流想法的环境，塑造一种创作与实践的氛围
            对有想法的人，这里是一个分享与交流的空间
            对于感兴趣的人，这里是一个参与与学习的环境
            同时，这里也是一个启发兴趣与社交的空间。""",
            'url': u'http://ecustmaker.com',
            'picurl': u'http://ecustmaker.com/static/LOGO.jpg'
        }
    ])
    return response
