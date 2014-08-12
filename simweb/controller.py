# -*- coding: utf-8 -*-
# Started by Alan
# MainTained by Alan
# Contact: alan@sinosims.com

from simweb import app
from flask import Flask, Response, json, session
from simweb.libs.database import db_session
from simweb.models import User

@app.route('/')
def hi():
    a = User.query.all()
    data = app.redis.keys("User*")
    u = User.query.filter_by(login='crane').first()
    session['uid'] = u.id
    session['login'] = u.login
    return Response(json.dumps(data), status=200, mimetype='application/json')

@app.route('/login', methods=['POST'])
def login():
    u = User.query.filter_by(login='crane').first()
    session['uid'] = u.id
    session['login'] = u.login
    return Response(json.dumps('ok'), status=200, mimetype='application/json')

@app.route('/logout', methods=['POST'])
def logout():
    return Response(json.dumps('ok'), status=200, mimetype='application/json')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
