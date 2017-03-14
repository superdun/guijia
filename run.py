#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, jsonify, request, Response, redirect, session
from dbORM import db, User, Missingchildren,Message
import thumb
from moduleGlobal import app, qiniu_store, QINIU_DOMAIN, CATEGORY, UPLOAD_URL
import moduleAdmin as admin
import flask_login
from moduleWechat import wechat_resp
from flask_paginate import Pagination, get_page_args
from werkzeug import secure_filename
from moduleCache import cache
from faceModule import detect
from smsModule import sendSMS
import time,datetime
import random
import json

# debug in wsgi
# from werkzeug.debug import DebuggedApplication

# app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

#

application = app


def makeIdCode(key):
    v=str(random.randint(100000, 999999))
    cache.set(key=key,value=v,timeout=int(app.config.get('IDCODE_TIMEOUT')))
    return v
def dateConvert(date):

    raw_date = '-'.join([date.split(u'年')[0],date.split(u'年')[1].split(u'月')[0],date.split(u'年')[1].split(u'月')[1].split(u'日')[0]])

    return str(int(time.mktime(datetime.datetime.strptime(raw_date, "%Y-%m-%d").timetuple())))


@app.route('/')
def index(thumbnail=''):
    return render_template('index.html')


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
    msg={"idCode":"%s"% idCode}
    sendResult = sendSMS('id',num,msg).send()
    print sendResult
    return jsonify({'status': 'ok','msg':sendResult})


@app.route('/api/profile', methods=['POST'])
def profileApi():
    adminPhone = app.config.get('SMS_ADMIN_PHONE')
    filter_list=[]
    for i in request.form:
        if request.form[i]=='' or request.form[i]=='null':
            filter_list.append(i)
    if  filter_list:
        return jsonify({'status': 'lacked','msg':filter_list})

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
    idCode = request.form['idCode']
    img = request.files['img']
    if not img:
        return jsonify({'status': 'nopic','msg':''})
    if idCode !=  cache.get(c_tel):
        return jsonify({'status': 'wrongcode', 'msg': ''})
    sourceResult = thumb.upload_file(img, UPLOAD_URL, QINIU_DOMAIN, qiniu_store)
    if sourceResult['result'] == 1:
        sourceImg = sourceResult['localUrl']
        profile = Missingchildren(bid='', image=sourceImg, name=name, gender=gender, birthday=birthday
                        , height=str(height) + u'厘米', missing_time=missing_time, source='guijia', c_name=c_name
                        , c_tel=c_tel, confirm_location='', missing_location_province=missing_location_province
                        , missing_location_city=missing_location_city, missing_location_town=missing_location_town,
                        description=description, comment='', login_time=time.time(), volunteer='', status='pending',
                        short_name=name.split('(')[0].split(u'（')[0].split(' ')[0])
        db.session.add(profile)
        db.session.commit()
        notiMsg='{"name": "%s","number":"%s","description":"%s"}'%(name,c_tel,description[0:20])
        sendNotiResult = sendSMS('noti',adminPhone,notiMsg).send()

        return jsonify(status='ok', error=u'')
    else:
        return jsonify(status='failed', error=u'服务器出错，请稍后再试')
@app.route('/api/member',methods=['POST',])
def newMemberApi():
    filter_list=[]
    adminPhone = app.config.get('SMS_ADMIN_PHONE')
    print request.form
    for i in request.form:
        if request.form[i]=='' or request.form[i]=='null':
            filter_list.append(i)
    if  filter_list:
        return jsonify({'status': 'lacked','msg':filter_list})
    name = request.form['join_name']
    description = request.form['join_description']
    num = str(request.form['join_phone'])
    idCode = str(request.form['idCode'])
    # if idCode !=  cache.get(num):
    #     return jsonify({'status': 'wrongcode', 'msg': ''})

    status = 'pending'

    newMsg = Message(name=name,description=description,mobile=num,status=status)
    db.session.add(newMsg)
    db.session.commit()
    notiMsg='{"name": "%s","number":"%s","description":"%s"}'%(name,num,description[0:20])
    sendNotiResult = sendSMS('noti',adminPhone,notiMsg).send()

    return jsonify(status='ok', error=u'')    



@app.route('/emergency')
def emergencyList():
    return render_template('emergencyList.html')


@app.route('/disappearance')
def disappearanceList():
    bbhj_img_domain = app.config.get('BAOBEIHUIJIA_PREVIEW_IMG_DOMAIN')
    local_img_domain = QINIU_DOMAIN
    page, per_page, offset = get_page_args()
    per_page = app.config.get('PER_PAGE')
    items = Missingchildren.query.filter(Missingchildren.status == 'open').order_by('id desc').offset(offset).limit(
        per_page).all()
    print len(items)
    pagination = Pagination(page=page, total=len(items))
    return render_template('disappearanceList.html', items=items, pagination=pagination,
                           bbhj_img_domain=bbhj_img_domain, local_img_domain=local_img_domain)


@app.route('/disappearance/<disappearanceId>')
def disappearanceDetail(disappearanceId):
    bbhj_img_domain = app.config.get('BAOBEIHUIJIA_IMG_DOMAIN')
    local_img_domain = QINIU_DOMAIN
    item = Missingchildren.query.filter(Missingchildren.id == disappearanceId).first()
    return render_template('disappearanceDetail.html', item=item, bbhj_img_domain=bbhj_img_domain,
                           local_img_domain=local_img_domain)


@app.route('/comparison')
def comparison():
    return render_template('comparisonList.html')


@app.route('/issuance')
def issuance():
    return render_template('issuanceList.html')


# @app.route('/joinus')
# def joinUs():
#     return render_template('join.html')

# @app.route('/donate')
# def donate():
#     return render_template('donate.html')
# @app.route('/post/<postId>')
def post(postId):
    item = Post.query.filter_by(id=postId).first()
    item.view_count = item.view_count + 1
    db.session.commit()
    return render_template('post.html', item=item)


@app.route('/wechat', methods=['GET', 'POST'])
def iot_bath_temp():
    token = app.config.get('WECHAT_TOKEN')
    appid = app.config.get('WECHAT_APPID')
    appsecret = app.config.get('WECHAT_APPSECRET')
    encoding_aes_key = app.config.get('WECHAT_AESKEY')
    encrypt_mode = app.config.get('WECHAT_ENC_MODE')
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    body_text = request.data
    return wechat_resp(token, appid, appsecret,
                       encoding_aes_key, encrypt_mode, signature, timestamp, nonce, body_text)


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
    print request.args.get('echostr')
    body_text = request.data
    return request.args.get('echostr')
    # return wechat_resp(token, appid, appsecret,
    #                    encoding_aes_key, encrypt_mode, signature, timestamp, nonce, body_text)


@app.route('/admin/upload', methods=['POST'])
def upload():
    file = request.files.to_dict()['files[]']
    result = thumb.upload_file(file, UPLOAD_URL, QINIU_DOMAIN, qiniu_store)
    return jsonify(result)


@app.route('/face', methods=['GET', 'POST'])
def face():
    if request.method == 'GET':
        if len(Face.query.filter_by(gender='Male').order_by(Face.grade).all()) < 3:
            listMale = Face.query.filter_by(gender='Male').order_by(Face.grade.desc())[
                       0:len(Face.query.order_by(Face.grade).all())]
        else:
            listMale = Face.query.filter_by(gender='Male').order_by(Face.grade.desc())[0:3]

        if len(Face.query.filter_by(gender='Female').order_by(Face.grade).all()) < 3:
            listFemale = Face.query.filter_by(gender='Female').order_by(Face.grade.desc())[
                         0:len(Face.query.order_by(Face.grade).all())]
        else:
            listFemale = Face.query.filter_by(gender='Female').order_by(Face.grade.desc())[0:3]

        if len(Face.query.filter(Face.age <= 13, Face.age > 0).order_by(Face.grade).all()) < 3:
            listBaby = Face.query.filter(Face.age <= 13, Face.age > 0).order_by(Face.grade.desc())[
                       0:len(Face.query.order_by(Face.grade).all())]
        else:
            listBaby = Face.query.filter(Face.age <= 13, Face.age > 0).order_by(Face.grade.desc())[0:3]
        return render_template('face/faceIndex.html', listMale=listMale, listFemale=listFemale, listBaby=listBaby)
    if request.method == 'POST':
        key = app.config.get('FACE_KEY')
        appKey = app.config.get('FACE_API_KEY')
        img = request.files['img']
        sourceResult = thumb.upload_file(img, UPLOAD_URL, QINIU_DOMAIN, qiniu_store)
        if sourceResult['result'] == 1:
            sourceImg = sourceResult['localUrl']
            detectResult = detect(sourceImg, key, appKey)
            print detectResult
            if detectResult['status']:
                detectResult['status'] = 'ok'
                detectResult['sourceImg'] = sourceImg
                faceDB = Face(grade=round(detectResult['grades']['grade'], 3),
                              eye=round(detectResult['grades']['eye'], 3),
                              mouth=round(detectResult['grades']['mouth'], 3),
                              chin=round(detectResult['grades']['chin'], 3),
                              feel=round(detectResult['grades']['feel'], 3),
                              nose=round(detectResult['grades']['nose'], 3),
                              comment=detectResult['comment'], sourceImg=sourceImg,
                              resultImg=detectResult['imgResult']['localUrl'], gender=detectResult['gender'],
                              age=detectResult['age'])
                db.session.add(faceDB)
                db.session.commit()
                return jsonify(detectResult)
            else:
                detectResult['status'] = 'failed'
                return jsonify(detectResult)
        else:
            return jsonify(status='failed', error=u'服务器出错，请稍后再试')


@app.route('/randomchat', methods=['GET', 'POST'])
def randomChat():
    waitingRoom = redis_store.get('waitingRoom')

    if not waitingRoom or waitingRoom == '':

        room = makeRoomNumber()
        session['room'] = room
        session['name'] = 'A'
        redis_store.set('waitingRoom', '%s:A' % room)
        return render_template('randomchat/chat.html', room=room, name='A')

    else:

        roomInform = waitingRoom.split(':')
        room = roomInform[0]
        if roomInform[1] == 'B':
            name = 'A'
        else:
            name = 'B'
        session['room'] = room
        session['name'] = name
        redis_store.set('waitingRoom', '')
        redis_store.set(room, "{\"A\":{\"count\":0,\"detail\":\"\"},\"B\":{\"count\":0,\"detail\":\"\"}}")
        return render_template('randomchat/chat.html', room=room, name=name)


@app.route('/randomchat/index')
def randomChatIndex():
    if request.args.get('room', '') == redis_store.get('waitingRoom').split(':')[0]:
        redis_store.set('waitingRoom', '')
    return redirect(url_for('randomChat'))


@app.route('/randomchat/getinform')
def getChatInform():
    if request.args.get('room', '') == redis_store.get('waitingRoom').split(':')[0]:
        redis_store.set('waitingRoom', '')
    return redirect(url_for('randomChat'))


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

app.debug = True
if __name__ == '__main__':
    app.run()
