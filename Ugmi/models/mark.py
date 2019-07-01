# -*- coding: utf-8 -*-
import os
import subprocess
import json
from random import randint
from flask import send_from_directory
from shutil import rmtree
from datetime import datetime
from Ugmi import db, app


class Mark(db.Model):
    __tablename__ = 'mark'
    id = db.Column(db.Integer, default=None, primary_key=True)
    title = db.Column(db.String(256))
    img = db.Column(db.String(2048))
    site = db.Column(db.String(2048))
    video = db.Column(db.String(2048), default=None)
    creation_time = db.Column(db.DateTime, default=datetime.utcnow())
    views = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='mark')
    __table_args__ = (
        db.PrimaryKeyConstraint('id'),
    )

    @property
    def mark_file(self):
        """Returns path to mark file."""
        return os.path.join(os.path.join(app.config['SMALL_MARKS_DIR'], str(self.id)), str(self.id) + app.config['SMALL_MARKS_EXTENSION'])

    def write_to_db(self):
        db.session.add(self)
        db.session.commit()

    def generate_mark(self):
        mark_dir = os.path.join(app.config['SMALL_MARKS_DIR'], str(self.id))
        mark_file = os.path.join(mark_dir, str(self.id) + app.config['SMALL_MARKS_EXTENSION'])
        if not os.path.isdir(mark_dir):
            os.mkdir(mark_dir)
        subprocess.call(['java', '-jar', app.config['SMALL_GENERATOR'], 'generate', str(self.id), mark_file])

    def get_mark(self):
        mark_dir = os.path.join(app.config['SMALL_MARKS_DIR'], str(self.id))
        mark_file = str(self.id) + app.config['SMALL_MARKS_EXTENSION']
        return send_from_directory(mark_dir, mark_file)

    def delete_files(self):
        json_mark_dir = os.path.join(app.config['SMALL_MARKS_JSON_DIR'], str(self.id))
        if os.path.isdir(json_mark_dir):
            rmtree(json_mark_dir)
        mark_dir = os.path.join(app.config['SMALL_MARKS_DIR'], str(self.id))
        if os.path.isdir(mark_dir):
            rmtree(mark_dir)

    # External server:
    def init_json(self):
        json_mark_dir = os.path.join(app.config['SMALL_MARKS_JSON_DIR'], str(self.id))
        json_mark_file = os.path.join(json_mark_dir, app.config['SMALL_MARKS_JSON_FILE'])
        if not os.path.isdir(json_mark_dir):
            os.mkdir(json_mark_dir)
        data = {'name': self.title, 'img': self.img, 'site': self.site, 'res': self.video}
        with open(json_mark_file, 'w') as json_file:
            json_file.write(json.dumps(data))

    # AJAX:
    def ajax_get_info(self):
        data = {
            'id': self.id,
            'title': self.title,
            'img': self.img,
            'site': self.site,
            'video': self.video,
            'views': self.views,
            'owner': (
                    str(self.user.id) + ' | ' + str(self.user.role)
                    + '(' + self.user.prefix + ')' + ' | '
                    + self.user.username + ' | ' + self.user.email
            )
        }
        return data

    @classmethod
    def get_unique_mark_id(cls):
        l, r = 0, 2 ** 30 - 1
        _id = randint(l, r)
        while db.session.query(Mark.query.filter(Mark.id == _id).exists()).scalar():
            _id = cls.get_unique_mark_id()
        return _id

    def __init__(self, **kwargs):
        self.id = Mark.get_unique_mark_id()
        super(Mark, self).__init__(**kwargs)
        self.generate_mark()
        self.init_json()

    def __repr__(self):
        return '<Mark %r title %r by user %r>' % (self.id, self.title, self.user_id)
