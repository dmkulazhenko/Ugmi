# -*- coding: utf-8 -*-
from flask import jsonify, request

from Ugmi import app, db

from .models.user import User
from .models.mark import Mark
from .decorators import admin_only


#User:
@app.route('/ajax/user/list')
@admin_only
def ajax_get_list_of_users():
    users = User.query.all()
    data = {}
    data['status'] = 'success'
    data['users'] = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['name'] = user.name
        user_data['role'] = user.role
        user_data['have_marks'] = user.have_marks
        user_data['max_marks'] = user.max_marks
        data['users'].append(user_data)
    return jsonify(data)



@app.route('/ajax/user/<username>')
@admin_only
def ajax_get_info_about_user(username):
    data = {}
    user = User.query.filter_by(username = username).first()
    if not user:
        data['status'] = 'error'
        data['msg'] = "User with username '" + username + "' not found."
        return jsonify(data)
    data = user.ajax_get_info()
    data['status'] = 'success'
    data['msg'] = None
    return jsonify(data)


@app.route('/ajax/user/confirm')
def ajax_confirm_user():
    data = {}
    username = request.args.get('username')
    user = User.query.filter_by(username = username).first()
    if not user:
        data['status'] = 'error'
        data['msg'] = "User with username '" + username + "' not found."
        return jsonify(data)
    if user.confirmed == False:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        data['status'] = 'success'
        data['msg'] = 'User ' + username + ' successfully confirmed.'
    else:
        data['status'] = 'error'
        data['msg'] = 'User ' + username + ' already confirmed.'
    return jsonify(data)


@app.route('/ajax/user/delete')
def ajax_delete_user():
    data = {}
    username = request.args.get('username')
    user = User.query.filter_by(username = username).first()
    if not user:
        data['status'] = 'error'
        data['msg'] = "User with username '" + username + "' not found."
        return jsonify(data)
    cnt = 0
    for mark in user.marks:
        cnt += 1
        mark.delete_files()
        db.session.delete(mark)
    db.session.delete(user)
    db.session.commit()

    data['status'] = 'success'
    data['msg'] = 'Successfully deleted user with username ' + username + ' and ' + str(cnt) + ' marks.'

    return jsonify(data)


#Set:
@app.route('/ajax/user/set/role')
@admin_only
def ajax_set_role_for_user():
    data = {}
    username = request.args.get('username')
    role_id = request.args.get('role_id', default = 1, type = int)
    user = User.query.filter_by(username = username).first()
    if not user:
        data['status'] = 'error'
        data['msg'] = "User with username '" + username + "' not found."
        return jsonify(data)
    if role_id < 0 or role_id > 4:
        data['status'] = 'error'
        data['msg'] = "Role with id '" + role_id + "' not found."
        return jsonify(data)
    role_was = user.role
    user.role = role_id
    user.custom_marks_limit = None
    db.session.add(user)
    db.session.commit()
    data['status'] = 'success'
    data['msg'] = username +'`s role: ' + str(role_was) + ' -> ' + str(role_id) +'.'
    return jsonify(data)


@app.route('/ajax/user/set/custom_marks_limit')
@admin_only
def ajax_set_custom_marks_limit_for_user():
    data = {}
    username = request.args.get('username')
    max_marks = request.args.get('max_marks', default = None, type = int)
    user = User.query.filter_by(username = username).first()
    if not user:
        data['status'] = 'error'
        data['msg'] = "User with username '" + username + "' not found."
        return jsonify(data)
    if max_marks < 0:
        data['status'] = 'error'
        data['msg'] = "Marks limit can't be less than 0."
        return jsonify(data)
    user.custom_marks_limit = max_marks
    db.session.add(user)
    db.session.commit()
    data['status'] = 'success'
    data['msg'] = username +'`s marks limit successfully updated.'
    return jsonify(data)



#Mark:
@app.route('/ajax/mark/list')
@admin_only
def ajax_get_list_of_marks():
    marks = Mark.query.all()
    data = {}
    data['status'] = 'success'
    data['marks'] = []
    for mark in marks:
        mark_data = {}
        mark_data['id'] = mark.id
        mark_data['title'] = mark.title
        mark_data['views'] = mark.views
        mark_data['user'] = {}
        mark_data['user']['username'] = mark.user.username
        mark_data['user']['email'] = mark.user.email
        data['marks'].append(mark_data)
    return jsonify(data)


@app.route('/ajax/mark/<mark_id>')
@admin_only
def ajax_get_info_about_mark(mark_id):
    data = {}
    mark = Mark.query.get(mark_id)
    if not mark:
        data['status'] = 'error'
        data['msg'] = "Mark with id '" + mark_id + "' not found."
        return jsonify(data)
    data = mark.ajax_get_info()
    data['status'] = 'success'
    data['msg'] = None
    return jsonify(data)


#Delete
@app.route('/ajax/mark/delete')
@admin_only
def ajax_delete_mark():
    data = {}
    mark_id = request.args.get('mark_id', type = int)
    mark = Mark.query.get(mark_id)
    if not mark:
        data['status'] = 'error'
        data['msg'] = "Mark with id '" + str(mark_id) + "' not found."
        return jsonify(data)
    mark.delete_files()
    db.session.delete(mark)
    db.session.commit()
    data['status'] = 'success'
    data['msg'] = "Mark with id '" + str(mark_id) + "' successfully deleted."
    return jsonify(data)
