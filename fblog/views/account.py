#coding:utf-8

from flask import request, render_template, redirect, url_for, flash, Blueprint

from flaskext.login import (current_user, login_required, login_user,
                          logout_user, confirm_login,
                          fresh_login_required)

from fblog.extensions import login_manager

from fblog.models import Anonymous, User, LoginUser
from fblog.forms import LoginForm
from fblog.views import admin

account = Blueprint("account", __name__)

@login_manager.user_loader
def load_user(id):
    try:
        return LoginUser(int(id), User.query.get(id).username)
    except:
        return None

@account.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = 1

        user = User.query.filter_by(username=username).first()
        if not len(form.errors):
            if user and user.check_password(password):
                loginuser = LoginUser(user.id, user.username)
                if login_user(loginuser, remember=remember):
                    #flash(u"登录成功")
                    return redirect(request.args.get('next') or url_for("admin.index"))
                ## else:
                ##     flash(u"登录失败")
            else:
                flash(u"用户名不存在，或与密码不匹配")

    return render_template("admin/login.html", form=form)

@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u"你已退出后台管理界面，如需进行设置请登录")
    return redirect(url_for('account.login'))
