import os

import webapp2
import jinja2
import string
from google.appengine.ext import db

template_dir = os.path.dirname(__file__)
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)



class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

def blog_key(name = 'default'):
    return db.key.from_path('blogs', name)

#Datastore Object for storing blogs
class Blog(db.Model):
    title = db.StringProperty(required = True)
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

#NewLine replacement
    def render(self):
        self._render = self.content.replace('\n', '<br>')
        return render_str('html/post.html', p = self)

#Front Page listing 10 most recent blog entries
class MainPage(Handler):

    def render_front(self):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 10")
        self.render("html/front_page.html", blogs=blogs)

    def get(self):
        self.render_front()


#NewPost Page
class NewPost(Handler):
    def render_newpost(self, title="", blog="", error=""):
        self.render("html/newpost.html", title=title, blog=blog, error=error)

    def get(self):
        self.render_newpost()
    #Getting the title and blog from the form
    def post(self):
        title = self.request.get("title")
        blog = self.request.get("blog")
    #Storing the title and blog in the datastore
        if title and blog:
            a = Blog(parent = blog_key(), title=title, blog = blog)
            a.put()
            self.redirect("html/post/%s" % str.a.key() )
    #Error handling
        else:
            error = "You need to enter a title and some blogwork. Thanks!"
            self.render_newpost(title=title, blog=blog, error = error)


#Permalink Page
class PostPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Blog', int(post_id),parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return
        self.render("html/permalink.html", post = post)




#Mapping of handlers to their urls
app = webapp2.WSGIApplication([('/blog/newpost', NewPost),('/blog', MainPage), ('/blog/[0-9]+', PostPage)],debug=True)
