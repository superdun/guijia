#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, jsonify, request, Response, redirect, session
from dbORM import db,Searchrecord, User, Missingchildren, Message, Childrenface, Findingchildren,Fchildrenface
import thumb
from moduleGlobal import app, qiniu_store, QINIU_DOMAIN, CATEGORY, UPLOAD_URL
import moduleAdmin as admin
import flask_login
from moduleWechat import Wechat
from flask_paginate import Pagination, get_page_args
from werkzeug import secure_filename
from moduleCache import cache
from faceModule import detect
from smsModule import sendSMS
import time, datetime
from moduleFaceSet import Face,searchResultHandleForWeb
import random
import json

# debug in wsgi
# from werkzeug.debug import DebuggedApplication

# app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

#




@app.template_filter('strftime')
def _jinja2_filter_datetime(date):
    return time.strftime(u"%Y-%m-%d", time.localtime(float(date)))


def makeIdCode(key):
    v = str(random.randint(100000, 999999))
    cache.set(key=key, value=v, timeout=int(app.config.get('IDCODE_TIMEOUT')))
    return v


def dateConvert(date):
    raw_date = '-'.join(
        [date.split(u'年')[0], date.split(u'年')[1].split(u'月')[0], date.split(u'年')[1].split(u'月')[1].split(u'日')[0]])

    return str(int(time.mktime(datetime.datetime.strptime(raw_date, "%Y-%m-%d").timetuple())))


@app.route('/')
def guide(thumbnail=''):
    return render_template('guide.html')


@app.route('/index')
def index(thumbnail=''):
    return render_template('index.html')


@app.route('/profile')
def profile(thumbnail=''):
    return render_template('profile.html')


@app.route('/api/mapData')
def mapDataApi():
    curTime = time.time()
    bbhj_img_domain = app.config.get('BAOBEIHUIJIA_PREVIEW_IMG_DOMAIN')
    local_img_domain = QINIU_DOMAIN
    base_url = 'disappearance/'
    todayTime = curTime - curTime % 86400
    items = Missingchildren.query.filter(Missingchildren.created_at >= todayTime).filter(
        Missingchildren.status == 'open').all()
    results = {}
    for i in items:
        if u'内蒙古' in i.missing_location_province:
            province = u'内蒙古'
        elif len(i.missing_location_province) < 2:
            continue
        else:
            province = i.missing_location_province[:2]
        if province in results.keys():
            results[province]['count'] += 1
        else:
            if i.source == 'baobeihuijia':
                img_url = bbhj_img_domain + i.image
            else:
                img_url = local_img_domain + i.image
            results[province] = {"name": province, "count": 0,
                                 "tooltip": "<a href='%s'><b><font size='15' color='#238B45'>%s</font></b></a><br>%s<br><img src='%s' width='150'/>" % (
                                     base_url + str(i.id), i.short_name, i.description[:10] + '...', img_url)}
    for j in results.values():
        j['tooltip'] = (u"<font size='15' color='#238A45'>%s</font>最新动态：<br>" % (
            j['name'] + u':' + str(j['count']) + u'个<br>')) + \
                       j['tooltip']

    return jsonify(results.values())


@app.route('/api/idcode', methods=['POST'])
def idcodeApi():
    num = str(int(request.form['phone']))
    idCode = makeIdCode(num)
    msg = '{"idCode": "%s"}' % idCode
    sendResult = sendSMS('id', num, msg).send()
    # print sendResult
    return jsonify({'status': 'ok', 'msg': sendResult})


@app.route('/api/profile', methods=['POST'])
def profileApi():
    adminPhone = app.config.get('SMS_ADMIN_PHONE')
    filter_list = []
    for i in request.form:
        if request.form[i] == '' or request.form[i] == 'null':
            filter_list.append(i)
    if filter_list:
        return jsonify({'status': 'lacked', 'msg': filter_list})

    name = request.form['lost_name']
    gender = request.form['gender']
    birthday = dateConvert(request.form['birthday'])
    missing_time = dateConvert(request.form['lost_date'])
    missing_location_province = request.form['lost_loc_province']
    missing_location_city = request.form['lost_loc_city']
    missing_location_town = request.form['lost_loc_town']
    height = request.form['height']
    description = request.form['description']
    c_name = request.form['contact_name']
    c_tel = str(request.form['contact_phone'])
    idCode = str(request.form['idCode'])
    img = request.files['img']
    if not img:
        return jsonify({'status': 'nopic', 'msg': ''})
    if idCode != cache.get(c_tel):
        return jsonify({'status': 'wrongcode', 'msg': ''})
    sourceResult = thumb.upload_file(img, UPLOAD_URL, QINIU_DOMAIN, qiniu_store)
    if sourceResult['result'] == 1:
        sourceImg = sourceResult['localUrl']
        profile = Missingchildren(bid=None, image=sourceImg, name=name, gender=gender, birthday=birthday
                                  , height=str(height) + u'厘米', missing_time=missing_time, source='guijia',
                                  c_name=c_name
                                  , c_tel=c_tel, confirm_location='',
                                  missing_location_province=missing_location_province
                                  , missing_location_city=missing_location_city,
                                  missing_location_town=missing_location_town,
                                  description=description, comment='', login_time=time.time(), volunteer='',
                                  status='pending',
                                  short_name=name.split('(')[0].split(u'（')[0].split(' ')[0])

        db.session.add(profile)
        db.session.commit()
        cache.delete(c_tel)
        tag='findingchildren'
        rawSearchResult = Face.search(sourceImg,tag)
        searchResult=searchResultHandleForWeb(rawSearchResult)
        uploadFaceSetResult = Face.uploadFaces([sourceImg], 'missingchildren')

        if uploadFaceSetResult[0][0]=="":
            return jsonify(status='failed', error=u'服务器出错，请稍后再试', description=u"", title="")
        # print uploadFaceSetResult
        CF = Childrenface(childrenId=profile.id, token=uploadFaceSetResult[0][0])
        db.session.add(CF)
        db.session.commit()
        description=""
        title=""
        if searchResult['stage']>0:
            description=searchResult['description']
            title=searchResult['title']
        # print searchResult['description']
        notiMsg = '{"name": "%s","number":"%s"}' % (name, c_tel)
        sendNotiResult = sendSMS('noti_a', adminPhone, notiMsg).send()

        return jsonify(status='ok', error=u'',title=title,description=description)
    else:
        return jsonify(status='failed', error=u'服务器出错，请稍后再试',description=u"",title="")


@app.route('/api/member', methods=['POST', ])
def newMemberApi():
    filter_list = []
    adminPhone = app.config.get('SMS_ADMIN_PHONE')
    # print request.form
    for i in request.form:
        if request.form[i] == '' or request.form[i] == 'null':
            filter_list.append(i)
    if filter_list:
        return jsonify({'status': 'lacked', 'msg': filter_list})
    name = request.form['join_name']
    description = request.form['join_description']
    num = str(request.form['join_phone'])
    idCode = str(request.form['idCode'])
    if idCode != cache.get(num):
        return jsonify({'status': 'wrongcode', 'msg': ''})

    status = 'pending'

    newMsg = Message(name=name, description=description, mobile=num, status=status)
    db.session.add(newMsg)
    db.session.commit()
    cache.delete(num)
    notiMsg = '{"name": "%s","number":"%s"}' % (name, num)
    # sendNotiResult = sendSMS('noti_v', adminPhone, notiMsg).send()

    return jsonify(status='ok', error=u'')


@app.route('/api/clu', methods=['POST', ])
def newCluApi():
    adminPhone = app.config.get('SMS_ADMIN_PHONE')
    filter_list = []
    for i in request.form:
        if request.form[i] == '' or request.form[i] == 'null':
            filter_list.append(i)
    if filter_list:
        return jsonify({'status': 'lacked', 'msg': filter_list})
    find_date = dateConvert(request.form['find_date'])
    find_loc_province = request.form['find_loc_province']
    find_loc_city = request.form['find_loc_city']
    find_loc_town = request.form['find_loc_town']
    description = request.form['description']
    c_name = request.form['contact_name']
    c_tel = str(request.form['contact_phone'])
    idCode = request.form['idCode']
    img = request.files['img']
    if not img:
        return jsonify({'status': 'nopic', 'msg': ''})
    if idCode != cache.get(c_tel):
        return jsonify({'status': 'wrongcode', 'msg': ''})
    sourceResult = thumb.upload_file(img, UPLOAD_URL, QINIU_DOMAIN, qiniu_store)
    if sourceResult['result'] == 1:
        sourceImg = sourceResult['localUrl']
        clu = Findingchildren(img=sourceImg, finding_time=find_date, source='guijia',
                              c_name=c_name, c_tel=c_tel,
                              loc_province=find_loc_province
                              , loc_city=find_loc_city,
                              loc_town=find_loc_town,
                              description=description,
                              status='pending')

        db.session.add(clu)
        db.session.commit()
        cache.delete(c_tel)
        tag='missingchildren'
        rawSearchResult = Face.search(sourceImg,tag)
        searchResult=searchResultHandleForWeb(rawSearchResult)
        if searchResult['status']!='ok':
            # searchrecord = Searchrecord(tag=tag, source='findingchildren', source_id=clu.id,
            #                             confidence=0,
            #                             detail=json.dumps(rawSearchResult['detail']),
            #                             theshold=json.dumps(rawSearchResult['thresholds']),target=rawSearchResult['token'],status='error')
            # db.session.add(searchrecord)
            # db.session.commit()
            return jsonify(status='failed', error=u'服务器出错，请稍后再试')
        else:
            searchrecord = Searchrecord(tag=tag, source='findingchildren', source_id=clu.id,
                                        confidence=rawSearchResult['confidence'],
                                        detail=json.dumps(rawSearchResult['detail']),
                                        theshold=json.dumps(rawSearchResult['thresholds']),target=rawSearchResult['token']
                                        ,status=rawSearchResult['status'])
            db.session.add(searchrecord)
            db.session.commit()
            notiMsg = u'{"name": "%s","number":"%s"}' % (u'新线索'+str(rawSearchResult['confidence']), c_tel)


        uploadFaceSetResult = Face.uploadFaces([sourceImg], 'findingchildren')
        if uploadFaceSetResult[0][0]=="":
            return jsonify(status='failed', error=u'服务器出错，请稍后再试', description=u"", title="")

        fChildrenFace = Fchildrenface(clu.id, uploadFaceSetResult[0][0])
        db.session.add(fChildrenFace)
        db.session.commit()
        sendNotiResult = sendSMS(u'noti_a', adminPhone, notiMsg).send()
        return jsonify(status='ok', error=u'',msg=searchResult)
    else:
        return jsonify(status='failed', error=u'服务器出错，请稍后再试')


@app.route('/emergency')
def emergencyList():
    return render_template('emergencyList.html')


@app.route('/disappearance')
def disappearanceList():
    bbhj_img_domain = app.config.get('BAOBEIHUIJIA_PREVIEW_IMG_DOMAIN')
    local_img_domain = QINIU_DOMAIN
    page, per_page, offset = get_page_args()
    per_page = app.config.get('PER_PAGE')
    total = len(Missingchildren.query.filter(Missingchildren.status == 'open').all())
    items = Missingchildren.query.filter(Missingchildren.status == 'open').filter(
        Missingchildren.missing_time != u'未知时间').order_by('missing_time desc').offset(offset).limit(
        per_page).all()
    # print get_page_args()
    pagination = Pagination(page=page, total=total,per_page=per_page)
    return render_template('disappearanceList.html', items=items, pagination=pagination,
                           bbhj_img_domain=bbhj_img_domain, local_img_domain=local_img_domain)


@app.route('/disappearance/<disappearanceId>')
def disappearanceDetail(disappearanceId):
    bbhj_img_domain = app.config.get('BAOBEIHUIJIA_IMG_DOMAIN')
    local_img_domain = QINIU_DOMAIN
    item = Missingchildren.query.filter(Missingchildren.id == disappearanceId).first()
    return render_template('disappearanceDetail.html', item=item, bbhj_img_domain=bbhj_img_domain,
                           local_img_domain=local_img_domain)


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/api/wechat', methods=['GET', 'POST'])
def iot_bath_temp():
    token = app.config.get('WECHAT_TOKEN')
    appid = app.config.get('WECHAT_APPID')
    appsecret = app.config.get('WECHAT_APPSECRET')
    encoding_aes_key = app.config.get('WECHAT_AESKEY')
    encrypt_mode = app.config.get('WECHAT_ENC_MODE')
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    return echostr
    # body_text = request.data
    # return wechat_resp(token, appid, appsecret,
    #                    encoding_aes_key, encrypt_mode, signature, timestamp, nonce, body_text)


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    token = app.config.get('WECHAT_TOKEN')
    appid = app.config.get('WECHAT_APPID')
    appsecret = app.config.get('WECHAT_APPSECRET')
    encoding_aes_key = app.config.get('WECHAT_AESKEY')
    encrypt_mode = app.config.get('WECHAT_ENC_MODE')
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    # print request.args.get('echostr')
    body_text = request.data
    # return request.args.get('echostr')
    w = Wechat(token, appid, appsecret,
                       encoding_aes_key, encrypt_mode, signature, timestamp, nonce)
    return w.getResponse(body_text)


# @app.route('/token')
# def faceToken():
#     children=Missingchildren.query.all()
#     secret = app.config.get('FACE_SECRET')
#     apiKey = app.config.get('FACE_API_KEY')
#     face = FaceSet(secret, apiKey)
#     for i in children:
#
#         url=app.config.get('BAOBEIHUIJIA_IMG_DOMAIN')+i.image
#         result = face.uploadFaces([url], 'missingchildren')
#         print result
#         cf = Childrenface(childrenId=i.id, token=result[0])
#         db.session.add(cf)
#         db.session.commit()
#
#
#     # if len(result)==len(ids):
#     #     for i in range(len(result)):
#     #         cf = Childrenface(childrenId=ids[i],token=result[i])
#     #         db.session.add(cf)
#     db.session.commit()



@app.route('/admin/upload', methods=['POST'])
def upload():
    file = request.files.to_dict()['files[]']
    result = thumb.upload_file(file, UPLOAD_URL, QINIU_DOMAIN, qiniu_store)
    return jsonify(result)


@app.route("/robots.txt")
def robots_txt():
    return Response('User-agent: *' + '\n' + 'Allow: /')


@app.route("/baidu_verify_5DVru9pOZg.html")
def baidu_verify():
    return Response('5DVru9pOZg')


@app.route("/google538a02e0b0893d2d.html")
def google_verify():
    return Response('google-site-verification: google538a02e0b0893d2d.html')


# admin
admin.dashboard()

# login


login_manager = flask_login.LoginManager()

login_manager.init_app(app)
users = {}
raw_users = User.query.all()
for user in raw_users:
    users[user.mobile] = {'password': user.password}


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    mobile = request.form.get('mobile')
    if mobile not in users:
        return

    user = User()
    user.id = mobile

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[mobile]['password']

    return user

@app.route('/api/login', methods=['POST',])
def loginApi():
    mobile = str(request.form['phone'])
    idCode = str(request.form['idCode'])
    if idCode==cache.get(mobile):
        return jsonify({'status': 'bad idCode'})
    if request.form['password'] == users[mobile]['password']:
        user = User()
        user.id = mobile
        flask_login.login_user(user)
        cache.delete(mobile)
        return jsonify({'status': 'OK'})

    return jsonify({'status': 'bad login'})
@app.route('/login')
def login():
    if flask_login.current_user.is_authenticated:
        return redirect('/admin')
    return render_template('log.html')





@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


application = app
if __name__ == '__main__':
    app.run(port=8080)
