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

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

secret = 'fart'


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

# # # # #  user stuff
def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


def users_key(group='default'):
    return db.Key.from_path('users', group)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")


def valid_username(username):
    return username and USER_RE.match(username)


PASS_RE = re.compile(r"^.{3,20}$")


def valid_password(password):
    return password and PASS_RE.match(password)


EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_email(email):
    return not email or EMAIL_RE.match(email)

# # # # #  blog stuff

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))


class User(db.Model):
    user_id = db.Key()
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def by_post_id(cls, post_id):
        u = User.all().filter('name =', post_id).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    user_id=db.Key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


class Post(db.Model):
    post_id = db.Key()
    user_id = db.StringProperty(required=True)
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def by_user_id(cls, user_id):
        p = Post.all().filter('user_id =', user_id).get()
        return p

    def render(self, likes, error=None):
        self._render_text = self.content.replace('\n', '<br>')
        if error:
            return render_str("post.html", p=self, error=error, u=User.by_id(int(self.user_id)), likes=likes)
        else:
            return render_str("post.html", p=self, u=User.by_id(int(self.user_id)), likes=likes)

# Duplicated render function to render front-post.html to exclude delete and comment
    def render_front(self, error=None):
        self._render_text = self.content.replace('\n', '<br>')
        if error:
            return render_str("front-post.html", p=self, error=error, u=User.by_id(int(self.user_id)))
        else:
            return render_str("front-post.html", p=self, u=User.by_id(int(self.user_id)))


class Comment(db.Model):
    comment_id = db.Key()
    user_id = db.StringProperty(required=True)
    post_id = db.StringProperty(required=True)
    comment = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def by_user_id(cls, user_id):
        c = Comment.all().filter('user_id =', user_id).get()
        return c

    @classmethod
    def by_post_id(cls, post_id):
        c = Comment.all().filter('post_id =', post_id).fetch(99999999)
        return c

    @classmethod
    def by_id(cls, comment_id):
        c = Comment.all().filter('comment_id =', comment_id).get()
        return c

    def render(self, session_user_id):
        self._render_text = self.comment.replace('\n', '<br>')
        return render_str("comment.html", c=self, session_user_id=session_user_id)


class Like(db.Model):
    like_id = db.Key()
    like_count = db.IntegerProperty(required=True)
    post_id = db.StringProperty(required=True)
    post_user_id = db.ListProperty(int, default=[])

    @classmethod
    def by_post_id(cls, post_id):
        l = Like.all().filter('post_id =', post_id).fetch(1)
        return l


class MainPage(BlogHandler):
    def get(self):
        self.redirect('/blog')


class BlogFront(BlogHandler):
    def get(self, error=None):
        posts = Post.all().order('-created')
        self.render('front.html', posts=posts, error=error)

    def post(self):
        # Get the post user ID
        post_user_id = self.request.get('post_user_id')
        session_user_id = self.read_secure_cookie('user_id')
        if post_user_id:
            if session_user_id != '':
                if int(post_user_id) == int(session_user_id):
                    post_object = Post.by_user_id(post_user_id)
                    post_object.delete()
                    time.sleep(0.1)
                    self.redirect("/blog")


class CommentPage(BlogHandler):
    def get(self):
        comments = Comment.all()
        self.render("comment-test.html", comments=comments)


class PostPage(BlogHandler):
    def get(self, post_id, error=None):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        comments = Comment.by_post_id(post_id)
        likes = Like.by_post_id(post_id)
        # Session user Id needs validation for displaying delete button
        session_user_id = self.read_secure_cookie('user_id')
        if not post:
            return self.error(404)  # Should never reach here
        if comments:
            if error:
                return self.render("permalink.html", post=post, comments=comments, error=error, likes=likes, session_user_id=session_user_id)
            else:
                return self.render("permalink.html", post=post, comments=comments, likes=likes, session_user_id=session_user_id)
        else:
            if error:
                return self.render("permalink.html", post=post, comments=comments, likes=likes, error=error, session_user_id=session_user_id)
            else:
                return self.render("permalink.html", post=post, comments=comments, likes=likes, session_user_id=session_user_id)

    def post(self,post_id):
        # Get the post user ID from hidden input
        session_user_id = self.read_secure_cookie('user_id')
        post_user_id = self.request.get('post_user_id')

        # Get the hidden inputs to decide which functionality is required
        delete_post = self.request.get('delete_post')
        add_comment = self.request.get('add_comment')
        delete_comment = self.request.get('delete_comment')
        edit_post = self.request.get('edit_post')
        edit_comment = self.request.get('edit_comment')
        like_post = self.request.get('like_post')

        # delete functionality
        if delete_post:
            if int(post_user_id) == int(session_user_id):
                post_object = Post.by_user_id(post_user_id)
                post_object.delete()
                time.sleep(0.1)
                return self.redirect("/blog")
            else:
                error = "You can only delete your own post"
                return self.get(post_id, error)

        # Add comment
        if add_comment:
            comment = self.request.get('comment')
            if comment:
                if int(post_user_id) == int(session_user_id):
                    c = Comment(user_id=session_user_id, post_id=post_id, comment=comment)
                    c.put()
                    time.sleep(0.1)
                    return self.redirect("/blog/%s" % post_id)
            else:
                error = 'Please enter a comment!'
                return self.get(post_id, error)

        # Delete Comment
        if delete_comment:
            comment_id = self.request.get('comment_id')
            key = db.Key.from_path('Comment', int(comment_id))
            comment_object = db.get(key)
            if int(session_user_id) == int(comment_object.user_id):
                comment_object.delete()
                time.sleep(0.1)
                return self.redirect("/blog/%s" % post_id)
            else:
                error = "You can only delete your own comment"
                return self.get(post_id, error)

        # Edit Post
        if edit_post:
            if int(post_user_id) == int(session_user_id):
                return self.redirect("/blog/%s/editpost" % post_id)
            else:
                error = "This is not your post"
                return self.get(post_id, error)

        if edit_comment:
            comment_id = self.request.get('comment_id')
            key = db.Key.from_path('Comment', int(comment_id))
            comment = db.get(key)
            if int(comment.user_id) == int(session_user_id):
                return self.redirect("/blog/%s/editcomment/%s" % (post_id, comment_id))
            else:
                error = "This is not your comment"
                return self.get(post_id, error)

        # Like Feature
        if like_post:
            l = Like.by_post_id(post_id)
            for like in l:
                if int(like.post_id) != int(session_user_id):  # Check if the post_id belongs to the current logged in user
                    if int(session_user_id) in like.post_user_id:  # Check if the user has already liked the post
                        like.post_user_id.remove(int(session_user_id))  # Unlike the post
                        like.like_count = like.like_count - 1  # Decrease the like count
                        like.put()  # Update the datastore
                        time.sleep(0.1)
                        return self.get(post_id)
                    else:  # If the user has not liked, then increase count
                        print "Session User_ID: %d" % int(session_user_id)
                        like.post_user_id.insert(0, int(session_user_id))  # Add the current logged in user to
                        print like.post_user_id
                        like.like_count = int(like.like_count) + 1  # Increase the like_count
                        like.put()
                        time.sleep(0.1)
                        return self.get(post_id)
                else:
                    error = "You cannot like your own post"
                    return self.get(post_id, error=error)


class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')
        user_id = self.read_secure_cookie('user_id')

        if subject and content:
            p = Post(parent=blog_key(), user_id=user_id, subject=subject, content=content)
            p.put()
            self.like_count = 0
            self.post_id = str(p.key().id())
            l = Like(like_count=self.like_count, post_id=self.post_id)  # Create the like entity for this post
            l.put()
            time.sleep(0.1)
            return self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)


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
            self.redirect('/blog/%s' % post_id)
        else:
            error = "Please enter both subject and content, please!"
            self.render("editpost.html", subject=subject, content=content, error=error)

class EditComment(BlogHandler):
    def get(self, post_id, comment_id):
        if self.user:
            key = db.Key.from_path('Comment', int(comment_id))
            c = db.get(key)
            comment = c.comment
            self.render("editcomment.html", comment=comment)
        else:
            self.redirect("/blog/%s" % post_id)

    def post(self, post_id, comment_id):
        comment = self.request.get('comment')
        user_id = self.read_secure_cookie('user_id')

        if comment:
            key = db.Key.from_path('Comment', int(comment_id))
            c = db.get(key)
            c = Comment(key=key, user_id=user_id, post_id=post_id, comment=comment)
            c.put()
            time.sleep(0.1)
            self.redirect('/blog/%s' % post_id)
        else:
            error = "Please enter a comment!"
            self.render("editpost.html", comment=comment, error=error)


class Signup(BlogHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(Signup):
    def done(self):
        # make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/blog')


class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)


class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/blog')

class Welcome(BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/signup')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/blog/([0-9]+)/editpost', EditPost),
                               ('/blog/([0-9]+)/editcomment/([0-9]+)', EditComment),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/welcome', Welcome),
                               ('/comment', CommentPage)
                               ],
                              debug=True)
