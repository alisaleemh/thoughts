# Handlers

from handlers.bloghandler import BlogHandler


from helpers import *
from decorators import *


class MainPage(BlogHandler):
    def get(self):
        self.redirect('/blog')
