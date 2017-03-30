# Models
from models.post import Post
from models.like import Like

# Handlers

from handlers.postpage import PostPage

from google.appengine.ext import db
from helpers import *
from decorators import *
import time


class LikePost(PostPage):
    @post_exists
    def get(self, post_id):
        l = Like.by_post_id(post_id)
        session_user_id = self.read_secure_cookie('user_id')
        for like in l:
            if like:
                if int(session_user_id) in like.post_user_id:
                    like_bool = "Unlike"
                    like.like_count -= 1
                    like.post_user_id.remove(int(session_user_id))
                    like.put()
                    time.sleep(0.2)
                    return self.redirect("/blog/%s" % post_id)
                else:
                    like.like_count += 1
                    like.post_user_id.append(int(session_user_id))
                    like.put()
                    time.sleep(0.2)
                    return PostPage.get(self, post_id)

            else:
                error = "Error"
                return PostPage.get(self, post_id, error)
