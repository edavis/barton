import pytz
import uuid
from datetime import datetime

from backend.redis_backend import Store
from backend.s3_backend import Media

class MetaWeblog(object):
    def __init__(self):
        self.tz = pytz.utc
        self.store = Store()
        self.media = Media()

    def _dispatch(self, method, params):
        lookup = {
            'metaWeblog.newPost': self.new_post,
            'metaWeblog.getPost': self.get_post,
            'metaWeblog.editPost': self.edit_post,
            'blogger.deletePost': self.delete_post,
            'metaWeblog.getRecentPosts': self.get_recent_posts,
            'metaWeblog.getCategories': self.get_categories,
            'metaWeblog.newMediaObject': self.new_media_object,
        }
        return lookup[method](*params)

    def current_timestamp(self):
        return datetime.now(self.tz).isoformat()

    def new_post(self, blogid, username, password, struct, publish):
        postid = '%s:%s' % (blogid, uuid.uuid4())
        struct.update({
            'postid': postid,
            'dateCreated': self.current_timestamp(),
        })
        return self.store.new_post(postid, struct)

    def edit_post(self, postid, username, password, struct, publish):
        struct.update({
            'dateModified': self.current_timestamp(),
        })
        return self.store.edit_post(postid, struct)

    def get_post(self, postid, username, password):
        return self.store.get_post(postid)

    def delete_post(self, appkey, postid, username, password, publish):
        return self.store.delete_post(postid)

    def get_recent_posts(self, blogid, username, password, post_count):
        return list(self.store.get_recent_posts(blogid, post_count))

    def get_categories(self, blogid, username, password):
        return []

    def new_media_object(self, blogid, username, password, struct):
        return self.media.new_media_object(blogid, struct)
