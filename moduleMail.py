# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, jsonify, request, Response, redirect
from flask_mail import Message
from moduleGlobal import app, send_mail
def mail(goal, text):

    msg = Message(u'申请加入%s' % goal, sender=app.config.get('MAIL_USERNAME'),
                  recipients=[app.config.get('MAIL_USERNAME')])
    msg.body = text
    with app.app_context():
        send_mail.send(msg)