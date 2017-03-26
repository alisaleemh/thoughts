from google.appengine.ext import db
from helpers import *
from user import User




class Post(db.Model):
    post_id = db.Key()
    user_id = db.StringProperty(required=True)
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def by_user_id(cls, user_id):
        p = Post.all().filter('user_id =', user_id).get()
        return p

    def render(self, likes, likes_count, like_bool, error=None):
        self._render_text = self.content.replace('\n', '<br>')
        if error:
            return render_str("post.html", p=self, error=error, u=User.by_id(int(self.user_id)), likes=likes, likes_count=likes_count, like_bool=like_bool)
        else:
            return render_str("post.html", p=self, u=User.by_id(int(self.user_id)), likes=likes, likes_count=likes_count, like_bool=like_bool)

# Duplicated render function to render front-post.html to exclude delete and comment
    def render_front(self, error=None):
        self._render_text = self.content.replace('\n', '<br>')
        if error:
            return render_str("front-post.html", p=self, error=error, u=User.by_id(int(self.user_id)))
        else:
            return render_str("front-post.html", p=self, u=User.by_id(int(self.user_id)))
