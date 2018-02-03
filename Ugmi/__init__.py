# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer, TimedJSONWebSignatureSerializer
from Ugmi.utils import init_Ugmi
from momentjs import momentjs

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.globals['momentjs'] = momentjs

db   = SQLAlchemy(app)
migrate = Migrate(app, db)

mail = Mail(app)
lm   = LoginManager()

lm.init_app(app)
lm.login_view = 'login'

email_confirm_serializer  = URLSafeTimedSerializer(app.config['SECRET_CONFIRM_EMAIL_KEY'])
password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_PASSWORD_RESET_KEY'])
api_token_serializer      = TimedJSONWebSignatureSerializer(app.config['SECRET_API_TOKEN_KEY'], expires_in = app.config['API_TOKEN_EXPRIRATION_TIME'])

init_Ugmi()


from Ugmi import views, mark_views, ajax, api
from Ugmi.models import user, mark, support_msg, comment
