from google.appengine.ext import db
from helpers import *
from user import User



class Comment(db.Model):
    comment_id = db.Key()
    user_id = db.StringProperty(required=True)
    post_id = db.StringProperty(required=True)
    comment = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def by_user_id(cls, user_id):
        c = Comment.all().filter('user_id =', user_id).get()
        return c

    @classmethod
    def by_post_id(cls, post_id):
        c = Comment.all().filter('post_id =', post_id).fetch(99999999)
        return c

    @classmethod
    def by_id(cls, comment_id):
        c = Comment.all().filter('comment_id =', comment_id).get()
        return c

    def render(self, session_user_id):
        self._render_text = self.comment.replace('\n', '<br>')
        return render_str("comment.html", c=self, u=User.by_id(int(self.user_id)), session_user_id=session_user_id)
