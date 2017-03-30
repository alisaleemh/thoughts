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
from handlers.signup import Signup


from helpers import *
from decorators import *

#template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
#                               autoescape=True)


# class BlogHandler(webapp2.RequestHandler):
#     def write(self, *a, **kw):
#         self.response.out.write(*a, **kw)
#
#     def render_str(self, template, **params):
#         params['user'] = self.user
#         return render_str(template, **params)
#
#     def render(self, template, **kw):
#         self.write(self.render_str(template, **kw))
#
#     def set_secure_cookie(self, name, val):
#         cookie_val = make_secure_val(val)
#         self.response.headers.add_header(
#             'Set-Cookie',
#             '%s=%s; Path=/' % (name, cookie_val))
#
#     def read_secure_cookie(self, name):
#         cookie_val = self.request.cookies.get(name)
#         return cookie_val and check_secure_val(cookie_val)
#
#     def login(self, user):
#         self.set_secure_cookie('user_id', str(user.key().id()))
#
#     def logout(self):
#         self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
#
#     def initialize(self, *a, **kw):
#         webapp2.RequestHandler.initialize(self, *a, **kw)
#         uid = self.read_secure_cookie('user_id')
#         self.user = uid and User.by_id(int(uid))


# class MainPage(BlogHandler):
#     def get(self):
#         self.redirect('/blog')


# class BlogFront(BlogHandler):
#     def get(self, error=None):
#         posts = Post.all().order('-created')
#         print posts
#         self.render('front.html', posts=posts, error=error)
#
#     # def post(self):
#     #     # Get the post user ID
#     #     post_user_id = self.request.get('post_user_id')
#     #     session_user_id = self.read_secure_cookie('user_id')
#     #     if post_user_id:
#     #         if session_user_id != '':
#     #             if int(post_user_id) == int(session_user_id):
#     #                 post_object = Post.by_user_id(post_user_id)
#     #                 post_object.delete()
#     #                 time.sleep(0.1)
#     #                 self.redirect("/blog")

# class PostPage(BlogHandler):
#
#     @post_exists
#     def get(self, post_id, error=None):
#         if not self.user:
#             return self.redirect('/blog')
#
#         session_user_id = self.read_secure_cookie('user_id')
#         key = db.Key.from_path('Post', int(post_id), parent=blog_key())
#         post = db.get(key)
#         comments = Comment.by_post_id(post_id)
#         likes = Like.by_post_id(post_id)
#
#         if likes:
#             for like in likes:
#                 likes_count = like.like_count
#                 if int(session_user_id) in like.post_user_id:
#                     like_bool = 'Unlike'
#                 if int(session_user_id) not in like.post_user_id:
#                     like_bool = 'Like'
#         else:
#             likes_count = 0
#
#         # TODO Session user Id needs validation for displaying delete button
#         if comments:
#             if error:
#                 return self.render("permalink.html", post=post, comments=comments, error=error, likes=likes, session_user_id=session_user_id, likes_count=likes_count, like_bool=like_bool)
#             else:
#                 return self.render("permalink.html", post=post, comments=comments, likes=likes, session_user_id=session_user_id, likes_count=likes_count, like_bool=like_bool)
#         else:
#             if error:
#                 return self.render("permalink.html", post=post, comments=comments, likes=likes, error=error, session_user_id=session_user_id, likes_count=likes_count, like_bool=like_bool)
#             else:
#                 return self.render("permalink.html", post=post, comments=comments, likes=likes, session_user_id=session_user_id, likes_count=likes_count, like_bool=like_bool)
#
#     @user_logged_in
#     @post_exists
#     def post(self,post_id):
#         # Get the post user ID from hidden input
#         session_user_id = self.read_secure_cookie('user_id')
#         post_user_id = self.request.get('post_user_id')
#         like_bool = 'Like'
#
#         # Get the hidden inputs to decide which functionality is required
#         delete_post = self.request.get('delete_post')
#         add_comment = self.request.get('add_comment')
#         delete_comment = self.request.get('delete_comment')
#         edit_post = self.request.get('edit_post')
#         edit_comment = self.request.get('edit_comment')
#         like_post = self.request.get('like_post')
#
#         # delete functionality
#         if delete_post:
#             if int(post_user_id) == int(session_user_id):
#                 post_object = Post.by_user_id(post_user_id)
#                 post_object.delete()
#                 time.sleep(0.1)
#                 return self.redirect("/blog")
#             else:
#                 error = "You can only delete your own post"
#                 return self.get(post_id, error)
#
#         # Add comment
#         if add_comment:
#             comment = self.request.get('comment')
#             print comment
#             if comment and session_user_id:
#                 c = Comment(user_id=session_user_id, post_id=post_id, comment=comment)
#                 c.put()
#                 time.sleep(0.1)
#                 return self.get(post_id)
#             else:
#                 error = 'Please enter a comment!'
#                 return self.get(post_id, error)
#
#         # Delete Comment
#         if delete_comment:
#             comment_id = self.request.get('comment_id')
#             key = db.Key.from_path('Comment', int(comment_id))
#             comment_object = db.get(key)
#             if int(session_user_id) == int(comment_object.user_id):
#                 comment_object.delete()
#                 time.sleep(0.2)
#                 return self.get(post_id)
#             else:
#                 error = "You can only delete your own comment"
#                 return self.get(post_id, error)
#
#         # Edit Post
#         if edit_post:
#             if int(post_user_id) == int(session_user_id):
#                 return self.redirect("/blog/%s/editpost" % post_id)
#             else:
#                 error = "This is not your post"
#                 return self.get(post_id, error)
#
#         if edit_comment:
#             comment_id = self.request.get('comment_id')
#             key = db.Key.from_path('Comment', int(comment_id))
#             comment = db.get(key)
#             if int(comment.user_id) == int(session_user_id):
#                 return self.redirect("/blog/%s/editcomment/%s" % (post_id, comment_id))
#             else:
#                 error = "This is not your comment"
#                 return self.get(post_id, error)
#
#         # Like Feature
#         if like_post:
#             l = Like.by_post_id(post_id)
#             for like in l:
#                 if like:
#                     if int(session_user_id) == int(post_user_id):
#                         error = "Can't like your own post"
#                         return self.get(post_id, error)
#                     if int(session_user_id) in like.post_user_id:
#                         like_bool = "Unlike"
#                         like.like_count -= 1
#                         like.post_user_id.remove(int(session_user_id))
#                         like.put()
#                         time.sleep(0.2)
#                         return self.get(post_id)
#                     else:
#                         like.like_count += 1
#                         like.post_user_id.append(int(session_user_id))
#                         like.put()
#                         time.sleep(0.2)
#                         return self.get(post_id)
#
#                 else:
#                     error = "Error"
#                     return self.get(post_id, error)


# class NewPost(BlogHandler):
#     def get(self):
#         if self.user:
#             return self.render("newpost.html")
#         else:
#             return self.redirect("/login")
#
#     def post(self):
#         if not self.user:
#             return self.redirect('/blog')
#
#         subject = self.request.get('subject')
#         content = self.request.get('content')
#         user_id = self.read_secure_cookie('user_id')
#
#         if subject and content:
#             p = Post(parent=blog_key(), user_id=user_id, subject=subject, content=content)
#             p.put()
#             like_count = 0
#             post_id = str(p.key().id())
#             l = Like(like_count=like_count, post_id=post_id)  # Create the like entity for this post
#             l.put()
#             time.sleep(0.1)
#             return self.redirect('/blog/%s' % str(p.key().id()))
#         else:
#             error = "subject and content, please!"
#             self.render("newpost.html", subject=subject, content=content, error=error)


# class EditPost(BlogHandler):
#     def get(self, post_id):
#         if self.user:
#             key = db.Key.from_path('Post', int(post_id), parent=blog_key())
#             post = db.get(key)
#             subject = post.subject
#             content = post.content
#             self.render("editpost.html", subject=subject, content=content)
#         else:
#             self.redirect("/blog/%s" % post_id)
#
#     def post(self, post_id):
#         subject = self.request.get('subject')
#         content = self.request.get('content')
#         user_id = self.read_secure_cookie('user_id')
#
#         if subject and content:
#             key = db.Key.from_path('Post', int(post_id), parent=blog_key())
#             p = db.get(key)
#             p = Post(key=key, parent=blog_key(), user_id=user_id, subject=subject, content=content)
#             p.put()
#             self.redirect('/blog/%s' % post_id)
#         else:
#             error = "Please enter both subject and content, please!"
#             self.render("editpost.html", subject=subject, content=content, error=error)

# class EditComment(BlogHandler):
#     def get(self, post_id, comment_id):
#         if self.user:
#             key = db.Key.from_path('Comment', int(comment_id))
#             c = db.get(key)
#             comment = c.comment
#             self.render("editcomment.html", comment=comment)
#         else:
#             self.redirect("/blog/%s" % post_id)
#
#     def post(self, post_id, comment_id):
#         comment = self.request.get('comment')
#         user_id = self.read_secure_cookie('user_id')
#         cancel_comment = self.request.get('cancel_comment')
#         if cancel_comment:
#             return self.redirect('/blog/%s' % post_id)
#         elif comment:
#             key = db.Key.from_path('Comment', int(comment_id))
#             c = db.get(key)
#             c = Comment(key=key, user_id=user_id, post_id=post_id, comment=comment)
#             c.put()
#             time.sleep(0.2)
#             return self.redirect('/blog/%s' % post_id)
#         else:
#             error = "Please enter a comment!"
#             return self.render("editpost.html", comment=comment, error=error)


# class Signup(BlogHandler):
#     def get(self):
#         self.render("signup-form.html")
#
#     def post(self):
#         have_error = False
#         self.username = self.request.get('username')
#         self.password = self.request.get('password')
#         self.verify = self.request.get('verify')
#         self.email = self.request.get('email')
#
#         params = dict(username=self.username,
#                       email=self.email)
#
#         if not valid_username(self.username):
#             params['error_username'] = "That's not a valid username."
#             have_error = True
#
#         if not valid_password(self.password):
#             params['error_password'] = "That wasn't a valid password."
#             have_error = True
#         elif self.password != self.verify:
#             params['error_verify'] = "Your passwords didn't match."
#             have_error = True
#
#         if not valid_email(self.email):
#             params['error_email'] = "That's not a valid email."
#             have_error = True
#
#         if have_error:
#             self.render('signup-form.html', **params)
#         else:
#             self.done()
#
#     def done(self, *a, **kw):
#         raise NotImplementedError


# class Register(Signup):
#     def done(self):
#         # make sure the user doesn't already exist
#         u = User.by_name(self.username)
#         if u:
#             msg = 'That user already exists.'
#             self.render('signup-form.html', error_username=msg)
#         else:
#             u = User.register(self.username, self.password, self.email)
#             u.put()
#
#             self.login(u)
#             self.redirect('/blog')


# class Login(BlogHandler):
#     def get(self):
#         self.render('login-form.html')
#
#     def post(self):
#         username = self.request.get('username')
#         password = self.request.get('password')
#
#         u = User.login(username, password)
#         if u:
#             self.login(u)
#             self.redirect('/blog')
#         else:
#             msg = 'Invalid login'
#             self.render('login-form.html', error=msg)


# class Logout(BlogHandler):
#     def get(self):
#         self.logout()
#         self.redirect('/blog')

# class Welcome(BlogHandler):
#     def get(self):
#         if self.user:
#             self.render('welcome.html', username=self.user.name)
#         else:
#             self.redirect('/signup')


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
