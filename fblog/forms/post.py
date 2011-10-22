#!/usr/bin/env python
#coding:utf-8

from flaskext.wtf import Form, TextField, TextAreaField, SubmitField, required

class PostForm(Form):
    title = TextField(u'标题', validators=[required(message=u'标题')])
    content = TextAreaField(u'内容', validators=[required(message=u'content')])
    tags = TextField(u"Tags")
    submit = SubmitField(u'发布')
