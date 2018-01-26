import os
from flask import jsonify, request
from shutil import rmtree

from Ugmi import app, db
from config import SMALL_MARKS_DIR

from .models import Mark, User
from .decorators import admin_only


#User:
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
    db.session.delete(mark)
    db.session.commit()
    mark_dir = os.path.join(SMALL_MARKS_DIR, str(mark_id))
    rmtree(mark_dir)
    data['status'] = 'success'
    data['msg'] = "Mark with id '" + str(mark_id) + "' successfully deleted."
    return jsonify(data)
