#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, jsonify, request, Response, redirect, session
from dbORM import db, User, Post, Carousel, Message, Face
import thumb
from moduleGlobal import app, qiniu_store, QINIU_DOMAIN, CATEGORY, UPLOAD_URL, redis_store
import moduleAdmin as admin
import flask_login
from moduleWechat import wechat_resp
from werkzeug import secure_filename
from faceModule import detect
from chatroomModule import socket, makeRoomNumber

# debug in wsgi
# from werkzeug.debug import DebuggedApplication

# app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

#

application = app


@app.route('/')
def index(carousels=None, img_domain=QINIU_DOMAIN, thumbnail=''):
    carousels = Carousel.query.all()
    thumbnail = app.config.get('CAROUSEL_THUMBNAIL')
    return render_template('index.html', carousels=carousels, img_domain=img_domain, thumbnail=thumbnail)


@app.route('/show_works')
def show_works(items=None, img_domain=QINIU_DOMAIN, thumbnail=''):
    thumbnail = app.config.get('PREVIEW_THUMBNAIL')
    print CATEGORY[0][0]
    items = Post.query.filter_by(
        category=CATEGORY[0][0], status='published').order_by('id desc')

    return render_template('show_works.html', items=items, img_domain=img_domain, thumbnail=thumbnail)


@app.route('/apply')
def apply(items=None, img_domain=QINIU_DOMAIN, thumbnail=''):
    thumbnail = app.config.get('PREVIEW_THUMBNAIL')
    items = Post.query.filter_by(
        category=CATEGORY[1][0], status='published').order_by('id desc')
    return render_template('apply.html', items=items, img_domain=img_domain, thumbnail=thumbnail)


@app.route('/book_tools')
def book_tools(items=None, img_domain=QINIU_DOMAIN, thumbnail=''):
    thumbnail = app.config.get('PREVIEW_THUMBNAIL')
    items = Post.query.filter_by(
        category=CATEGORY[2][0], status='published').order_by('id desc')
    return render_template('book_tools.html', items=items, img_domain=img_domain, thumbnail=thumbnail)


@app.route('/our_cool')
def our_cool(items=None, img_domain=QINIU_DOMAIN, thumbnail=''):
    thumbnail = app.config.get('PREVIEW_THUMBNAIL')
    items = Post.query.filter_by(
        category=CATEGORY[3][0], status='published').order_by('id desc')
    return render_template('our_cool.html', items=items, img_domain=img_domain, thumbnail=thumbnail)


@app.route('/container_ajax')  # ajax
def apply_ajax():
    res = get_file_for_ajax(request.args.get('source'))
    return jsonify(pics=res[0], heads=res[1], introduction=res[2])


@app.route('/joinus')
def joinin():  # ajax....
    if request.args.get('name') and request.args.get('phone').isdigit() and app.config.get(
            'BASE_URL') in request.url_root:
        name = request.args.get('name')
        goal = request.args.get('goal')
        mobile = request.args.get('phone')
        M = Message(name=name, goal=goal, mobile=mobile)
        db.session.add(M)
        db.session.commit()

        # mail(request.args.get('goal'), text)

        return jsonify(status='OK', result=u'欢迎你!!  ' + request.args.get('name') + u'  你的信息已经提交，我们会尽快联系你')
    else:
        return jsonify(status='NO', result=u'请正确完整输入个人信息！')


# post


@app.route('/post/<postId>')
def post(postId):
    item = Post.query.filter_by(id=postId).first()
    item.view_count = item.view_count + 1
    db.session.commit()
    return render_template('post.html', item=item)


# IoT


@app.route('/iot')
def iot():
    return render_template('iot.html')


@app.route('/iot/wechat', methods=['GET', 'POST'])
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


# personal


@app.route('/stationmaster')  # personal
def stationmaster():
    return render_template('stationmaster.html')


@app.route('/guess_num')
def guess_num():
    return render_template('guess_num/guess_num.html')


@app.route('/marysue')
def marysue():
    return render_template('marysue/marysue.html')


@app.route('/spacebattle')
def spacebattle():
    return render_template('spacebattle/spacebattle.html')


@app.route('/eros')
def eros():
    return render_template('eros/eros.html')


@app.route('/refine')
def refine():
    return render_template('refine/refine.html')


@app.route('/dragonboat')
def dragonboat():
    return render_template('dragonboat/dragonboat.html')


@app.route('/fiveson')
def fiveson():
    return render_template('fiveson/fiveson.html')


@app.route('/mosquito')
def mosquito():
    return render_template('mosquito/mosquito.html')


@app.route('/cowboy')
def cowboy():
    return render_template('cowboy/cowboy.html')


@app.route('/cowboy')
def cowboy():
    return render_template('cowboy/cowboy.html')

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
    if request.args.get('room', '')==redis_store.get('waitingRoom').split(':')[0]:
        redis_store.set('waitingRoom', '')
    return redirect(url_for('randomChat'))

@app.route('/randomchat/getinform')
def getChatInform():
    if request.args.get('room', '')==redis_store.get('waitingRoom').split(':')[0]:
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

# login


login_manager = flask_login.LoginManager()

login_manager.init_app(app)
users = {}
raw_users = User.query.all()
for user in raw_users:
    users[user.name] = {'password': user.password}


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
    email = request.form.get('username')
    if email not in users:
        return

    user = User()
    user.id = username

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form[
                                'password'] == users[email]['password']

    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if flask_login.current_user.is_authenticated:
            return redirect('/admin')
        return render_template('login.html')

    username = request.form['username']
    if request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return redirect('/admin')


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


app.debug = True
if __name__ == '__main__':
    socket.run(app)
