#coding:utf-8
"""
    models/account.py
    ~~~~~~~~~~~~~~~~~~~~~~~~

    admin account

"""

from werkzeug import generate_password_hash, check_password_hash
from flaskext.login import AnonymousUser, UserMixin

from fblog.extensions import db

class Anonymous(AnonymousUser):
    name = u"Guest"

class User(db.Model):

    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    is_active = db.Column(db.Boolean())

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return self.username

    def store_to_db(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class LoginUser(UserMixin):
    def __init__(self, id, name, active=True):
        self.id = id
        self.name = name
        self.active = active

    def is_active(self):
        return self.active
    
