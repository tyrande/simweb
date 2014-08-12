import pickle
from uuid import uuid1
from redis import Redis
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin

def total_seconds(td):
    return td.days * 60 * 60 * 24 + td.seconds

class RedisSession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class RedisSessionInterface(SessionInterface):
    serializer = pickle
    session_class = RedisSession

    def __init__(self, redis=None):
        if redis is None:
            redis = Redis()
        self.redis = redis

    def generate_sid(self):
        return str(uuid1().hex)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        data = self.redis.hgetall("Session:%s:info"%sid)
        if len(data) > 0:
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete("Session:%s:info"%session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain)
            return
        cookie_exp = self.get_expiration_time(app, session)
        self.redis.hmset("Session:%s:info"%session.sid, dict(session))
        self.redis.expire("Session:%s:info"%session.sid, 604800)
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True,
                            domain=domain)