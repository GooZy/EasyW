#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/24 16:03
# @Author  : GUO Ziyao
from easyw.watermark.biz.user import UserBiz
from easyw.watermark.service.user import UserService

from flask import flash
from flask import Blueprint
from flask import session
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template

bp = Blueprint('user', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        error_message = UserBiz.register_user(username, password, password2)
        if not error_message:
            UserService.add_user(username, password)
            flash('Register successfully!')
            return render_template('login.html')
    return render_template('register.html', error=error_message)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = UserService.get_user_by_name_and_password(username, password)
        if not result:
            error_message = "Invalid username or password!"
        else:
            session['logged_in'] = True
            flash('Welcome back %s!' % username)
            return render_template('main.html')
    return render_template('login.html', error=error_message)


@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index.hello_world'))
