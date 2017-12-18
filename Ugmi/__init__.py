# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db   = SQLAlchemy(app)
mail = Mail(app)
lm   = LoginManager()

lm.init_app(app)
lm.login_view = 'login'

from Ugmi import views, models
