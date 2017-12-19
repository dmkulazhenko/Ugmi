import os
project_dir                    = os.path.dirname(__file__)
base_dir                       = os.path.join(project_dir, 'Ugmi')
database_dir                   = os.path.join(base_dir, 'database')
generators_dir                 = os.path.join(base_dir, 'generators')

#Flask config
DEBUG                          = True
SECRET_KEY                     = ''

#WTForms config
WTF_CSRF_SECRET_KEY            = ''

#Hash salts
SECRET_CONFIRM_EMAIL_SALT      = ''
SECRET_PASSWORD_RESET_SALT     = ''

#Serializer secret keys
SECRET_CONFIRM_EMAIL_KEY       = ''
SECRET_PASSWORD_RESET_KEY      = ''

#SQLAlchemy config
if not DEBUG:
    SQLALCHEMY_DATABASE_URI    = 'mysql://apps:@localhost/apps'
else:
    SQLALCHEMY_DATABASE_URI    = 'sqlite:///' + os.path.join(database_dir, 'main.db')

SQLALCHEMY_MIGRATE_REPO        = os.path.join(database_dir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False


#Email server config
MAIL_SERVER                    = 'smtp.yandex.ru'
MAIL_PORT                      = 465
MAIL_USE_TLS                   = False
MAIL_USE_SSL                   = True
MAIL_USERNAME                  = ''
MAIL_PASSWORD                  = ''

#Administrators list
ADMINS                         = ['admins']

#Support mail
MAIL_SUPPORT                   = 'support@ugmi.me'

#Roles
ROLE_USER                      = 0
ROLE_ADMIN                     = 1

#Log file
LOG_FILE                       = 'ugmi.log'

#Marks

#Small
SMALL_GENERATOR = os.path.join(generators_dir, 'small_generator.jar')
SMALL_MARKS_DIR = os.path.join(base_dir, 'Small_marks')
SMALL_MARKS_EXTENSION = '.png'

#Large


#Alias
BYDLO_ALIAS = os.path.join(base_dir, 'bydlo_alias.json')
