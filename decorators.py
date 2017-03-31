from helpers import *
from google.appengine.ext import db


def post_exists(function):
    @wraps(function)
    def wrapper(self, post_id, *args, **kwargs):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if not post:
            return self.error("404")
        else:
            return function(self, post_id, *args, **kwargs)
    return wrapper


def comment_exists(function):
    @wraps(function)
    def wrapper(self, post_id, comment_id, *args, **kwargs):
        key = db.Key.from_path('Comment', int(comment_id))
        comment_object = db.get(key)
        if not comment_object:
            return self.error("404")
        else:
            return function(self, post_id, comment_id, *args, **kwargs)
    return wrapper


def user_logged_in(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if not self.user:
            return self.redirect("/login")
        else:
            return function(self, *args, **kwargs)
    return wrapper


def user_owns_post(function):
    @wraps(function)
    def wrapper(self, post_id, *args, **kwargs):
        session_user_id = self.read_secure_cookie('user_id')
        post_user_id = self.request.get('post_user_id')
        if not int(post_user_id) == int(session_user_id):
            error = "You can only delete your own post"
            return self.get(post_id, error)
        else:
            return function(self, *args, **kwargs)
    return wrapper


def user_owns_comment(function):
    @wraps
    def wrapper(self, post_id, comment_id, *args, **kwargs):
        session_user_id = self.request.get('session_user_id')
        key = db.Key.from_path('Comment', int(comment_id))
        comment_object = db.get(key)
        if not int(session_user_id) == int(comment_object.user_id):
            return self.error("404")
        else:
            return function(self, *args, **kwargs)
    return wrapper
