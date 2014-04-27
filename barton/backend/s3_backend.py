import boto
import pytz
import urllib
from datetime import datetime

class Media(object):
    def __init__(self):
        self.s3 = boto.connect_s3()

    def write_key(self, blogid, path, data, headers, policy='public-read'):
        bucket = self.s3.lookup(blogid)
        if bucket is None:
            bucket = self.s3.create_bucket(blogid)
        key = bucket.new_key(path)
        return key.set_contents_from_string(
            data, headers=headers, policy=policy)

    def new_media_object(self, blogid, struct):
        now = datetime.now(pytz.utc)
        path = 'uploads/%s/%s' % (
            now.strftime('%Y/%m/%d'),
            struct['name'],
        )
        headers = {'Content-Type': struct['type']}
        key = self.write_key(blogid, path, struct['bits'].data, headers=headers)
        return {
            'url': 'https://s3.amazonaws.com/%s/%s' % (blogid, urllib.quote(key.name)),
        }
