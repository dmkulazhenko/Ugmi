# -*- coding: utf-8 -*-
from Ugmi import db, app




class Support_msg(db.Model):
    __tablename__ = 'support_msg'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    msg = db.Column(db.Text)
    date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Support_msg from %r with email %r left %r>' % (self.name, self.email, self.date)
