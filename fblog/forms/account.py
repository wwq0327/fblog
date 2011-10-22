#coding:utf-8

from flaskext.wtf import Form, TextField, PasswordField, BooleanField,\
     SubmitField, required

class LoginForm(Form):
    username = TextField(u"用户名", validators=[required()])
    password = PasswordField(u"密码", validators=[required()])
    submit = SubmitField(u"登录")
