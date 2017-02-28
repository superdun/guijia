# -*- coding: utf-8 -*-
from flask import Flask

DEBUG = False
SQLALCHEMY_ECHO = False
POST_PER_PAGE = 20
UPLOAD_URL = 'static/upload'
BAOBEIHUIJIA_PREVIEW_IMG_DOMAIN = 'http://www.baobeihuijia.com/photo/small/s_'
BAOBEIHUIJIA_IMG_DOMAIN = 'http://www.baobeihuijia.com/photo/water/water_'
PREVIEW_THUMBNAIL = '-preview'
CATEGORY = [('show_works', u'作品展示'), ('apply', u'活动报名'), ('book_tools', u'仪器预约'), ('our_cool', u'组织风采')]
BASE_URL = '127.0.0.1'
PER_PAGE = 36

CACHE_TYPE = 'filesystem'
CACHE_DIR ='./cache'
CACHE_DEFAULT_TIMEOUT = '3000'
IDCODE_TIMEOUT = '300'