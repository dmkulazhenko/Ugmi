# -*- coding: utf-8 -*-
import bcrypt
from itsdangerous import URLSafeTimedSerializer
from flask import url_for
from datetime import datetime
from Ugmi import db, app
from .emails import confirm_email_notification, password_reset_notification
from config import ROLE_USER, ROLE_ADMIN




CONFIRM_FALSE = 0
CONFIRM_TRUE  = 1

TOKEN_EXPRIRATION_TIME = 3600




class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(256))
    name = db.Column(db.String(64))
    role = db.Column(db.Integer, default = ROLE_USER)
    confirmed = db.Column(db.Integer, default = CONFIRM_FALSE)
    last_email_confirm = db.Column(db.DateTime, default = None)
    last_password_reset = db.Column(db.DateTime, default = None)
    last_seen = db.Column(db.DateTime, default = None)


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
        return (self.role == ROLE_ADMIN)

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


    def __repr__(self):
        return '<User %r name %r email %r>' % (self.username, self.name, self.email)




class Support_msg(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    msg = db.Column(db.Text)
    date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Support_msg from %r with email %r left %r>' % (self.name, self.email, self.date)
