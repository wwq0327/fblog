#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    application.py
    ~~~~~~~~~~~~~~~~~~~~

    fblog 应用程序配置程序，处理程序的相关模块。
    
    :date: 2011-10-22
    :author: wwq0327 <wwq0327@gmail.com>
    :license: lgpl
"""

from datetime import datetime
import markdown

from flask import Flask

#from flaskext.gravatar import Gravatar
from fblog.config import Config, DevConfig, ProConfig
from fblog.extensions import db, login_manager

#导入相关视图模块
from fblog.views import blog, admin, account, feed
from fblog.models import Anonymous

__all__ = ['create_app']

# 默认应用程序名称，与应用程序目录名一致
DEFAULT_APP_NAME = 'fblog'

# 程序模块
DEFAULT_BLUEPRINTS = (
    (blog, ''),
    (admin, '/admin'),
    (account, '/account'),
    (feed, '/feed'),
    )

def create_app(config=None, app_name=None, blueprints=None):
    """创建应用程序配置"""

    if app_name is None:
        app_name = DEFAULT_APP_NAME

    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name)

    configure_app(app, config)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_templates(app)
    configure_login(app)

    return app

def configure_app(app, config):
    """调用运行环境配置"""

    app.config.from_object(DevConfig())

    if config is not None:
        app.config.from_object(config)

    app.config.from_envvar("APP_CONFIG", silent=True)

def configure_blueprints(app, blueprints):
    """程序模块"""

    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)

def configure_extensions(app):
    """扩展导入"""

    db.init_app(app)

def configure_login(app):
    login_manager.anonymouse = Anonymous
    login_manager.login_view = 'account.login'

    login_manager.setup_app(app)



def format_datetime(dbtime):
    """Format a timestamp for display."""
    return datetime.strftime(dbtime, '%Y-%m-%d %H:%M')

def format_text(content):
    return markdown.markdown(content)


def configure_templates(app):
    # 自订义的模板过滤器
    app.jinja_env.filters['datetimeformat'] = format_datetime
    app.jinja_env.filters['markdown'] = format_text
