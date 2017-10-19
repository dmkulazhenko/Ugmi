# -*- coding: utf-8 -*-
from flask import *
from werkzeug import secure_filename

from config import UPLOAD_FOLDER
import sender, os

app = Flask(__name__)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.ico', mimetype='img/favicon.ico')

@app.route('/google09f46f29de6ab559.html')
def goolge():
    return render_template('google.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/home.html', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        msg = request.form['msg']
        if name == "" or email == "" or phone == "" or msg == "":
            return render_template('index.html', err=u'Заполните все поля.')
        sender.send_email(name, email, phone, msg)
        return render_template('index.html', err=u'Ваше сообщение уже у нас, мы ответим в ближайшие сроки!')
    return render_template('index.html')

@app.route('/contacts', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        msg = request.form['msg']
        if name == "" or email == "" or phone == "" or msg == "":
            return render_template('contacts.html', err=u'Заполните все поля.')
        sender.send_email(name, email, phone, msg)
        return render_template('contacts.html', err=u'Ваше сообщение уже у нас, мы ответим в ближайшие сроки!')
    return render_template('contacts.html')

@app.route('/team', methods=['GET', 'POST'])
def team():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        msg = request.form['msg']
        if name == "" or email == "" or phone == "" or msg == "":
            return render_template('team.html', err=u'Заполните все поля.')
        sender.send_email(name, email, phone, msg)
        return render_template('team.html', err=u'Ваше сообщение уже у нас, мы ответим в ближайшие сроки!')
    return render_template('team.html')

@app.route('/project')
def project():
    return render_template('project.html')


@app.route('/download/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/download', methods=['GET', 'POST'])
def download_ome():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if username == "" or email == "" or password == "":
            return render_template('download.html', err=u"Данные введены неверно.")
        if len(username) < 3 or len(username) > 32:
            return render_template('download.html', err=u"Слишком короткое или длинное имя пользователя.")
        if len(password) < 6 or len(password) > 256:
            return render_template('download.html', err=u"Слишком короткий или длинный пароль.")
        if len(email) < 4 or len(email) > 32:
            return render_template('download.html', err=u"Слишком короткий или длинный E-Mail.")
        sender.send_email_reg(username, email, password)
        return render_template('download.html', success=u'Пользователь '+username+u' зарегистрирован.')
    return render_template('download.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', err="No selected file.")
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', err="No selected file.")
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return render_template('upload.html', err="Uploaded!")
    return render_template('upload.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
