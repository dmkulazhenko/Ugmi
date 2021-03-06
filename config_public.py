# -*- coding: utf-8 -*-
import os

project_dir = os.path.dirname(__file__)
base_dir = os.path.join(project_dir, 'Ugmi')
marks_dir = os.path.join(base_dir, 'marks')
temp_dir = os.environ.get("TEMP_DIR", os.path.join(base_dir, 'temp'))

# Flask config
DEBUG = bool(int(os.environ.get("DEBUG", 1)))
SECRET_KEY = os.environ.get("SECRET_KEY")

# WTForms config
WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY")

# Hash salts
SECRET_CONFIRM_EMAIL_SALT = os.environ.get("SECRET_CONFIRM_EMAIL_SALT")
SECRET_PASSWORD_RESET_SALT = os.environ.get("SECRET_PASSWORD_RESET_SALT")
SECRET_API_TOKEN_SALT = os.environ.get("SECRET_API_TOKEN_SALT")

# Serializer secret keys
SECRET_CONFIRM_EMAIL_KEY = os.environ.get("SECRET_CONFIRM_EMAIL_KEY")
SECRET_PASSWORD_RESET_KEY = os.environ.get("SECRET_PASSWORD_RESET_KEY")
SECRET_API_TOKEN_KEY = os.environ.get("SECRET_API_TOKEN_KEY")

# SQLAlchemy config
if not DEBUG:
    MYSQL_CREDENTIALS = (
        os.environ.get("MYSQL_CONNECTOR"),
        os.environ.get("MYSQL_USER"),
        os.environ.get("MYSQL_PASSWORD"),
        os.environ.get("MYSQL_HOST"),
        os.environ.get("MYSQL_DATABASE"),
    )
    if all(MYSQL_CREDENTIALS):
        SQLALCHEMY_DATABASE_URI = "mysql+{}://{}:{}@{}/{}".format(
            *MYSQL_CREDENTIALS
        )
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        project_dir, 'main.db'
    )

SQLALCHEMY_MIGRATIONS_DIR = (
    os.environ.get("SQLALCHEMY_MIGRATIONS_DIR") or "migrations"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Tokens
TOKEN_EXPRIRATION_TIME = 3600
API_TOKEN_EXPRIRATION_TIME = 2592000

# Email confirm
EMAIL_CONFIRM_TRUE = 1
EMAIL_CONFIRM_FALSE = 0

# Email server config
MAIL_SERVER = 'smtp.yandex.ru'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

# Administrators list
ADMINS = []

# Support mail
MAIL_SUPPORT = 'ugmi@xionix.xyz'

# Roles
ROLE_DEFAULT = 0
ROLE_USER = 1
ROLE_ADVANCED = 2
ROLE_COW = 3
ROLE_ADMIN = 4
ROLE = {
    'MAX_MARKS': {
        ROLE_DEFAULT: 2,
        ROLE_USER: 4,
        ROLE_ADVANCED: 10,
        ROLE_COW: 30,
        ROLE_ADMIN: 2 ** 31
    },
    'PREFIX': {
        ROLE_DEFAULT: u'новичок',
        ROLE_USER: u'пользователь',
        ROLE_ADVANCED: u'продвинутый',
        ROLE_COW: u'сотрудник',
        ROLE_ADMIN: u'разработчик'
    }
}

# Log file
LOG_FILE = 'ugmi.log'

# Small marks
SMALL_GENERATOR = os.path.join(marks_dir, 'small_generator.jar')
SMALL_MARKS_DIR = os.environ.get("DATA_DIR", os.path.join(marks_dir, 'small'))
SMALL_MARKS_EXTENSION = '.png'
SMALL_MARKS_JSON_DIR = SMALL_MARKS_DIR
SMALL_MARKS_JSON_FILE = 'data.json'
