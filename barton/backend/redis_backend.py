import time
import redis
import xmlrpclib

class Store(object):
    def __init__(self):
        self.redis = redis.Redis()

    def new_post(self, postid, struct):
        self.redis.hmset(postid, struct)
        self.increment_saves(postid)
        self.add_to_sorted_set(postid)
        return postid

    def edit_post(self, postid, struct):
        obj = self.redis.hgetall(postid)
        obj.update(struct)
        self.redis.hmset(postid, obj)
        self.increment_saves(postid)
        return True

    def get_post(self, postid):
        obj = self.redis.hgetall(postid)
        return self.hydrate_objects(obj)

    def delete_post(self, postid):
        self.redis.delete(postid)
        self.remove_from_sorted_set(postid)
        return True

    def get_recent_posts(self, blogid, post_count):
        keys = self.redis.zrevrange(blogid, 0, post_count - 1)
        pipe = self.redis.pipeline()
        for key in keys:
            pipe.hgetall(key)
        for obj in pipe.execute():
            yield self.hydrate_objects(obj)

    ###########################################################################
    # Helper methods

    def add_to_sorted_set(self, postid):
        (blogid, _) = postid.split(':')
        self.redis.zadd(blogid, postid, time.time())

    def remove_from_sorted_set(self, postid):
        (blogid, _) = postid.split(':')
        self.redis.zrem(blogid, postid)

    def hydrate_objects(self, obj):
        """
        Turn str values into proper XML-RPC types.
        """
        if 'dateCreated' in obj:
            obj['dateCreated'] = xmlrpclib.DateTime(obj['dateCreated'])

        if 'dateModified' in obj:
            obj['dateModified'] = xmlrpclib.DateTime(obj['dateModified'])

        if 'flNotOnHomePage' in obj:
            value = obj['flNotOnHomePage']
            obj['flNotOnHomePage'] = {'True': True, 'False': False}[value]

        if 'ctSaves' in obj:
            obj['ctSaves'] = int(obj['ctSaves'])

        return obj
                
    def increment_saves(self, postid):
        self.redis.hincrby(postid, 'ctSaves', 1)
