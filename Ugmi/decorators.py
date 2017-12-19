# -*- coding: utf-8 -*-
from threading import Thread
from flask import g, redirect, url_for, flash
from config import ROLE_ADMIN
from functools import wraps

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper


def admin_only(f):
    def wrapper(*args, **kwargs):
        if (not g.user.is_authenticated) or (not g.user.is_admin):
            flash({'head' : u'Ты не пройдешь!', 'msg' : u'Доступ только администраторам.' }, 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return wrapper
