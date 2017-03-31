# Models
from models.post import Post

# Handlers

from handlers.bloghandler import BlogHandler

from helpers import *
from decorators import *
import time


class EditPost(BlogHandler):
    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            subject = post.subject
            content = post.content
            self.render("editpost.html", subject=subject, content=content)
        else:
            self.redirect("/blog/%s" % post_id)

    def post(self, post_id):
        subject = self.request.get('subject')
        content = self.request.get('content')
        user_id = self.read_secure_cookie('user_id')

        if subject and content:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            p = db.get(key)
            p = Post(key=key, parent=blog_key(), user_id=user_id, subject=subject, content=content)
            p.put()
            time.sleet(0.2)
            self.redirect('/blog/%s' % post_id)
        else:
            error = "Please enter both subject and content, please!"
            self.render("editpost.html", subject=subject, content=content, error=error)