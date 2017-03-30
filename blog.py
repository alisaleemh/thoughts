import os
import re
import random
import hashlib
import hmac
from string import letters
import time

import webapp2
import jinja2
from google.appengine.ext import db


# Models
from models.user import User
from models.post import Post
from models.like import Like
from models.comment import Comment

# Handlers

from handlers.blogfront import BlogFront
from handlers.deletecomment import DeleteComment
from handlers.deletepost import DeletePost
from handlers.editcomment import EditComment
from handlers.editpost import EditPost
from handlers.login import Login
from handlers.logout import Logout
from handlers.mainpage import MainPage
from handlers.newpost import NewPost
from handlers.postpage import PostPage
from handlers.register import Register

from helpers import *
from decorators import *


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/blog/([0-9]+)/editpost', EditPost),
                               ('/blog/([0-9]+)/delete', DeletePost),
                               ('/blog/([0-9]+)/editcomment/([0-9]+)', EditComment),
                               ('/blog/([0-9]+)/delete/([0-9]+)', DeleteComment),
                               ('/signup', Register),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout)
                               ],
                              debug=True)
