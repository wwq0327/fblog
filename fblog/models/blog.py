#!/usr/bin/env python
#coding:utf-8

from datetime import datetime

from fblog.extensions import db

post_tag = db.Table('post_tag', # 关联表名称
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                    )

class Post(db.Model):

    __tablename__ = 'post'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted_on = db.Column(db.DateTime, default=datetime.now)

    _tags = db.relationship('Tag', secondary=post_tag,
                           backref=db.backref('post', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

    def _set_tags(self, taglist):
        self._tags = []
        for tag_name in taglist:
            self._tags.append(Tag.get_or_create(tag_name))

    def _get_tags(self):
        return self._tags

    tags = db.synonym("_tags", descriptor=property(_get_tags, _set_tags))

    def __repr__(self):
        return "<Post %s>" % self.title

    def store_to_db(self):

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Tag(db.Model):
    __tablename__ = 'tag'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))

    @classmethod
    def get_or_create(cls, tag_name):
        tag = cls.query.filter(cls.name==tag_name).first()
        if not tag:
            tag = cls(tag_name)
        return tag

    def __init__(self, name):
        self.name = name
    
