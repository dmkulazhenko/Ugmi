# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from Ugmi.marks import small_manager

app = Flask(__name__)
app.config.from_object('config')

db   = SQLAlchemy(app)
mail = Mail(app)
lm   = LoginManager()

lm.init_app(app)
lm.login_view = 'login'


small_manager.init()

from Ugmi import views, models
