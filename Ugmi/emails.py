# -*- coding: utf-8 -*-
from flask import render_template
from flask_mail import Message

from Ugmi import mail, app

from .decorators import async


@async
def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, text_body, html_body, sender = app.config['MAIL_USERNAME']):
    msg = Message(subject = subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(msg)


def support_notification(support_msg):
    send_email(
        subject = u'[UGMI] Поддержка',
        recipients = [support_msg.email],
        text_body = render_template('support_notification_email.txt', support_msg=support_msg),
        html_body = render_template('support_notification_email.html', support_msg=support_msg)
    )
    send_email(
        subject = u'[UGMI] Поддержка',
        recipients = app.config['ADMINS'] + [app.config['MAIL_SUPPORT']],
        text_body = render_template('admin_support_notification_email.txt', support_msg=support_msg),
        html_body = render_template('admin_support_notification_email.html', support_msg=support_msg)
    )


def internal_error_notification():
    send_email(
        subject = u'[UGMI] СЕРВАК ЛЕГ!',
        recipients = app.config['ADMINS'],
        text_body = render_template('admin_internal_error_notification_email.txt'),
        html_body = render_template('admin_internal_error_notification_email.html')
    )


def confirm_email_notification(user, confirm_email_url):
    send_email(
        subject = u'[UGMI] Подтверждение email',
        recipients = [user.email],
        text_body = render_template('confirm_email_notification.txt', user=user, confirm_email_url=confirm_email_url),
        html_body = render_template('confirm_email_notification.html', user=user, confirm_email_url=confirm_email_url)
    )


def password_reset_notification(user, password_reset_url):
    send_email(
        subject = u'[UGMI] Изменение пароля',
        recipients = [user.email],
        text_body = render_template('password_reset_notification.txt', user=user, password_reset_url=password_reset_url),
        html_body = render_template('password_reset_notification.html', user=user, password_reset_url=password_reset_url)
    )
