# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, jsonify, request, Response, redirect
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms import Form as wtForm
from dbORM import db,Searchrecord, User,Message,Findingchildren,Missingchildren,Fchildrenface,Childrenface
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
import time

def dashboard():


    admin.add_view(LoginView(User, db.session))

    admin.add_view(LoginView(Message, db.session))

    admin.add_view(FindingChildrenView(Findingchildren, db.session))

    admin.add_view(MissingChildrenView(Missingchildren, db.session))
    admin.add_view(FChildrenFaceView(Fchildrenface, db.session))
    admin.add_view(ChildrenFaceView(Childrenface, db.session))





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


def date_format(value):
    return time.strftime(u'%Y/%m/%d %H:%M:%S', time.localtime(float(value)))
class LoginView(ModelView):
    def is_accessible(self):
        # return flask_login.current_user.is_authenticated
        return 1

    def column_display_pk(self):
        return 1

class MissingChildrenView(LoginView):
    column_exclude_list=('bid','image','birthday','height','confirm_location','description','comment','login_time','volunteer','short_name')
    column_default_sort = ('created_at', True)
    form_extra_fields = {
        'status': SelectField(u'status', choices=[('open', u'发布'), ('pending', u'不发布')]),
    }
    column_formatters = dict(created_at=lambda v, c, m, p:date_format(m.created_at),missing_time=lambda v, c, m, p:date_format(m.missing_time))
class FindingChildrenView(LoginView):
    column_exclude_list=('img','source')
    column_formatters = dict(created_at=lambda v, c, m, p:date_format(m.created_at),finding_time=lambda v, c, m, p:date_format(m.finding_time))
    form_extra_fields = {
        'status': SelectField(u'status', choices=[('open', u'发布'), ('pending', u'不发布')]),
    }
    column_default_sort = ('created_at', True)
class FChildrenFaceView(LoginView):
    column_exclude_list=()

class ChildrenFaceView(LoginView):
    column_exclude_list=()
class MessageView(LoginView):
    form_extra_fields = {
        'status': SelectField(u'status', choices=[('open', u'发布'), ('pending', u'不发布')]),
    }
    column_formatters = dict(created_at=lambda v, c, m, p:date_format(m.created_at))
    column_default_sort = ('created_at', True)