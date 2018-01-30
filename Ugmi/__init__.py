# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
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

init_Ugmi()


from Ugmi import views, mark_views, ajax, models
