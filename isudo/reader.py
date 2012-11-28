# -*- coding: utf-8 -*-
import re

import yaml

from isudo.post import Meta, Post
from isudo.utils import url, BlogError


class Resource:
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
    def read(self, path):
        with open(path, encoding='utf8') as f:
            raw = f.read().strip()

        meta, text = raw.split('\n\n', maxsplit=1)
        meta = meta.replace('#', '')
        meta = yaml.load(meta)
        if not set(meta.keys()).issuperset(['title', 'url', 'time']):
            raise BlogError('Post "{0}" meta need at least [title, url, time]'.format(path))
        meta = Meta.fromDict(meta)

        post = Post(path, meta, text.strip())
        post.resources = [Resource(i, post) for i in Resource.RE.findall(text)]
        return post