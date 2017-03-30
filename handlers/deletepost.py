# Models
from models.post import Post
from models.like import Like
from models.comment import Comment

# Handlers

from handlers.postpage import PostPage

from google.appengine.ext import db
from helpers import *
from decorators import *
import time


class DeletePost(PostPage):

    @post_exists
    def get(self, post_id):
        if not self.user:
            return self.redirect('/blog')
        session_user_id = self.read_secure_cookie('user_id')
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if int(post.user_id) == int(session_user_id):
            post.delete()
            time.sleep(0.1)
            return self.redirect("/blog")
        else:
            error = "You can only delete your own post"
            return PostPage.get(self, post_id, error)
