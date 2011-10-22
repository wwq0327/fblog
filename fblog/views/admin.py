#coding:utf-8
"""
    views/admin.py
    ~~~~~~~~~~~~~~~~~~~

    Blog 管理视图函数
    :copyright: 2011 wwq0327
    :license: LGPL
"""

from flask import Module, render_template, request, url_for, redirect, flash, abort, Blueprint
from flaskext.login import login_required

from fblog import config
from fblog.extensions import db
from fblog.forms import PostForm, CommentsForm
from fblog.models import Post, Comments
from fblog.helpers import normalize_tags

## admin = Module(__name__)
admin = Blueprint("admin", __name__)

@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html', postc=len(Post.query.all()),
                           commentc=len(Comments.query.all()))
@admin.route('/addpost', methods=['GET', 'POST'])
@login_required
def addpost():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        tags = normalize_tags(form.tags.data)
        entry = Post(title=title, content=content)
        entry.tags = tags
        try:
            entry.store_to_db()
            flash(u'文章存入成功')
        except:
            flash(u'文章存入失败，请与管理员联系')

        return redirect(url_for('admin.index'))
            
    return render_template('admin/addpost.html', form=form)

@admin.route('/mnpost')
@admin.route('/mnpost/<int:page>')
@login_required
def mnpost(page=1):
    if page < 1: page = 1
    
    page_obj = Post.query.order_by('-id').paginate(page, per_page=config.MN_PER_PAGE)
    page_url = lambda page: url_for("admin.mnpost", page=page)

    return render_template('admin/mnpost.html', page_obj=page_obj, page_url=page_url)

@admin.route('/<int:id>/del')
@login_required
def delpost(id):
    entry = Post.query.filter_by(id=id).first()
    if not entry:
        abort(404)

    entry.delete_from_db()

    return redirect(url_for('admin.mnpost'))
        
@admin.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    entry = Post.query.filter_by(id=id).first()
    if not entry:
        abort(404)

    taglist = []
    for tag in entry.tags:
        taglist.append(tag.name)

    form = PostForm(title=entry.title, content=entry.content, tags=','.join(taglist))
    if request.method == 'POST' and form.validate_on_submit():
        Post.query.filter_by(id=id).update({
            Post.title: request.form['title'],
            Post.content: request.form['content'],
            Post.tags: request.form['tags']})
        db.session.commit()
        return redirect(url_for('admin.mnpost'))

    return render_template('admin/edit.html', form=form)

@admin.route('/mncomment')
@admin.route('/mncomment/<int:page>')
@login_required
def mncomment(page=1):
    if page < 1: page = 1

    comm_obj = Comments.query.order_by('-id').paginate(page, per_page=config.MN_PER_PAGE)
    comm_url = lambda page: url_for("admin.mncomment", page=page)

    return render_template('admin/mncomment.html', comm_obj=comm_obj, comm_url=comm_url)

@admin.route('/<int:id>/delcomm')
@login_required
def delcomm(id):
    cs = Comments.query.filter_by(id=id).first()
    db.session.delete(cs)
    db.session.commit()

    return redirect(url_for("admin.mncomment"))

@admin.route('/<int:id>/editcomm')
@login_required
def editcomm(id):
    pass

@admin.route('/settings')
@login_required
def settings():
    return render_template('admin/settings.html')
