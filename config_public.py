import os
project_dir  = os.path.dirname(__file__)
base_dir     = os.path.join(project_dir, 'Ugmi')
database_dir = os.path.join(base_dir, 'database')

#SQLAlchemy config
SQLALCHEMY_DATABASE_URI        = 'sqlite:///' + os.path.join(database_dir, 'main.db')
SQLALCHEMY_MIGRATE_REPO        = os.path.join(database_dir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

#Flask config
SECRET_KEY              = 'ur_secret_key'

#WTForms config
WTF_CSRF_SECRET_KEY     = 'ur_secret_key'

#Hash salts
SECRET_CONFIRM_EMAIL_SALT   = 'ur_secret_salt'
SECRET_PASSWORD_RESET_SALT  = 'ur_secret_salt'

#Serializer secret keys
SECRET_CONFIRM_EMAIL_KEY      = 'ur_secret_key'
SECRET_PASSWORD_RESET_KEY     = 'ur_secret_key'

#Email server config
MAIL_SERVER             = 'smtp.yandex.ru'
MAIL_PORT               = 465
MAIL_USE_TLS            = False
MAIL_USE_SSL            = True
MAIL_USERNAME           = 'ur_username'
MAIL_PASSWORD           = 'ur_password'

#Administrators list
ADMINS = ['admin1@gmail.com', 'admin2@gmail.com']

#Support mail
MAIL_SUPPORT = 'support@gmail.com'

#Log file
LOG_FILE = 'ugmi.log'
