#coding:utf-8
"""
    views/blog.py
    ~~~~~~~~~~~~~~~~~~~

    Blog 视图函数
    :copyright: 2011 wwq0327
    :license: LGPL
"""
from markdown import markdown

from flask import Module, render_template, request, url_for, redirect, flash, abort, Blueprint
from flaskext.sqlalchemy import Pagination
from fblog import config
from fblog.extensions import db
from fblog.forms import PostForm, CommentsForm
from fblog.models import Post, Comments, Tag

## blog = Module(__name__)
blog = Blueprint("blog", __name__)

@blog.route('/')
@blog.route('/page/<int:page>')
def index(page=1):
    if page < 1: page = 1
    
    topwz = Post.query.order_by('-id').limit(10)
    topcs = Comments.query.order_by('-id').limit(10)
    page_obj = Post.query.order_by("-id").paginate(page, per_page=config.PER_PAGE)
    page_url = lambda page: url_for("blog.index", page=page)
    
    return render_template('index.html', page_obj=page_obj, page_url=page_url, topwz=topwz, topcs=topcs)

@blog.route('/tag/<tag>', defaults={'page':1})
@blog.route('/tag/<tag>/<int:page>')
def show_tag(tag, page):
    topwz = Post.query.order_by('-id').limit(10)
    topcs = Comments.query.order_by('-id').limit(10)
    tag = Tag.query.filter_by(name=tag).first() or abort(404)
    posts = tag.post.order_by(Post.id.desc())
    items = posts.limit(config.PER_PAGE).offset((page-1)*config.PER_PAGE).all()
    page_obj = Pagination(posts, page=page, per_page=config.PER_PAGE,
                          total=posts.count(), items=items)
    #page_obj = tag.post.order_by(Post.id.desc()).paginate(page, pre_page=config.PER_PAGE)
    page_url = lambda page: url_for("blog.show_tag", page=page, tag=tag)

    flash("Posts tagged with '%s'" % tag.name)
    return render_template('index.html', page_obj=page_obj, page_url=page_url, topwz=topwz, topcs=topcs)
                                                     
@blog.route('/post/<int:id>/entry', methods=['GET', 'POST'])
def entry(id):
    form = CommentsForm(request.form)
    topwz = Post.query.order_by("-id").limit(10)
    topcs = Comments.query.order_by('-id').limit(10)
    page = Post.query.filter_by(id=id).first()
    cs = Comments.query.filter_by(eid=id)

    if request.method == 'POST' and form.validate_on_submit():
        eid = id
        name = form.name.data
        email = form.email.data
        website = form.website.data
        comments = form.comments.data

        c = Comments(eid=eid,
                     name=name,
                     email=email,
                     website=website,
                     comments=comments)
        try:
            c.store_to_db()
            flash(u'评论成功')
        except:
            flash(u'失败')

        return redirect(url_for('blog.entry', id=id))

    return render_template('/entry.html', page=page, topwz=topwz, form=form, cs=cs, topcs=topcs)
