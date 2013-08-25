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

    `![foo](~image.png)` -> `![foo](/2012/10/post-name/image.png)`
    `[~image.png]` -> `/2012/10/post-name/image.png`

    `RE` field - find all links resources
    `RE2` field - find all resources
    """
    RE = re.compile('\(~[\w\./-]+\)')
    RE2 = re.compile('\[~[\w\./-]+\]')

    def __init__(self, macros, post, type=RE):
        """
        :type macros: str
        :type post: blog.post.Post
        :type type: Resource.RE | Resource.RE2
        """
        self.macros = macros
        self.post = post
        self.type = type
        self.link = macros[2:-1].strip()

    @classmethod
    def findall(cls, post):
        """
        Return list of all resources in post.

        :rtype: list of Resource
        """
        out = []
        for res in Resource.RE.findall(post.text):
            out.append(Resource(res, post, type=cls.RE))
        for res in Resource.RE2.findall(post.text):
            out.append(Resource(res, post, type=cls.RE2))
        return out

    def render(self):
        link = url(self.post.url, self.link, last=False)
        if self.type == self.RE:
            return '({0})'.format(link)
        return link

    def replace(self, text):
        return text.replace(self.macros, self.render())

    def __repr__(self):
        return 'Resource{%s}' % self.link


class Reader:
    """
    Call `read` to read md file with `path`.
    Not thread safe.
    """

    def read_meta(self, meta):
        try:
            if not all(i.startswith('# ') for i in meta.split('\n')):
                raise BlogError('Meta not start with "# "\n\n{0}'.format(meta))
            meta = meta.replace('#', '')
            meta = yaml.load(meta)
            if set(meta.keys()).issuperset(['title', 'url', 'time']):
                return Meta.fromDict(meta)
        except MarkedYAMLError as e:
            raise BlogError('Reading meta in "{0}"\n{1}'.format(self.path, e))

    def process(self, raw):
        meta, text = raw.split('\n\n', 1)
        meta = self.read_meta(meta)
        if not meta:
            raise BlogError('Post "{0}" meta need at least [title, url, time]'.format(self.path))

        post = Post(self.path, meta, text.strip())
        post.resources = Resource.findall(post)
        return post

    def read(self, path):
        try:
            self.path = path
            with open(path, encoding='utf8') as f:
                raw = f.read().strip()
            return self.process(raw)
        except Exception as e:
            raise BlogError('Reading in "{0}"\n{1}'.format(self.path, e))