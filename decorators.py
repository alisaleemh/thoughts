from helpers import *
from google.appengine.ext import db


def post_exists(function):
    @wraps(function)
    def wrapper(self, post_id, *args):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if not post:
            return self.write("tatta")
        else:
            return function(self, post_id, *args)
    return wrapper


def comment_exists(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        comment_id = self.request.get('comment_id')
        key = db.Key.from_path('Comment', int(comment_id))
        comment_object = db.get(key)
        if not comment_object:
            return self.error(404)
        else:
            return function(self, *args, **kwargs)
    return wrapper


def user_logged_in(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if not self.user:
            error = "You are not logged in. Please login or signup"
            return self.render("login-form.html", error=error)
        else:
            return function(self, *args, **kwargs)
    return wrapper


def user_owns_post(function):
    @wrap
    def wrapper(self, *args, **kwargs):
        session_user_id = self.read_secure_cookie('user_id')
        post_user_id = self.request.get('post_user_id')
        if not int(post_user_id) == int(session_user_id):
            error = "You can only delete your own post"
            return self.get(post_id, error)
        else:
            return function(self, *args, **kwargs)
    return wrapper


def user_owns_comment(function):
    @wrap
    def wrapper(self, *args, **kwargs):
        comment_id = self.request.get('comment_id')
        key = db.Key.from_path('Comment', int(comment_id))
        comment_object = db.get(key)
        if not int(session_user_id) == int(comment_object.user_id):
            error = "You can only delete your own comment"
            return self.get(post_id, error)
        else:
            return function(self, *args, **kwargs)
