# -*- coding: utf-8 -*-
from threading import Thread
from flask import g, redirect, url_for, flash
from config import ROLE_ADMIN
from functools import wraps
from .models.mark import Mark


def asynchronous(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (not g.user.is_authenticated) or (not g.user.is_admin):
            flash({'head' : u'Ты не пройдешь!', 'msg' : u'Доступ только администраторам.' }, 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


'''in kwargs MUST BE mark_id'''
def owner_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (not g.user.is_authenticated):
            flash({'head' : u'Ты не пройдешь!', 'msg' : u'Доступ только владельцу.' }, 'error')
            return redirect(url_for('index'))
        if g.user.is_admin or (Mark.query.get(kwargs['mark_id']) in g.user.marks):
            return f(*args, **kwargs)
        flash({'head' : u'Ты не пройдешь!', 'msg' : u'Доступ только владельцу.' }, 'error')
        return redirect(url_for('index'))
    return decorated_function


'''Wrapper for decorators with args.'''
def parametrized(dec):
    @wraps(dec)
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer
