#coding:utf-8

import os

_HERE = os.path.dirname(__file__)
_DB_SQLITE_PATH = os.path.join(_HERE, 'fblog.sqlite')

_DBUSER = "root"  # 数据库用户名
_DBPASS = "123"  # 数据库用户名密码
_DBHOST = "localhost"  # 服务器
_DBNAME = "fblog"  # 数据库名称

PER_PAGE = 5  # 每页显示文章数
MN_PER_PAGE = 10 # 后台管理中每页文章列表数

#_BLOG_NAME = "FBlog Project" # Blog名称

class Config(object):
    SECRET_KEY = '\xb5\xc8\xfb\x18\xba\xc7*\x03\xbe\x91{\xfd\xe0L\x9f\xe3\\\xb3\xb1P\xac\xab\x061'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % _DB_SQLITE_PATH
    BABEL_DEFAULT_TIMEZONE = 'Asia/Chongqing'


class ProConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % (_DBUSER, _DBPASS, _DBHOST, _DBNAME)

class DevConfig(Config):
    DEBUG = True

class TestConfig(Config):
    TESTING = True

    
