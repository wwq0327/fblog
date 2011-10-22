#coding:utf-8
"""
   feeds.py
   ~~~~~~~~~~~~~~~~~~
   RSS输出

   参考代码： https://github.com/laoqiu/pypress/blob/master/pypress/views/feeds.py
   :license: LGPL
"""

from werkzeug.contrib.atom import AtomFeed

from flask import Module, request, url_for

from fblog.models import Post

feed = Module(__name__)

class PostFeed(AtomFeed):
    def add_post(self, post):

        self.add(post.title,
                 unicode(post.content),
                 content_type='html',
                 author='wwq0327',
                 url=url_for('blog.entry', id=post.id),
                 updated=post.posted_on)

@feed.route('/')
def index():
    feed = PostFeed("FBlog Project blog",
                    feed_url=request.url,
                    url=request.url_root)

    posts = Post.query.order_by('posted_on desc').limit(10)
    for post in posts:
        feed.add_post(post)

    return feed.get_response()

    
                 
