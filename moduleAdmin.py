# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, jsonify, request, Response, redirect
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms import Form as wtForm
from dbORM import db, User,Message
from wtforms import TextAreaField, SelectField
from wtforms.widgets import TextArea
import thumb
from flask_qiniustorage import Qiniu
from flask_admin import form
from flask_admin.form import rules
import flask_login
import os
import os.path as op
from moduleGlobal import app, admin,qiniu_store, QINIU_DOMAIN, CATEGORY, UPLOAD_URL
import shutil

def dashboard():


    admin.add_view(UserView(User, db.session))

    admin.add_view(ModelView(Message, db.session))





class CKTextAreaWidget(TextArea):

    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class ImageUpload(form.ImageUploadField):

    def _save_file(self, data, filename):
        path = self._get_path(filename)
        if not op.exists(op.dirname(path)):
            os.makedirs(os.path.dirname(path), self.permission | 0o111)

        data.seek(0)
        data.save(path)
        with open(path, 'rb') as fp:
            ret, info = qiniu_store.save(fp, filename)
            if 200 != info.status_code:
                raise Exception("upload to qiniu failed", ret)
            #shutil.rmtree(os.path.dirname(path))
            return filename



class UserView(ModelView):
    def is_accessible(self):
        return flask_login.current_user.is_authenticated