import re, bcrypt
from flask import request, jsonify, g
from functools import wraps

from Ugmi import app, db

from .models.user import User



def api_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.get_json()
        if token is None:
            return jsonify(status = 'error', msg = 'Private area, token required.', code = 101), 401
        token = token.get('token')
        if token is None:
            return jsonify(status = 'error', msg = 'Private area, token required.', code = 101), 401
        user = User.check_api_token(token)
        if user is 'invalid':
            return jsonify(status = 'error', msg = 'Invalid token.', code = 102), 401
        if user is 'expired':
            return jsonify(status = 'error', msg = 'Token has expired.', code = 103), 401
        g.user = user
        return f(*args, **kwargs)
    return decorated_function




@app.errorhandler(405)
def not_found_error(error):
    return jsonify(status = 'error', msg = 'Method not allowed.', code = None), 405




@app.route('/api/user', methods = ['POST'])
def api_register_user():
    data = request.get_json()
    username = data.get('username')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

#VALIADTION
    if (username is None) or (name is None) or (email is None) or (password is None):
        return jsonify(status = 'error', msg = 'Incorrect request.', code = 1), 400
    ok = True
    if( len(name) < 3 or len(name) > 64 or re.match("^[A-Za-zА-Яа-я ]*$", name) is None):
        ok = False
    if( len(username) < 3 or len(username) > 64 or re.match("^[A-Za-z0-9_]*$", username) is None):
        ok = False
    if( len(email) < 3 or len(email) > 64 or '@' not in email ):
        ok = False
    if( len(password) < 8 or len(password) > 256 ):
        ok = False
    if not ok:
        return jsonify(status = 'error', msg = 'Incorrect request.', code = 2), 400
#END VALIDATION

    if User.query.filter_by(username = username).first() is not None:
        return jsonify(status = 'error', msg = 'Username already taken.', code = 3), 400
    if User.query.filter_by(email = email).first() is not None:
        return jsonify(status = 'error', msg = 'Email already registered.', code = 4), 400

    password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt()).decode('utf-8')
    role = app.config['ROLE_DEFAULT']
    if email in app.config['ADMINS']:
        role = app.config['ROLE_ADMIN']
    user = User(name = name, email = email, username = username,
        password = password, role = role)
    db.session.add(user)
    db.session.commit()
    user.send_email_confirm_token()
    return jsonify(status = 'success', msg = 'User successfully registered.', code = None, token = user.get_api_token()), 200




@app.route('/api/user/login', methods = ['POST'])
def api_auth_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if (username is None) or (password is None):
        return jsonify(status = 'error', msg = 'Where is username and password?', code = 1), 400

    user = User.query.filter_by(username = username).first()
    if user is None:
        return jsonify(status = 'error', msg = ("User with username '" + username + "' not found."), code = 2), 404
    if not user.auth(password):
        return jsonify(status = 'error', msg = 'Incorrect password.', code = 3), 401

    return jsonify(status = 'success', msg = 'Successfully authorized.', code = None, token = user.get_api_token()), 200




@app.route('/api/user/<username>', methods = ['GET'])
@api_token_required
def api_get_info_about_user(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        return jsonify(status = 'error', msg = ("User with username '" + username + "' not found."), code = 1), 404
    return jsonify(status = 'success', msg = ('Info about user ' + username), code = None,
        id = str(user.id), username = user.username, email = user.email, name = user.name, role = user.prefix), 200
