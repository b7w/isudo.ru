# -*- coding: utf-8 -*-
import re

import yaml
from yaml.error import MarkedYAMLError

from isudo.post import Meta, Post
from isudo.utils import url, BlogError


class Resource:
    """
    Some hack to replace relative resource links in `.md` to absolute,
    and copy resource.

    `![](~image.png)` -> `![](/2012/10/post-name/image.png)`

    `RE` field - find all resources
    `render` - make new text
    `replace` - replace old to new
    """
    RE = re.compile('\(~[\w\./-]+\)')

    def __init__(self, text, post):
        """
        :type text: str
        :type post: blog.post.Post
        """
        self.text = text
        self.post = post
        self.body = text[2:-1].strip()

    def render(self):
        return '(%s)' % url(self.post.url, self.body, last=False)

    def replace(self, text):
        return text.replace(self.text, self.render())

    def __repr__(self):
        return 'Resource{%s}' % self.body


class Reader:
    """
    Call `read` to read md file with `path`.
    Not thread safe.
    """

    def read_meta(self, meta):
        try:
            meta = meta.replace('#', '')
            meta = yaml.load(meta)
            if set(meta.keys()).issuperset(['title', 'url', 'time']):
                return Meta.fromDict(meta)
        except MarkedYAMLError as e:
            raise BlogError('Reading meta in "{0}"\n{1}'.format(self.path, e))

    def process(self, raw):
        meta, text = raw.split('\n\n', maxsplit=1)
        meta = self.read_meta(meta)
        if not meta:
            raise BlogError('Post "{0}" meta need at least [title, url, time]'.format(self.path))

        post = Post(self.path, meta, text.strip())
        post.resources = [Resource(i, post) for i in Resource.RE.findall(text)]
        return post

    def read(self, path):
        try:
            self.path = path
            with open(path, encoding='utf8') as f:
                raw = f.read().strip()
            return self.process(raw)
        except Exception as e:
            raise BlogError('Reading in "{0}"\n{1}'.format(self.path, e))