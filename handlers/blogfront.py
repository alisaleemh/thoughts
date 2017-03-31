# Models
from models.post import Post

# Handlers
from handlers.bloghandler import BlogHandler

from helpers import *
from decorators import *


class BlogFront(BlogHandler):
    def get(self, error=None):
        posts = Post.all().order('-created')
        self.render('front.html', posts=posts, error=error)
