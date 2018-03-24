#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/24 16:03
# @Author  : GUO Ziyao
from easyw.common.db import query_db
from easyw.common.utils import hash_password

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
        if not username or not password or not password2:
            error_message = "Please fill in all textbox!"
        else:
            result = query_db('SELECT * FROM users WHERE username=?', [username])
            if result:
                error_message = "Username exist!"
            elif password != password2:
                error_message = "Entered passwords differ!"
            else:
                query_db("INSERT INTO users(username, password) VALUES (?, ?)", [username, hash_password(password)])
                flash('Register successfully!')
                return render_template('login.html')
    return render_template('register.html', error=error_message)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        result = query_db('SELECT * FROM users WHERE username=? AND password=?', [username, password])
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