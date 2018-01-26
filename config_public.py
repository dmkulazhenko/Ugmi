# -*- coding: utf-8 -*-
import os

project_dir = os.path.dirname(__file__)
base_dir = os.path.join(project_dir, 'Ugmi')
database_dir = os.path.join(base_dir, 'database')
marks_dir = os.path.join(base_dir, 'marks')

#Flask config
DEBUG = True
SECRET_KEY = ''

#WTForms config
WTF_CSRF_SECRET_KEY = ''

#Hash salts
SECRET_CONFIRM_EMAIL_SALT = ''
SECRET_PASSWORD_RESET_SALT = ''

#Serializer secret keys
SECRET_CONFIRM_EMAIL_KEY = ''
SECRET_PASSWORD_RESET_KEY = ''

#SQLAlchemy config
if not DEBUG:
    SQLALCHEMY_DATABASE_URI = 'mysql://apps:@localhost/apps'
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(database_dir, 'main.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False


#Email server config
MAIL_SERVER = ''
MAIL_PORT = 444
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 'no-reply@ugmi.me'
MAIL_PASSWORD = ''

#Administrators list
ADMINS = ['dimkaxdx@gmail.com', 'derovi@list.ru', 'vladislav.oleshko@gmail.com', 'headsli@yandex.ru']

#Support mail
MAIL_SUPPORT = 'support@ugmi.me'

#Roles
ROLE_DEFAULT = 0
ROLE_USER = 1
ROLE_ADVANCED = 2
ROLE_COW = 3
ROLE_ADMIN = 4
ROLE = {
    'MAX_MARKS' : {
        ROLE_DEFAULT : 2,
        ROLE_USER : 4,
        ROLE_ADVANCED : 10,
        ROLE_COW : 30,
        ROLE_ADMIN : 2**31
    },
    'PREFIX' : {
        ROLE_DEFAULT : u'новичок',
        ROLE_USER : u'пользователь',
        ROLE_ADVANCED : u'продвинутый',
        ROLE_COW : u'сотрудник',
        ROLE_ADMIN : u'разработчик'
    }
}

#Log file
LOG_FILE = 'ugmi.log'

#Small marks
SMALL_GENERATOR = os.path.join(marks_dir, 'small_generator.jar')
SMALL_MARKS_DIR = os.path.join(marks_dir, 'small')
SMALL_MARKS_EXTENSION = '.png'
