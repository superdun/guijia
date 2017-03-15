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
    description = db.Column(db.String(1020))
    mobile = db.Column(db.String(11))
    created_at = db.Column(db.String(120))
    status = db.Column(db.String(120))

    def __init__(self, name='', description='', mobile='', created_at='', status='pending'):
        self.name = name
        self.description = description
        self.mobile = mobile
        self.created_at = time.time()
        self.status = status

    def __repr__(self):
        return '<msg %r>' % self.name


class Findingchildren(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1020))
    created_at = db.Column(db.String(120))
    status = db.Column(db.String(120))
    loc_province = db.Column(db.String(120))
    loc_city = db.Column(db.String(120))
    loc_town = db.Column(db.String(120))
    source = db.Column(db.String(1020))
    img = db.Column(db.String(1020))

    def __init__(self, description='', source='', created_at='', status='pending', loc_province='', loc_city='',
                 loc_town='', img=''):
        self.description = description
        self.created_at = time.time()
        self.status = status
        self.source = source
        self.loc_province = loc_province
        self.loc_city = loc_city
        self.loc_town = loc_town
        self.img = img

    def __repr__(self):
        return '<Findingchildren %r>' % self.source


class Childrenface(db.Model):
    childrenId = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(180))

    def __init__(self, childrenId=0, token=''):
        self.childrenId = childrenId
        self.token = token

    def __repr__(self):
        return '<cid %r>' % self.childrenId

class FChildrenface(db.Model):
    childrenId = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(180))

    def __init__(self, childrenId=0, token=''):
        self.childrenId = childrenId
        self.token = token

    def __repr__(self):
        return '<cid %r>' % self.childrenId


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


class Missingchildren(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bid = db.Column(db.String(1200))
    image = db.Column(db.String(1200))
    name = db.Column(db.String(1200))
    gender = db.Column(db.String(1200))
    birthday = db.Column(db.String(1200))
    height = db.Column(db.String(1200))
    missing_time = db.Column(db.String(1200))
    source = db.Column(db.String(1200))
    c_name = db.Column(db.String(1200))
    c_tel = db.Column(db.String(1200))
    confirm_location = db.Column(db.String(1200))
    missing_location_province = db.Column(db.String(1200))
    missing_location_city = db.Column(db.String(1200))
    missing_location_town = db.Column(db.String(1200))
    description = db.Column(db.String(1200))
    comment = db.Column(db.String(1200))
    login_time = db.Column(db.String(1200))
    created_at = db.Column(db.String(1200))
    volunteer = db.Column(db.String(1200))
    status = db.Column(db.String(1200))
    short_name = db.Column(db.String(1200))

    def __init__(self, bid='', image='', name='', gender='', birthday='', height='', missing_time='', source='',
                 c_name='', c_tel='', confirm_location='', missing_location_province='',
                 missing_location_city='', missing_location_town='', description='', comment='', login_time='',
                 volunteer='', status='open', short_name=''):
        self.bid = bid
        self.image = image
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.height = height
        self.missing_time = missing_time
        self.source = source
        self.c_name = c_name
        self.c_tel = c_tel
        self.confirm_location = confirm_location
        self.missing_location_province = missing_location_province
        self.missing_location_city = missing_location_city
        self.missing_location_town = missing_location_town
        self.description = description
        self.comment = comment
        self.login_time = login_time
        self.created_at = int(time.time())
        self.volunteer = volunteer
        self.status = status
        self.short_name = short_name

    def __repr__(self):
        return '<MissingChildren %r>' % self.name
