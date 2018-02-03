# -*- coding: utf-8 -*-
import bcrypt, json
from itsdangerous import BadSignature, SignatureExpired
from flask import url_for
from datetime import datetime
from Ugmi import db, app, email_confirm_serializer, password_reset_serializer, api_token_serializer
from Ugmi.emails import confirm_email_notification, password_reset_notification




class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(256))
    name = db.Column(db.String(64))
    role = db.Column(db.Integer, default = app.config['ROLE_DEFAULT'])
    custom_marks_limit = db.Column(db.Integer, default = None)
    confirmed = db.Column(db.Integer, default = app.config['EMAIL_CONFIRM_FALSE'])
    last_email_confirm = db.Column(db.DateTime, default = None)
    last_password_reset = db.Column(db.DateTime, default = None)
    last_seen = db.Column(db.DateTime, default = None)
    marks = db.relationship('Mark', backref = 'user')
    comments = db.relationship('Comment', backref = 'user')


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
        return ( self.role == app.config['ROLE_ADMIN'] )

    @property
    def max_marks(self):
        '''How many marks current user can have?'''
        if self.custom_marks_limit == None:
            return app.config['ROLE']['MAX_MARKS'][self.role]
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
        return app.config['ROLE']['PREFIX'][self.role]

    def get_id(self):
        '''Returns user id'''
        try:
            return str(self.id) #python3
        except:
            return unicode(self.id) #python2

    def write_to_db(self):
        db.session.add(self)
        db.session.commit()


    def auth(self, password):
        '''Returns true if password match for current user.'''
        return ( bytes(self.password, 'utf-8') == bcrypt.hashpw( bytes(password, 'utf-8'), bytes(self.password, 'utf-8') ) )


    def send_email_confirm_token(self):
        '''Creates email confirm token, using itsdangerous serializer.
        Sends email for user with email confirm token.'''
        token = email_confirm_serializer.dumps(self.email, salt = app.config['SECRET_CONFIRM_EMAIL_SALT'])
        confirm_email_url = url_for('confirm_email', token = token, _external = True)
        confirm_email_notification(user = self, confirm_email_url = confirm_email_url)
        self.last_email_confirm = datetime.utcnow()
        self.write_to_db()

    @staticmethod
    def check_email_confirm_token(token, expiration = app.config['TOKEN_EXPRIRATION_TIME']):
        '''Checks token, considering expiration time.'''
        try:
            email = email_confirm_serializer.loads(
                token,
                salt = app.config['SECRET_CONFIRM_EMAIL_SALT'],
                max_age = expiration
            )
        except:
            return None
        return email


    def confirm_email(self):
        self.confirmed = app.config['EMAIL_CONFIRM_TRUE']


    def send_password_reset_token(self):
        '''Creates password reset token, using itsdangerous serializer.
        Sends email for user with password reset token.'''
        token = password_reset_serializer.dumps(self.email, salt = app.config['SECRET_PASSWORD_RESET_SALT'])
        password_reset_url = url_for('reset_password_confirm', token = token, _external = True)
        password_reset_notification(user = self, password_reset_url = password_reset_url)
        self.last_password_reset = datetime.utcnow()
        self.write_to_db()

    @staticmethod
    def check_password_reset_token(token, expiration = app.config['TOKEN_EXPRIRATION_TIME']):
        '''Checks token, considering expiration time.'''
        try:
            email = password_reset_serializer.loads(
                token,
                salt = app.config['SECRET_PASSWORD_RESET_SALT'],
                max_age = expiration
            )
        except:
            return None
        return email


    #API:
    def get_api_token(self):
        '''Returns api token, which generates using itsdangerous serializer.'''
        data = {}
        data['id'] = str(self.id)
        data['password'] = self.password
        return api_token_serializer.dumps(data, salt = app.config['SECRET_API_TOKEN_SALT']).decode('utf-8')

    @staticmethod
    def check_api_token(token):
        try:
            data = api_token_serializer.loads(token, salt = app.config['SECRET_API_TOKEN_SALT'])
        except SignatureExpired:
            return 'expired' # valid token, but expired
        except BadSignature:
            return 'invalid' # invalid token
        user = User.query.get(data['id'])
        if(user.password != data['password']):
            return 'expired'
        return user


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
