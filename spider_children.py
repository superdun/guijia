#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf8")
from pyquery import PyQuery as pq
import time
import datetime

from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
def dateConvert(date):

    raw_date = '-'.join([date.split(u'年')[0],date.split(u'年')[1].split(u'月')[0],date.split(u'年')[1].split(u'月')[1].split(u'日')[0]])

    return str(int(time.mktime(datetime.datetime.strptime(raw_date, "%Y-%m-%d").timetuple())))
class MissingChild (Base):
    __tablename__ = 'missingchildren'

    id = Column(Integer, primary_key=True)


    bid = Column(String)

    image = Column(String)

    name = Column(String)

    gender = Column(String)

    birthday = Column(String)
    
    height = Column(String)
    
    missing_time = Column(String)
    source=Column(String)
    c_name=Column(String)
    c_tel=Column(String)
    status=Column(String)
    confirm_location = Column(String)
    missing_location_province = Column(String)
    missing_location_city = Column(String)
    missing_location_town = Column(String)
    description = Column(String)
    
    comment = Column(String)
    
    login_time = Column(String)
    
    created_at = Column(String)
    
    volunteer = Column(String)
    short_name= Column(String)

engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/guijia')
DBSession = sessionmaker(bind=engine)
session = DBSession()
def baseRecord():
    d = pq('http://www.baobeihuijia.com/list.aspx?tid=1&sex=&photo=1&page=1')
    page = int(d('.nxt').attr('href').split('=')[-1])
    for p in range(1, page + 1)[::-1]:
        d = pq('http://www.baobeihuijia.com/list.aspx?tid=1&sex=&photo=1&page=%d' % p)
        for i in d('.cimg')[::-1]:
            detailUrl = 'http://www.baobeihuijia.com' + d(i).parent('a').attr('href')
            dd = pq(detailUrl)
            dd('span').empty()
            bid = dd('#table_1_normaldivr > ul > li:nth-child(2) > a').text()
            image = dd('.cimg').attr('src').split('_')[-1]

            name = dd('#table_1_normaldivr > ul > li:nth-child(3)').text()

            gender = dd('#table_1_normaldivr > ul > li:nth-child(4)').text()


            birthday = dateConvert(dd('#table_1_normaldivr > ul > li:nth-child(5)').text())
            height = dd('#table_1_normaldivr > ul > li:nth-child(6)').text()

            missing_time = dateConvert(dd('#table_1_normaldivr > ul > li:nth-child(7)').text())

            confirm_location = dd('#table_1_normaldivr > ul > li:nth-child(8)').text()
            if len(dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(',')) > 1:
                missing_location_province = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(',')[0]
                missing_location_city = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(',')[1]
                missing_location_town = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(',')[-1]
            elif len(dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(u'省'))>1:
                missing_location_province = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(u'省')[0]+u'省'
                missing_location_city = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(u'省')[-1].split(u'市')[0]+u'室'
                missing_location_town = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(u'省')[-1].split(u'市')[-1]
            else:
                missing_location_province = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(',')[0]
                missing_location_city = ''
                missing_location_town = ''

            description = dd('#table_1_normaldivr > ul > li:nth-child(10)').text()

            comment = dd('#table_1_normaldivr > ul > li:nth-child(11)').text()

            login_time = dd('#table_1_normaldivr > ul > li:nth-child(12)').text()

            created_at = str(int(time.time()))

            volunteer = dd('#table_1_normaldivr > ul > li:nth-child(13)').text()

            newChild = MissingChild(bid=bid,
                                    image=image,
                                    name=name,
                                    gender=gender,
                                    birthday=birthday,
                                    height=height,
                                    missing_time=missing_time,
                                    confirm_location=confirm_location,
                                    missing_location_province=missing_location_province,
                                    missing_location_city=missing_location_city,
                                    missing_location_town=missing_location_town,
                                    description=description,
                                    comment=comment,
                                    login_time=login_time,
                                    created_at=created_at,
                                    volunteer=volunteer,
                                    source='baobeihuijia',
                                    status='open',
                                    short_name=name.split('(')[0].split(u'（')[0].split(' ')[0]
                                    )
            print name
            session.add(newChild)
            session.commit()



def addRecord():


    d = pq('http://www.baobeihuijia.com/list.aspx?tid=1&sex=&photo=1&page=1')
    page = int(d('.nxt').attr('href').split('=')[-1])
    for p in range(1, page + 1):
        d = pq('http://www.baobeihuijia.com/list.aspx?tid=1&sex=&photo=1&page=%d' % p)
        for i in d('.cimg'):
            detailUrl = 'http://www.baobeihuijia.com' + d(i).parent('a').attr('href')
            dd = pq(detailUrl)
            dd('span').empty()
            bid = dd('#table_1_normaldivr > ul > li:nth-child(2) > a').text()
            image = dd('.cimg').attr('src').split('_')[-1]

            name = dd('#table_1_normaldivr > ul > li:nth-child(3)').text()

            gender = dd('#table_1_normaldivr > ul > li:nth-child(4)').text()

            birthday = dateConvert(dd('#table_1_normaldivr > ul > li:nth-child(5)').text())

            height = dd('#table_1_normaldivr > ul > li:nth-child(6)').text()

            missing_time = dateConvert(dd('#table_1_normaldivr > ul > li:nth-child(7)').text())

            confirm_location = dd('#table_1_normaldivr > ul > li:nth-child(8)').text()
            if len(dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(',')) > 1:
                missing_location_province = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(',')[0]
                missing_location_city = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(',')[1]
                missing_location_town = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(',')[-1]
            elif len(dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(u'省'))>1:
                missing_location_province = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(u'省')[0]+u'省'
                missing_location_city = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(u'省')[-1].split(u'市')[0]+u'室'
                missing_location_town = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(u'省')[-1].split(u'市')[-1]
            else:
                missing_location_province = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(',')[0]
                missing_location_city = ''
                missing_location_town = ''

            description = dd('#table_1_normaldivr > ul > li:nth-child(10)').text()

            comment = dd('#table_1_normaldivr > ul > li:nth-child(11)').text()

            login_time = dd('#table_1_normaldivr > ul > li:nth-child(12)').text()

            created_at = str(int(time.time()))

            volunteer = dd('#table_1_normaldivr > ul > li:nth-child(13)').text()

            newChild = MissingChild(bid=bid,
                                    image=image,
                                    name=name,
                                    gender=gender,
                                    birthday=birthday,
                                    height=height,
                                    missing_time=missing_time,
                                    confirm_location=confirm_location,
                                    missing_location_province=missing_location_province,
                                    missing_location_city=missing_location_city,
                                    missing_location_town=missing_location_town,
                                    description=description,
                                    comment=comment,
                                    login_time=login_time,
                                    created_at=created_at,
                                    volunteer=volunteer,
                                    source='baobeihuijia',
                                    status='open',
                                    short_name=name.split('(')[0].split(u'（')[0].split(' ')[0]
                                    )
            print name
            hasName = len(session.query(MissingChild).filter(MissingChild.name == name).all())
            hasBirthday = len(session.query(MissingChild).filter(MissingChild.birthday == birthday).all())
            print birthday
            if hasName and hasBirthday:
                return  1
            else:
                session.add(newChild)
                session.commit()
                print '+1'
#addRecord()
baseRecord()