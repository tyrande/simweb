# -*- coding: utf-8 -*-
# Started by Alan
# MainTained by Alan
# Contact: alan@sinosims.com

from flask import Flask
import redis
from simweb.libs.session import RedisSessionInterface

app = Flask(__name__)
app.session_interface = RedisSessionInterface()
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
app.redis = redis.Redis(connection_pool=pool)


import simweb.controller
