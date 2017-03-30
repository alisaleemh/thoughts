# Handlers
from handlers.bloghandler import BlogHandler

from helpers import *
from decorators import *


class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/blog')
