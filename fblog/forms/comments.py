#!/usr/bin/env python
#coding:utf-8

from flaskext.wtf import Form, TextField, TextAreaField, SubmitField, required
from flaskext.wtf.html5 import URLField, EmailField
class CommentsForm(Form):
    name = TextField(u"Name(必填)", validators=[required(message=u'必填')])
    #email = TextField(u"Email", validators=[required(message=u'必填，邮箱不会被公开')])
    #website = TextField(u"Site")
    email = EmailField(u"Email(必填，不公开)", validators=[required(message=u'必填内容')])
    website = URLField(u"Site")
    comments = TextAreaField(u"Comment", validators=[required(message=u'内容必填')])
    submit = SubmitField(u"Comment")
