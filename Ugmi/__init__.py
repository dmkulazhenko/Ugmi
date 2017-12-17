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

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    from config import LOG_FILE
    file_handler = RotatingFileHandler(LOG_FILE, 'a', 8 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Ugmi startup')
