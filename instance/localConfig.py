# -*- coding: utf-8 -*-
from flask import Flask

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost:3306/guijia'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = '123456'

QINIU_ACCESS_KEY = 'u1M-QQ-m0ciNAhDn2AZ6iODyKnjUmY7EW1uH2ZiZ'
QINIU_SECRET_KEY = 'QN3dDZvbX5MdDxfWsf4vua774Wz_5JFCZP78PGTU'
QINIU_BUCKET_NAME = 'makerimg'
QINIU_BUCKET_DOMAIN = 'oc1is8h9w.bkt.clouddn.com'

WECHAT_TOKEN = 'weixin'
WECHAT_APPID = 'wx684db814d4ca03c7'
WECHAT_APPSECRET = '104bea23055f9456b08ced99b52534ee'
WECHAT_AESKEY = '0x4XDH4Q7zxbBzeglgSkUXsb1gEtUM9mAamuf1m1Hjk'
WECHAT_ENC_MODE = 'normal'
ONENET_API_DEVICE = {'bathroom': 3227278}
ONENET_API_KEY = 'txhCzJ9NX7iORS9RwYHEdfpTck0='

FACE_KEY = "ZfZkvZVgtmq023KgiYjj8zYp-eGmG-wJ"
FACE_API_KEY = "F2pl2jjyeTtSFPIllQ-MCF9HT2DPqRv5"

SMS_ACCESS_KEY = 'LTAIUOngdXDC5UZG'
SMS_SIGN_NAME = u'归家网'
SMS_MODEL_ID_CODE = 'SMS_50170185'
SMS_MODEL_NOTI_CODE = 'SMS_53810335'
SMS_ACCESS_SECRET = 'OJrsCzzMOZSIzbnhplwQO1krfgRNnF'
SMS_URL = 'https://sms.aliyuncs.com'
