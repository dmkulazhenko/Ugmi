# -*- coding: utf-8 -*-
import os, json

from flask import render_template, flash, redirect, url_for, request, g, session, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required, AnonymousUserMixin

from datetime import datetime

from Ugmi import app, db, lm
from config import MAIL_SUPPORT, ADMINS

from .forms import Contact_us_form, Registration_form, Login_form, Password_reset_form, Password_reset_set_form, Add_small_mark_form, Generate_small_mark_form
from .models import Support_msg, User
from .emails import support_notification, internal_error_notification
from .utils import is_safe_url
from .decorators import admin_only

from .small_marks import small_manager



@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(400)
def internal_error(error):
    return render_template('500.html'), 400


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if not app.debug:
        internal_error_notification()
    return render_template('500.html'), 500



@lm.user_loader
def load_user(id):
    return User.query.get(int(id))




@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()




@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = Contact_us_form()
    if form.validate_on_submit():
        msg = Support_msg(name = form.name.data, email = form.email.data, phone = form.phone.data, msg = form.msg.data, date = datetime.utcnow())
        db.session.add(msg)
        db.session.commit()
        support_notification(msg)
        flash({'head' : u'Спасибо!', 'msg' : u'Ваше сообщение доставлено.' }, 'success')
        return redirect(url_for('index'))
    form.flash_errors()
    return render_template('index.html', form = form)




@app.route('/contacts', methods = ['GET', 'POST'])
def contacts():
    form = Contact_us_form()
    if form.validate_on_submit():
        msg = Support_msg(name = form.name.data, email = form.email.data, phone = form.phone.data,
            msg = form.msg.data, date = datetime.utcnow())
        db.session.add(msg)
        db.session.commit()
        support_notification(msg)
        flash({'head' : u'Спасибо!', 'msg' : u'Ваше сообщение доставлено.' }, 'success')
        return redirect(url_for('contacts'))
    form.flash_errors()
    return render_template('contacts.html', form = form)




@app.route('/team', methods = ['GET', 'POST'])
def team():
    form = Contact_us_form()
    if form.validate_on_submit():
        msg = Support_msg(name = form.name.data, email = form.email.data, phone = form.phone.data,
            msg = form.msg.data, date = datetime.utcnow())
        db.session.add(msg)
        db.session.commit()
        support_notification(msg)
        flash({'head' : u'Спасибо!', 'msg' : u'Ваше сообщение доставлено.' }, 'success')
        return redirect(url_for('team'))
    form.flash_errors()
    return render_template('team.html', form = form)




@app.route('/project')
def project():
    return render_template('project.html')




@app.route('/download', methods = ['GET', 'POST'])
def download():
    form = Registration_form()
    if form.validate_on_submit():
        user = User(name = form.name.data, email = form.email.data, username = form.username.data,
            password = form.password.data, role = (form.email.data in ADMINS))
        db.session.add(user)
        db.session.commit()
        flash({'head' : u'Ура!', 'msg' : u'Вы успешно зарегистрированы.' }, 'success')

        user.send_email_confirm_token()
        flash({'head' : u'Внимание!', 'msg' : u'Письмо для подтверждения вашего email отправлено!' }, 'info')

        return redirect(url_for('index'))
    form.flash_errors()
    return render_template('download.html', form = form)




@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = User.check_email_confirm_token(token)
    except:
        flash({'head' : u'Упс...', 'msg' : u'Ссылка повреждена или просрочена.' }, 'error')
        return redirect(url_for('index'))
    if email == None:
        flash({'head' : u'Упс...', 'msg' : u'Ссылка повреждена или просрочена.' }, 'error')
        return redirect(url_for('index'))

    user = User.query.filter_by(email = email).first()

    if user == None:
        flash({'head' : u'Упс...', 'msg' : u'Ссылка повреждена или просрочена.' }, 'error')
        return redirect(url_for('index'))
    if user.confirmed:
        flash({'head' : u'Все хорошо!', 'msg' : u'Email уже подтвержден. Вы можете авторизоваться.' }, '')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash({'head' : u'Прекрасно!', 'msg' : u'Email успешно подтвержден! Вы можете авторизоваться.' }, 'success')
    return redirect(url_for('login'))




@app.route('/resend/<username>')
def resend_confirmation(username):
    user = User.query.filter_by(username = username).first()
    if user == None:
        flash({'head' : u'Упс...', 'msg' : u'Неверное имя пользователя.' }, 'error')
        return redirect(url_for('login'))
    if user.confirmed == True:
        flash({'head' : u'Упс...', 'msg' : u'Ваш email уже подтвержден.' }, 'info')
        return redirect(url_for('login'))
    if (user.last_email_confirm != None) and ((datetime.utcnow() - user.last_email_confirm).total_seconds() < 900):
        flash({'head' : u'Упс...', 'msg' : u'Следующие письмо с интервалом в 15 минуток.' }, 'error')
        return redirect(url_for('login'))
    user.send_email_confirm_token()
    user.last_email_confirm = datetime.utcnow()
    db.session.add(user)
    db.session.commit()
    flash({'head' : u'Успех!', 'msg' : u'Подтверждение отправлено еще раз. Не забудьте проверить спам.' }, 'success')
    return redirect(url_for('login'))




@app.route('/reset/<token>', methods = ['GET', 'POST'])
def reset_password_confirm(token):
    try:
        email = User.check_password_reset_token(token)
    except:
        flash({'head' : u'Упс...', 'msg' : u'Ссылка повреждена или просрочена.' }, 'error')
        return redirect(url_for('index'))
    if email == None:
        flash({'head' : u'Упс...', 'msg' : u'Ссылка повреждена или просрочена.' }, 'error')
        return redirect(url_for('index'))

    user = User.query.filter_by(email = email).first()
    if user == None:
        flash({'head' : u'Упс...', 'msg' : u'Ссылка повреждена или просрочена.' }, 'error')
        return redirect(url_for('index'))
    form = Password_reset_set_form()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash({'head' : u'Ура!', 'msg' : u'Пароль успешно изменен.' }, 'success')
        return redirect(url_for('login'))
    form.flash_errors()
    return render_template('reset_set_password.html', form = form)




@app.route('/reset', methods = ['GET', 'POST'])
@app.route('/reset/', methods = ['GET', 'POST'])
def reset_password():
    form = Password_reset_form()
    if form.validate_on_submit():
        user = load_user(form.id.data)
        user.send_password_reset_token()
        user.last_password_reset = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        flash({'head' : u'Отлично!', 'msg' : u'Письмо для восстановления пароля отправлено на ваш email.'}, 'success')
        return redirect(url_for('login'))
    form.flash_errors()
    return render_template('reset_password.html', form = form)




@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user.is_authenticated:
        flash({'head' : u'Хмм...', 'msg' : u'Вы уже авторизованы!' }, 'info')
        return redirect(url_for('index'))
    form = Login_form()
    if form.validate_on_submit():
        user = load_user(form.id.data)
        login_user(user, remember = form.remember_me.data)
        flash({'head' : u'Привет!', 'msg' : u'Мы очень рады Вас видеть!' }, 'success')
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('index'))
    form.flash_errors()
    return render_template('login.html', form = form)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash({'head' : u'Мы будем скучать!', 'msg' : u'Возвращайтесь поскорее!' }, 'success')
    return redirect(url_for('index'))




@app.route('/admin/small/generate', methods = ['POST', 'GET'])
@admin_only
def generate_small_mark():
    form = Generate_small_mark_form()
    if form.validate_on_submit():
        mark_file = small_manager.generate_small_mark(form.mark_id.data)
        return send_from_directory(directory = os.path.dirname(mark_file),
        filename = os.path.basename(mark_file))
    form.flash_errors()
    return render_template('admin_generate_mark.html', form = form, img = None)



@app.route('/admin/small/add', methods = ['GET', 'POST'])
@admin_only
def add_small_mark():
    form = Add_small_mark_form()
    if form.validate_on_submit():
        small_manager.add_small_mark(form.mark_id.data, form.title.data,
            form.img.data, form.video.data, form.site.data)
        flash({ 'head' : u'Успех!', 'msg' : u'Объект успешно добавлен!' }, 'success')
        return redirect(url_for('add_small_mark'))
    form.flash_errors()
    return render_template('admin_add_mark.html', form = form)
