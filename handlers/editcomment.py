# Models
from models.comment import Comment

# Handlers

from handlers.bloghandler import BlogHandler


from helpers import *
from decorators import *
import time


class EditComment(BlogHandler):
    @post_exists
    @comment_exists
    @user_logged_in
    def get(self, post_id, comment_id):
        if self.user:
            key = db.Key.from_path('Comment', int(comment_id))
            c = db.get(key)
            comment = c.comment
            self.render("editcomment.html", comment=comment)
        else:
            self.redirect("/blog/%s" % post_id)

    @post_exists
    @comment_exists
    @user_logged_in
    @user_owns_comment
    def post(self, post_id, comment_id):
        comment = self.request.get('comment')
        user_id = self.read_secure_cookie('user_id')
        cancel_comment = self.request.get('cancel_comment')
        if cancel_comment:
            return self.redirect('/blog/%s' % post_id)
        elif comment:
            key = db.Key.from_path('Comment', int(comment_id))
            c = db.get(key)
            c = Comment(key=key, user_id=user_id, post_id=post_id, comment=comment)
            c.put()
            time.sleep(0.2)
            return self.redirect('/blog/%s' % post_id)
        else:
            error = "Please enter a comment!"
            return self.render("editcomment.html", comment=comment, error=error)
