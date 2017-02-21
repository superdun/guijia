from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('localConfig.py')
db = SQLAlchemy(app)


# db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    goal = db.Column(db.String(120))
    mobile = db.Column(db.String(120))
    update_time = db.Column(db.String(120))

    def __init__(self, name='', goal='', password='', mobile='', update_time=''):
        self.name = name
        self.goal = goal
        self.mobile = mobile
        self.update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    def __repr__(self):
        return '<User %r>' % self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    auth = db.Column(db.String(120))
    password = db.Column(db.String(120))

    def __init__(self, name='', auth=1, password=''):
        self.name = name
        self.auth = auth
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name


# Flask-Admin can't create model if it has constructor with non-default parameters


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(2000))
    create_at = db.Column(db.String(255))
    img = db.Column(db.String(120))
    view_count = db.Column(db.Integer)
    summary = db.Column(db.String(255))
    category = db.Column(db.String(120))
    book_count = db.Column(db.Integer)
    max_book_count = db.Column(db.Integer)
    status = db.Column(db.String(120))
    is_full = db.Column(db.String(120))

    def __init__(self, title='', content='', img='', view_count=0, summary='', category='', book_count=0,
                 max_book_count=0, status='', is_full='no'):
        self.title = title
        self.content = content
        self.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.img = img
        self.view_count = view_count
        self.summary = summary
        self.category = category
        self.book_count = book_count
        self.max_book_count = max_book_count
        self.status = status
        self.is_full = is_full

    def __repr__(self):
        return '<post %r>' % self.title


class Carousel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(80))
    title = db.Column(db.String(120))
    content = db.Column(db.String(120))

    def __init__(self, img='', title=1, content=''):
        self.img = img
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Carousel %r>' % self.title


class Face(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(120))
    eye = db.Column(db.String(120))
    nose = db.Column(db.String(120))
    mouth = db.Column(db.String(120))
    chin = db.Column(db.String(120))
    feel = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    age = db.Column(db.Integer)
    comment = db.Column(db.String(520))
    sourceImg = db.Column(db.String(120))
    resultImg = db.Column(db.String(120))

    def __init__(self, grade='0', age=0, eye='0', gender='Male', mouth='0', chin='0', feel='0', nose='0', comment='',
                 sourceImg='', resultImg=''):
        self.grade = grade
        self.eye = eye
        self.mouth = mouth
        self.chin = chin
        self.feel = feel
        self.nose = nose
        self.age = age
        self.gender = gender
        self.comment = comment
        self.resultImg = resultImg
        self.sourceImg = sourceImg

    def __repr__(self):
        return '<Face %r>' % self.grade
