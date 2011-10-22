#Blog by Flask

## 简介
个人博客程序，具备基本的博客浏览发布评论及简单的管理功能。由于尚在开发中，所以数据使用的是轻量级的SQLite，如果需要使用MySQL，需另外配置。

## 运行要求
- Python 2.5+ 
- Flask 0.7+

## 安装插件

- markdown
- flask-script
- flask-login
- flask-sqlalchemy
- flask-wtf

## 运行

### 初始化数据库

- python run.py creatall

### 启动

- python run.py runserver

### 运行

- 在浏览器中打开: http://127.0.0.1:8888

## MySQL

如果选择MySQL作为数据库，则需要下面的一些配置。

### 数据库信息

- _DBUSER = ""  # 数据库用户名
- _DBPASS = ""  # 数据库用户名密码
- _DBHOST = "localhost"  # 服务器 默认 localhost
- _DBNAME = "fblog"  # 数据库名称 默认 fblog

### 数据库选择

修改 fblog/__init__.py 文件：

- app.config.from_object('fblog.config.DevConfig') # sqlite
- app.config.from_object('fblog.config.ProConfig') #mysql

确定数据库后，去掉其中一个代码前面的 # ，另一个刚加上　#

### 创建MySQL数据库

两步走：

- mysql -pUSER -p # USER为数据库用户名，键入相应密码进入下一步。
- create database fblog;

## 创建用户

执行命令：

- python run.py createuser

键入用户名，邮箱，密码后，即可创建成功，后台管理即可用相应的用户名及密码登录进行管理。

## 关于博客名称

修办法，可以 fblog/templates下的 "_blog_name.html" 中的换称换掉即可，只需一行。（暂时没找到通过配置文件修改的办法，先这样了。）