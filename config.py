# -*- coding: utf-8 -*-
from flask import Flask

DEBUG = False
SQLALCHEMY_ECHO = False
POST_PER_PAGE = 20
UPLOAD_URL = 'static/upload'
CAROUSEL_THUMBNAIL = ''
PREVIEW_THUMBNAIL = '-preview'
CATEGORY = [('show_works', u'作品展示'), ('apply', u'活动报名'), ('book_tools', u'仪器预约'), ('our_cool', u'组织风采')]
BASE_URL = '127.0.0'
