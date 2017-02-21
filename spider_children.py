#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
import time

from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MissingChild (Base):
    __tablename__ = 'missingChild'

    id = Column(Integer, primary_key=True)

    
    bid = Column(String)
    
    image = Column(String)
    
    name = Column(String)
    
    gender = Column(String)
    
    birthday = Column(String)
    
    height = Column(String)
    
    missing_time = Column(String)
    
    confirm_location = Column(String)
    missing_location_province = Column(String)
    missing_location_city = Column(String)
    missing_location_town = Column(String)
    description = Column(String)
    
    comment = Column(String)
    
    login_time = Column(String)
    
    created_at = Column(String)
    
    volunteer = Column(String)


engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/mywebsite')

DBSession = sessionmaker(bind=engine)
session = DBSession()

d = pq('http://www.baobeihuijia.com/list.aspx?tid=1&sex=&photo=1&page=1')
page = int(d('.nxt').attr('href').split('=')[-1])
for p in range(404,page+1):
    d= pq('http://www.baobeihuijia.com/list.aspx?tid=1&sex=&photo=1&page=%d'%p)
    for i in d('.cimg'):
        detailUrl = 'http://www.baobeihuijia.com'+d(i).parent('a').attr('href')
        dd=pq(detailUrl)
        dd('span').empty()
        bid = dd('#table_1_normaldivr > ul > li:nth-child(2) > a').text()
        image = dd('.cimg').attr('src')

        name = dd('#table_1_normaldivr > ul > li:nth-child(3)').text()

        gender = dd('#table_1_normaldivr > ul > li:nth-child(4)').text()


        birthday = dd('#table_1_normaldivr > ul > li:nth-child(5)').text()

        height = dd('#table_1_normaldivr > ul > li:nth-child(6)').text()

        missing_time = dd('#table_1_normaldivr > ul > li:nth-child(7)').text()

        confirm_location = dd('#table_1_normaldivr > ul > li:nth-child(8)').text()
        if len(dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(','))>1:
            missing_location_province  = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(',')[0]
            missing_location_city  = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(',')[1]
            missing_location_town  = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(',')[-1]
        else:
            missing_location_province  = dd('#table_1_normaldivr > ul > li:nth-child(9)').text().split(',')[0]
            missing_location_city  = ''
            missing_location_town  = ''

        description = dd('#table_1_normaldivr > ul > li:nth-child(10)').text()

        comment = dd('#table_1_normaldivr > ul > li:nth-child(11)').text()

        login_time = dd('#table_1_normaldivr > ul > li:nth-child(12)').text()

        created_at = str(int(time.time()))

        volunteer = dd('#table_1_normaldivr > ul > li:nth-child(13)').text()

        newChild = MissingChild( bid = bid,
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
                                 volunteer=volunteer
                                )
        print name
        session.add(newChild)
        session.commit()


# for i in range(1,page+1):

    # urllib.urlretrieve( %page)