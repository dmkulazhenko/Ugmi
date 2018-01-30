# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, g, jsonify
from flask_login import login_required

from Ugmi import app, db, forms

from .models import Mark
from .decorators import owner_only



@app.route('/small/add', methods = ['GET', 'POST'])
@login_required
def add_small_mark():
    if g.user.is_marks_limit_exceeded:
        flash({ 'head' : u'Упс!', 'msg' : u'Лимит по добавлению меток для вашего аккаунта исчерпан!' }, 'error')
        return redirect(url_for('index'))
    form = forms.Add_small_mark_form()
    if form.validate_on_submit():
        mark = Mark(
            id = form.mark_id.data,
            title = form.title.data,
            img = form.img.data,
            video = form.video.data,
            site = form.site.data,
            user = g.user,
            creation_time = datetime.utcnow()
        )
        db.session.add(mark)
        db.session.commit()
        flash({ 'head' : u'Успех!', 'msg' : u'Метка успешно добавлена!' }, 'success')
        return redirect(url_for('list_of_marks'))
    form.flash_errors()
    return render_template('add_small_mark.html', form = form)




@app.route('/small/get/<mark_id>')
def get_small_mark(mark_id):
    mark = Mark.query.get(mark_id)
    if mark == None:
        return jsonify({'status' : 'error', 'msg' : 'mark with id ' + mark_id + ' not found.'}), 404
    mark.views += 1
    db.session.add(mark)
    db.session.commit()
    data = {}
    data['status'] = 'success'
    data['msg'] = None
    data['title'] = mark.title
    data['img'] = mark.img
    data['site'] = mark.site
    data['res'] = mark.video
    return jsonify(data)




@app.route('/small/print/<mark_id>')
def print_small_mark(mark_id):
    mark = Mark.query.get(mark_id)
    if mark == None:
        return jsonify({'status' : 'error', 'msg' : 'mark with id ' + mark_id + ' not found.'}), 404
    return mark.get_mark()




@app.route('/small/delete/<mark_id>')
@owner_only
def delete_small_mark(mark_id):
    mark = Mark.query.get(mark_id)
    mark.delete_files()
    db.session.delete(mark)
    db.session.commit()
    flash({ 'head' : u'Упспешно!', 'msg' : u'Метка успешно удалена!' }, 'success')
    return redirect(url_for('list_of_marks'))




@app.route('/small/<mark_id>')
@owner_only
def about_mark(mark_id):
    mark = Mark.query.get(mark_id)
    if mark == None:
        flash({ 'head' : u'Упс!', 'msg' : u'Метки с таким ID не существует!' }, 'error')
        return redirect(url_for('index'))
    return render_template('about_small_mark.html', mark = mark)




@app.route('/small/edit/<mark_id>', methods=['GET', 'POST'])
@owner_only
def edit_small_mark(mark_id):
    form = forms.Edit_small_mark_form()
    mark = Mark.query.get(mark_id)
    if form.validate_on_submit():
        mark.title = form.title.data
        mark.video = form.video.data
        mark.img = form.img.data
        mark.site = form.site.data
        mark._init_json()
        db.session.add(mark)
        db.session.commit()
        flash({ 'head' : u'Прекрасно!', 'msg' : u'Информация о метке успешно сохранена!' }, 'success')
        return redirect(url_for('about_mark', mark_id = mark_id))
    form.flash_errors()
    return render_template('edit_small_mark.html', form = form, mark = mark)




@app.route('/list')
@login_required
def list_of_marks():
    return render_template('list_of_marks.html')
