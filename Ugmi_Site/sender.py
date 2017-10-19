import smtplib
from config import mail_login, mail_password, mail_feedback

def send_email(name, email, phone, message):
    info = '\nName: '+name+'\nE-Mail: '+email+'\nPhone: '+phone+'\n'
    message = info+message
    msg = "\r\n".join([
        "From: "+mail_login,
        "To: "+mail_feedback,
        "Subject: Feedback from ugmi.me",
        "",
        message
        ])
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(mail_login, mail_password)
    server.sendmail(mail_login, mail_feedback, msg)
    server.close()

def send_email_reg(name, email, password):
    info = '\nName: '+name+'\nE-Mail: '+email+'\nPassword: '+password+'\n'
    message = info+'Registration form.'
    msg = "\r\n".join([
        "From: "+mail_login,
        "To: "+mail_feedback,
        "Subject: Registration from ugmi.me",
        "",
        message
        ])
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(mail_login, mail_password)
    server.sendmail(mail_login, mail_feedback, msg)
    server.close()
