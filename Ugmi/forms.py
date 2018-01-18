# -*- coding: utf-8 -*-
import string, re, bcrypt, os
from datetime import datetime
from flask import flash, Markup, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from .models import User
from config import SMALL_MARKS_DIR, MARKS_DATA_FILE




class Contact_us_form(FlaskForm):
    name  = StringField('name', [
        DataRequired(message=u'Как Вас зовут?'),
        Length(min=3, max=64, message=u'Неужели Ваше имя такое короткое?)')
    ], render_kw = {"placeholder" : u"* Имя"})

    email = StringField('email', [
        DataRequired(message=u'Мы не будем спамить, честно!'),
        Email(message=u'Не похоже на Ваш email.'),
        Length(min=3, max=64, message=u'Не похоже на Ваш email.')
    ], render_kw = {"placeholder" : u"* E-mail"})

    phone = StringField('phone', [
        DataRequired(message=u'Оставьте Ваш телефончик, никому не скажем.'),
        Length(min=7, max=20, message=u'Оставьте Ваш телефончик, никому не скажем.')
    ], render_kw = {"placeholder" : u"* Телефон"})

    msg   = TextAreaField('msg', [DataRequired(message=u'А что Вы хотели нам сказать?')],
        render_kw = {"placeholder" : u"* Сообщение"})


    def flash_errors(self):
        for field, errors in self.errors.items():
            for error in errors:
                flash({'head' : u'Упс...', 'msg' : error }, 'error')

    def validate(self):
        '''Validates for strange chars in name and phone.
        Formats name email and phone to std view.'''
        if not FlaskForm.validate(self):
            return False

        ac = True
        if re.match("^[A-Za-zА-Яа-я ]*$", self.name.data) == None:
            self.name.errors.append(u'Не похоже на Ваше имя.')
            ac = False
        if re.match("^[0-9 +#()-]*$", self.phone.data) == None:
            self.phone.errors.append(u'Не похоже на Ваш телефон.')
            ac = False
        if ac == False:
            return False

        self.name.data = self.name.data.strip().title()
        self.email.data = self.email.data.strip().lower()
        for junk_char in '#()- ': self.phone.data = self.phone.data.replace(junk_char, '')

        return True




class Registration_form(FlaskForm):
    name  = StringField('name', [
        DataRequired(message=u'Как Вас зовут?'),
        Length(min=3, max=64, message=u'Неужели Ваше имя такое короткое?)')
    ], render_kw = {"placeholder" : u"* Имя"})

    username = StringField('username', [
        DataRequired(message=u'Кажется, вы забыли указать Ваше имя пользователя.'),
        Length(min=3, max=64, message=u'Придумайте ник подлинее.')
    ], render_kw = {"placeholder" : u"* Имя пользователя"})

    email = StringField('email', [
        DataRequired(message=u'Мы не будем спамить, честно!'),
        Email(message=u'Не похоже на Ваш email.'),
        Length(min=3, max=64, message=u'Не похоже на Ваш email.')
    ], render_kw = {"placeholder" : u"* E-mail"})

    password = PasswordField('password', [
        DataRequired(message=u'Без пароля мы не сможем узнать Вы ли это.'),
        Length(min=8, max=256, message=u'Сликшом короткий пароль.')
    ], render_kw = {"placeholder" : u"* Пароль"})

    password_conf = PasswordField('password_conf', [EqualTo('password', message='Пароли не совпадают.')], render_kw = {"placeholder" : u"* Пароль"})


    def flash_errors(self):
        for field, errors in self.errors.items():
            for error in errors:
                flash({'head' : u'Упс...', 'msg' : error }, 'error')

    def validate(self):
        '''Validates for strange chars in name, username.
        Formats name, username, email to std view,
        Checks for username and email uniqueness.
        Converts password to hash using bcrypt.'''
        if not FlaskForm.validate(self):
            return False

        self.name.data = self.name.data.strip().title()
        self.username.data = self.username.data.strip().lower()
        self.email.data = self.email.data.strip().lower()

        ac = True
        if re.match("^[A-Za-zА-Яа-я ]*$", self.name.data) == None:
            self.name.errors.append(u'Не похоже на Ваше имя.')
            ac = False
        if re.match("^[A-Za-z0-9_]*$", self.username.data) == None:
            self.username.errors.append(u'Имя пользователя должно состоять только из английских букв, цифр и нижнего подчеркивания.')
            ac = False
        if User.query.filter_by(username = self.username.data).first() != None:
            self.username.errors.append(u'Данное имя пользователя занято :(')
            ac = False

        if User.query.filter_by(email = self.email.data).first() != None:
            self.email.errors.append('Аккаунт с таким email существует. Вы можете восстановить пароль.')
            ac = False

        if ac == False:
            return False

        self.password.data = bcrypt.hashpw(bytes(self.password.data, 'utf-8'), bcrypt.gensalt()).decode('utf-8')
        return True




class Login_form(FlaskForm):
    login = StringField('login', [
        DataRequired(message=u'Введите имя пользователя или email.'),
        Length(min=3, max=64, message=u'Неверное имя пользовтеля или email.)')
    ], render_kw = {"placeholder" : u"* Email/Имя пользовтеля"})
    password = PasswordField('password', [
        DataRequired(message=u'Без пароля мы не сможем узнать Вы ли это.'),
        Length(min=8, max=256, message=u'Неверный пароль.')
    ], render_kw = {"placeholder" : u"* Пароль"})
    remember_me = BooleanField('remember_me', default = False)
    id = StringField('id')

    def flash_errors(self):
        for field, errors in self.errors.items():
            for error in errors:
                flash({'head' : u'Упс...', 'msg' : error }, 'error')


    def validate(self):
        '''Gets a User with email or username.
        Checks email for confirm status.'''
        if not FlaskForm.validate(self):
            return False

        self.login.data = self.login.data.strip().lower()

        if '@' in self.login.data:
            user = User.query.filter_by(email = self.login.data).first()
        else:
            user = User.query.filter_by(username = self.login.data).first()

        if (user == None) or (not user.auth(self.password.data)):
            self.login.errors.append(u'Неверный логин или пароль.')
            return False

        if not user.confirmed:
            self.login.errors.append(Markup(u'Подтвердите ваш email. Для отправки повторного письма тыкните <a href="' + url_for('resend_confirmation', username = user.username) + u'">сюда</a>.'))
            return False

        self.id.data = str(user.id)
        return True




class Password_reset_form(FlaskForm):
    '''Gets a User with email or username,
    Protects from spam.'''
    login = StringField('login', [
        DataRequired(message=u'Введите имя пользователя или email.'),
        Length(min=3, max=64, message=u'Неверное имя пользовтеля или email.)')
    ], render_kw = {"placeholder" : u"Email / Username"})
    id = StringField('id')

    def flash_errors(self):
        for field, errors in self.errors.items():
            for error in errors:
                flash({'head' : u'Упс...', 'msg' : error }, 'error')


    def validate(self):
        if not FlaskForm.validate(self):
            return False

        self.login.data = self.login.data.strip().lower()

        if '@' in self.login.data:
            user = User.query.filter_by(email = self.login.data).first()
        else:
            user = User.query.filter_by(username = self.login.data).first()

        if user == None:
            self.login.errors.append(u'Данного пользователя не существует.')
            return False

        if (user.last_password_reset != None) and ((datetime.utcnow() - user.last_password_reset).total_seconds() < 900):
            self.login.errors.append(u'Следующие письмо с интервалом в 15 минуток.')
            return False

        self.id.data = str(user.id)
        return True




class Password_reset_set_form(FlaskForm):
    '''Hashs new User password.'''
    password = PasswordField('password', [
        DataRequired(message=u'Введите новый пароль.'),
        Length(min=8, max=256, message=u'Сликшом короткий пароль.')
    ], render_kw = {"placeholder" : u"Пароль"})

    password_conf = PasswordField('password_conf', [EqualTo('password', message='Пароли не совпадают.')], render_kw = {"placeholder" : u"Ещё разок"})


    def flash_errors(self):
        for field, errors in self.errors.items():
            for error in errors:
                flash({'head' : u'Упс...', 'msg' : error }, 'error')


    def validate(self):
        if not FlaskForm.validate(self):
            return False

        self.password.data = bcrypt.hashpw(bytes(self.password.data, 'utf-8'), bcrypt.gensalt()).decode('utf-8')
        return True




class Add_small_mark_form(FlaskForm):
    mark_id = StringField('mark_id', [ DataRequired(message=u'Введите ID метки.') ], render_kw = {"placeholder" : u"ID метки"})
    title = StringField('title', [
        DataRequired(message=u'Введите заголовок.'),
        Length(min=3, max=256, message=u'Сликшом короткий или длинный заголовок.)')
    ], render_kw = {"placeholder" : u"Заголовок"})
    img = StringField('image', [ DataRequired(message=u'Введите ссылку на аватарку.') ], render_kw = {"placeholder" : u"Ссылка на аватарку"})
    video = StringField('video', [ DataRequired(message=u'Введите ссылку на видео.') ], render_kw = {"placeholder" : u"Ссылка на видео"})
    site = StringField('site', [ DataRequired(message=u'Введите ссылку на сайт.') ], render_kw = {"placeholder" : u"Ссылка на сайт"})


    def flash_errors(self):
        for field, errors in self.errors.items():
            for error in errors:
                flash({'head' : u'Упс...', 'msg' : error }, 'error')


    def validate(self):
        if not FlaskForm.validate(self):
            return False

        if re.match("^[0-9]*$", self.mark_id.data) == None:
            self.mark_id.errors.append(u'ID метки -- число.')
            return False

        if(int(self.mark_id.data) < 0 or int(self.mark_id.data) > 2**30):
            self.mark_id.errors.append(u'ID метки -- число от 0 до 2^30.')
            return False

        mark_dir = os.path.join(SMALL_MARKS_DIR, self.mark_id.data)
        if not os.path.isdir(mark_dir):
            os.mkdir(mark_dir)
        mark_data_file = os.path.join(mark_dir, MARKS_DATA_FILE)
        if os.path.isfile(mark_data_file):
            self.mark_id.errors.append(u'ID метки уже занят.')
            return False

        return True


class Generate_small_mark_form(FlaskForm):
    mark_id = StringField('mark_id', [ DataRequired(message=u'Введите ID метки.') ], render_kw = {"placeholder" : u"ID метки"})


    def flash_errors(self):
        for field, errors in self.errors.items():
            for error in errors:
                flash({'head' : u'Упс...', 'msg' : error }, 'error')


    def validate(self):
        if not FlaskForm.validate(self):
            return False

        if re.match("^[0-9]*$", self.mark_id.data) == None:
            self.mark_id.errors.append(u'ID метки -- число.')
            return False

        if(int(self.mark_id.data) < 0 or int(self.mark_id.data) > 2**30):
            self.mark_id.errors.append(u'ID метки -- число от 0 до 2^30.')
            return False

        return True
