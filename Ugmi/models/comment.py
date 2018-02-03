# -*- coding: utf-8 -*-
from datetime import datetime

from Ugmi import db





class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(2048))
    stars = db.Column(db.Integer, default = 0)
    creation_time = db.Column(db.DateTime, default = datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mark_id = db.Column(db.Integer, db.ForeignKey('mark.id'))

    def write_to_db(self):
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return '<Comment %r with %r stars, for mark %r by user %r>' % (self.id, self.stars, self.mark_id, self.user.username)
