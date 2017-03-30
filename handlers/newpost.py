# Models
from models.post import Post
from models.like import Like

from handlers.bloghandler import BlogHandler
import time


from helpers import *
from decorators import *


class NewPost(BlogHandler):
    def get(self):
        if self.user:
            return self.render("newpost.html")
        else:
            return self.redirect("/login")

    def post(self):
        if not self.user:
            return self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')
        user_id = self.read_secure_cookie('user_id')

        if subject and content:
            p = Post(parent=blog_key(), user_id=user_id, subject=subject, content=content)
            p.put()
            like_count = 0
            post_id = str(p.key().id())
            l = Like(like_count=like_count, post_id=post_id)  # Create the like entity for this post
            l.put()
            time.sleep(0.1)
            return self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)
