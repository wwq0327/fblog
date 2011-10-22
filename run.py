#!/usr/bin/env python
#coding:utf-8

"""
    run.py
    ~~~~~~~~~~~

    主程序，创建数据库，用户帐号，启动服务器。

    :copyright: (c) 2011 by wwq0327 <wwq0327@gmail.coom>
    :license: LGPL
"""
from flask import current_app

from flaskext.script import Manager, Server, prompt_bool, prompt, prompt_pass

from fblog import app, db
from fblog.models import User, Post, Comments, Tag

manager = Manager(app)

server = Server(host='127.0.0.1', port=8888)
manager.add_command("runserver", server)

@manager.option('-u', '--username', dest='username', required=False)
@manager.option('-p', '--password', dest='password', required=False)
@manager.option('-e', '--email', dest='email', required=False)
def createuser(username=None, password=None, email=None):
    """
    Create new user
    """

    if username is None:
        while True:
            username = prompt("Username")
            user = User.query.filter(User.username==username).first()
            if user is not None:
                print "Username %s is already taken" % username
            else:
                break
 
    if email is None:
        while True:
            email = prompt("Email")
            user = User.query.filter(User.email==email).first()
            if user is not None:
                print "Email %s is already taken" % email
            else:
                break

    if password is None:
        password = prompt_pass("Password")
        
        while True:
            password_again = prompt_pass("Password again")
            if password != password_again:
                print "Password do not match"
            else:
                break

    user = User(username, None, email)
    user.set_password(password)
    user.store_to_db()

    print "User created with ID", user.id

@manager.command
def createall():
    db.create_all()

@manager.command
def dropall():

    if prompt_bool("Are you sure? You will lose all your DATA!"):
        db.drop_all()

@manager.shell
def make_shell_context():
    return dict(app=current_app,
                db=db,
                Post=Post,
                Tag = Tag,
                User=User,
                Comments=Comments)

if __name__ == '__main__':
    manager.run()
