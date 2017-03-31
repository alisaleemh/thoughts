# Models
from models.post import Post
from models.like import Like
from models.comment import Comment

# Handlers

from handlers.bloghandler import BlogHandler

from google.appengine.ext import db
from helpers import *
from decorators import *
import time


class PostPage(BlogHandler):

    @post_exists
    @user_logged_in
    def get(self, post_id, error=None):


        session_user_id = self.read_secure_cookie('user_id')
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        comments = Comment.by_post_id(post_id)
        likes = Like.by_post_id(post_id)

        if likes:
            for like in likes:
                likes_count = like.like_count
                if int(session_user_id) in like.post_user_id:
                    like_bool = 'Unlike'
                if int(session_user_id) not in like.post_user_id:
                    like_bool = 'Like'
        else:
            likes_count = 0

        # TODO Session user Id needs validation for displaying delete button
        if comments:
            if error:
                return self.render("permalink.html", post=post, comments=comments, error=error, likes=likes, session_user_id=session_user_id, likes_count=likes_count, like_bool=like_bool)
            else:
                return self.render("permalink.html", post=post, comments=comments, likes=likes, session_user_id=session_user_id, likes_count=likes_count, like_bool=like_bool)
        else:
            if error:
                return self.render("permalink.html", post=post, comments=comments, likes=likes, error=error, session_user_id=session_user_id, likes_count=likes_count, like_bool=like_bool)
            else:
                return self.render("permalink.html", post=post, comments=comments, likes=likes, session_user_id=session_user_id, likes_count=likes_count, like_bool=like_bool)

    @user_logged_in
    @post_exists
    def post(self, post_id):
        # Get the post user ID from hidden input
        session_user_id = self.read_secure_cookie('user_id')
        post_user_id = self.request.get('post_user_id')
        like_bool = 'Like'

        # Get the hidden inputs to decide which functionality is required
        delete_post = self.request.get('delete_post')
        add_comment = self.request.get('add_comment')
        delete_comment = self.request.get('delete_comment')
        edit_post = self.request.get('edit_post')
        edit_comment = self.request.get('edit_comment')
        like_post = self.request.get('like_post')


        # Add comment
        if add_comment:
            comment = self.request.get('comment')
            print comment
            if comment and session_user_id:
                c = Comment(user_id=session_user_id, post_id=post_id, comment=comment)
                c.put()
                time.sleep(0.1)
                return self.get(post_id)
            else:
                error = 'Please enter a comment!'
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
            if int(post_user_id) == int(session_user_id):
                error = "You can't like your own post"
                return self.get(post_id, error)
            else:
                return self.redirect("/blog/%s/like" % post_id)
