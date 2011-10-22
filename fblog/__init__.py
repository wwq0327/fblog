#coding:utf-8

from datetime import datetime
import markdown

from flask import Flask, render_template, g ,request
from flaskext.gravatar import Gravatar
from flaskext.babel import Babel

from fblog.views import blog, admin, account, login_manager, feed
from fblog.extensions import db

def format_datetime(dbtime):
    """Format a timestamp for display."""
    return datetime.strftime(dbtime, '%Y-%m-%d %H:%M')

def format_text(content):
    return markdown.markdown(content)

app = Flask(__name__)

app.config.from_object('fblog.config.DevConfig') # sqlite
#app.config.from_object('fblog.config.ProConfig') #mysql
babel = Babel(app)

app.register_module(blog)
app.register_module(admin, url_prefix='/admin')
app.register_module(account, url_prefix='/account')
app.register_module(feed, url_prefix='/feed')

login_manager.setup_app(app)
db.init_app(app)

# 根据Email产生头像
gravatar = Gravatar(app,
                    size=36,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_404.html'), 404

@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

# 自订义的模板过滤器
app.jinja_env.filters['datetimeformat'] = format_datetime
app.jinja_env.filters['markdown'] = format_text
