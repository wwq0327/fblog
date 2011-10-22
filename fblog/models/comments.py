#!/usr/bin/env python
#coding:utf-8

from datetime import datetime

from fblog.extensions import db

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.Integer)
    name = db.Column(db.String(48), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    website = db.Column(db.String(60))
    comments = db.Column(db.Text)
    commented_on = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        super(Comments, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<Name %s>" % self.name

    def store_to_db(self):

        db.session.add(self)
        db.session.commit()
    
    
