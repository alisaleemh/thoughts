# Models
from models.post import Post

# Handlers
from handlers.bloghandler import BlogHandler

from helpers import *
from decorators import *


class BlogFront(BlogHandler):
    def get(self, error=None):
        posts = Post.all().order('-created')
        print posts
        self.render('front.html', posts=posts, error=error)

    # def post(self):
    #     # Get the post user ID
    #     post_user_id = self.request.get('post_user_id')
    #     session_user_id = self.read_secure_cookie('user_id')
    #     if post_user_id:
    #         if session_user_id != '':
    #             if int(post_user_id) == int(session_user_id):
    #                 post_object = Post.by_user_id(post_user_id)
    #                 post_object.delete()
    #                 time.sleep(0.1)
    #                 self.redirect("/blog")
