#coding:utf-8

from flask import Module, request, render_template, redirect, url_for, flash, Blueprint

from flaskext.login import (LoginManager, current_user, login_required, login_user,
                          logout_user, UserMixin, AnonymousUser, confirm_login,
                          fresh_login_required)

from fblog.models import Anonymous, User, LoginUser
from fblog.forms import LoginForm
from fblog.views import admin

## account = Module(__name__)
account = Blueprint("account", __name__)

login_manager = LoginManager()
login_manager.anonymous_user = Anonymous
login_manager.login_view = 'account.login'
login_manager.login_message = u'你需要登录后才能进行下一步操作'
## login_manager.refresh_view = 'fblog.views.account.reauth'

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

## @account.route('/reauth', methods=['GET', 'POST'])
## @login_required
## def reauth():
##     if request.method == 'POST':
##         confirm_login()
##         flash(u"用户认证")
##         return redirect(request.args.get('next') or url_for('blog.index'))
##     return render_template('admin/reauth.html')

@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u"你已退出后台管理界面，如需进行设置请登录")
    return redirect(url_for('account.login'))
