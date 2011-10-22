#coding:utf-8

from flaskext.sqlalchemy import SQLAlchemy
#from flaskext.script import Manager
from flaskext.babel import Babel
#from flaskext.gravatar import Gravatar
from flaskext.login import LoginManager
db = SQLAlchemy()
#manager = Manager()
babel = Babel()
#G = Gravatar()
login_manager = LoginManager()
