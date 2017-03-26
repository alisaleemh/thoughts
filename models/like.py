from google.appengine.ext import db
from helpers import *




class Like(db.Model):
    like_count = db.IntegerProperty(required=True)
    post_id = db.StringProperty(required=True)
    post_user_id = db.ListProperty(int, default=[])

    @classmethod
    def by_post_id(cls, post_id):
        l = Like.all().filter('post_id =', str(post_id)).fetch(1)
        return l
