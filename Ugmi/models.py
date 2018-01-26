# -*- coding: utf-8 -*-
import bcrypt, os, subprocess
from itsdangerous import URLSafeTimedSerializer
from flask import url_for, send_from_directory
from datetime import datetime
from Ugmi import db, app
from .emails import confirm_email_notification, password_reset_notification
from config import ROLE_DEFAULT, ROLE_USER, ROLE_ADVANCED, ROLE_COW, ROLE_ADMIN, ROLE, SMALL_MARKS_DIR, SMALL_GENERATOR, SMALL_MARKS_EXTENSION




CONFIRM_FALSE = 0
CONFIRM_TRUE  = 1

TOKEN_EXPRIRATION_TIME = 3600




class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(256))
    name = db.Column(db.String(64))
    role = db.Column(db.Integer, default = ROLE_DEFAULT)
    custom_marks_limit = db.Column(db.Integer, default = None)
    confirmed = db.Column(db.Integer, default = CONFIRM_FALSE)
    last_email_confirm = db.Column(db.DateTime, default = None)
    last_password_reset = db.Column(db.DateTime, default = None)
    last_seen = db.Column(db.DateTime, default = None)
    marks = db.relationship('Mark', backref = 'user')


    @property
    def is_authenticated(self):
        '''Return True if user is authenticated.'''
        return True

    @property
    def is_active(self):
        '''Returns True if user is active.'''
        return True

    @property
    def is_anonymous(self):
        '''Returns True if user is anonymous.'''
        return False

    @property
    def is_admin(self):
        '''Return True if user is admin'''
        return ( self.role == ROLE_ADMIN )

    @property
    def max_marks(self):
        '''How many marks current user can have?'''
        if self.custom_marks_limit == None:
            return ROLE['MAX_MARKS'][self.role]
        return self.custom_marks_limit

    @property
    def have_marks(self):
        '''Number of marks for current user.'''
        return len(self.marks)

    @property
    def is_marks_limit_exceeded(self):
        '''Returns True if marks limit for current user exceeded.'''
        return ( self.have_marks >= self.max_marks )

    @property
    def prefix(self):
        '''Returns user prefix based on role.'''
        return ROLE['PREFIX'][self.role]

    def get_id(self):
        '''Returns user id'''
        try:
            return str(self.id) #python3
        except:
            return unicode(self.id) #python2


    def auth(self, password):
        '''Returns true if password match for current user.'''
        return ( bytes(self.password, 'utf-8') == bcrypt.hashpw( bytes(password, 'utf-8'), bytes(self.password, 'utf-8') ) )


    def send_email_confirm_token(self):
        '''Creates email confirm token, using itsdangerous serializer.
        Sends email for user with email confirm token.'''
        serializer = URLSafeTimedSerializer(app.config['SECRET_CONFIRM_EMAIL_KEY'])
        token = serializer.dumps(self.email, salt = app.config['SECRET_CONFIRM_EMAIL_SALT'])
        confirm_email_url = url_for('confirm_email', token = token, _external = True)
        confirm_email_notification(user = self, confirm_email_url = confirm_email_url)

    @staticmethod
    def check_email_confirm_token(token, expiration = TOKEN_EXPRIRATION_TIME):
        '''Checks token, considering expiration time.'''
        serializer = URLSafeTimedSerializer(app.config['SECRET_CONFIRM_EMAIL_KEY'])
        try:
            email = serializer.loads(
                token,
                salt = app.config['SECRET_CONFIRM_EMAIL_SALT'],
                max_age = expiration
            )
        except:
            return False
        return email


    def send_password_reset_token(self):
        '''Creates password reset token, using itsdangerous serializer.
        Sends email for user with password reset token.'''
        serializer = URLSafeTimedSerializer(app.config['SECRET_PASSWORD_RESET_KEY'])
        token = serializer.dumps(self.email, salt = app.config['SECRET_PASSWORD_RESET_SALT'])
        password_reset_url = url_for('reset_password_confirm', token = token, _external = True)
        password_reset_notification(user = self, password_reset_url = password_reset_url)

    @staticmethod
    def check_password_reset_token(token, expiration = TOKEN_EXPRIRATION_TIME):
        '''Checks token, considering expiration time.'''
        serializer = URLSafeTimedSerializer(app.config['SECRET_PASSWORD_RESET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt = app.config['SECRET_PASSWORD_RESET_SALT'],
                max_age = expiration
            )
        except:
            return False
        return email


    #AJAX:
    def ajax_get_info(self):
        data = {}
        data['id'] = self.id
        data['username'] = self.username
        data['email'] = self.email
        data['name'] = self.name
        data['role'] = self.role
        data['prefix'] = self.prefix
        data['marks'] = []
        for mark in self.marks:
            data['marks'].append(mark.id)
        data['num_marks'] = self.have_marks
        data['max_marks'] = self.max_marks
        data['confirmed'] = self.confirmed
        return data


    def __repr__(self):
        return '<User %r name %r email %r>' % (self.username, self.name, self.email)



class Mark(db.Model):
    __tablename__ = 'mark'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(256))
    img = db.Column(db.String(2048))
    site = db.Column(db.String(2048))
    video = db.Column(db.String(2048), default = None)
    creation_time = db.Column(db.DateTime, default = datetime.utcnow())
    views = db.Column(db.Integer, default = 0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    __table_args__ = (
        db.PrimaryKeyConstraint('id'),
    )


    @property
    def mark_file(self):
        '''Returns path to mark file.'''
        return os.path.join(os.path.join(SMALL_MARKS_DIR, str(self.id)), str(self.id) + SMALL_MARKS_EXTENSION)


    def generate_mark(self):
        mark_dir = os.path.join(SMALL_MARKS_DIR, str(self.id))
        mark_file = os.path.join(mark_dir, str(self.id) + SMALL_MARKS_EXTENSION)
        if not os.path.isdir(mark_dir):
            os.mkdir(mark_dir)
        if os.path.isfile(mark_file):
            return
        subprocess.call(['java', '-jar', SMALL_GENERATOR, 'generate', str(self.id), mark_file])
        return


    def get_mark(self):
        mark_dir = os.path.join(SMALL_MARKS_DIR, str(self.id))
        mark_file = str(self.id) + SMALL_MARKS_EXTENSION
        return send_from_directory(mark_dir, mark_file)


    #AJAX:
    def ajax_get_info(self):
        data = {}
        data['id'] = self.id
        data['title'] = self.title
        data['img'] = self.img
        data['site'] = self.site
        data['video'] = self.video
        data['views'] = self.views
        data['owner'] = str(self.user.id) + ' | ' + str(self.user.role) + '(' + self.user.prefix + ')' + ' | ' + self.user.username + ' | ' + self.user.email
        return data


    def __init__(self, **kwargs):
        super(Mark, self).__init__(**kwargs)
        self.generate_mark()

    def __repr__(self):
        return '<Mark %r title %r by user %r>' % (self.id, self.title, self.user_id)



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
