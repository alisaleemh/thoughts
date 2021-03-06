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



class DeleteComment(PostPage):
    @post_exists
    @comment_exists
    @user_logged_in
    def get(self, post_id, comment_id):
        if not self.user:
            return self.redirect('/blog')

        session_user_id = self.read_secure_cookie('user_id')
        key = db.Key.from_path('Comment', int(comment_id))
        comment = db.get(key)
        if int(session_user_id) == int(comment.user_id):
            comment.delete()
            time.sleep(0.2)
            return self.redirect("/blog/%s" % post_id)
        else:
            error = "You can only delete your own comment"
            self.redirect("/blog/%s" % post_id)
            return PostPage.get(self, post_id, error)
