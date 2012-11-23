# -*- coding: utf-8 -*-
import re

import yaml

from isudo.post import Meta, Post
from isudo.utils import url


class Macros:
    def __init__(self, text, post):
        """
        :type text: str
        :type post: blog.post.Post
        """
        self.md = text
        self.post = post
        name, body = text[:-1].split('{')
        self.name = name.strip()
        self.body = body.strip()

    def render(self, post):
        raise NotImplementedError()

    def replace(self, text):
        return text.replace(self.md, self.render(self.post))

    def __repr__(self):
        return 'Macros{%s, %s}' % (self.name, self.body)


class IconMacros(Macros):
    def render(self, post):
        t = """<a href="{url}"><img src="{image}" class="align-left"/></a>"""
        image = url(post.url, self.body, last=False)
        return t.format(url=post.url, image=image)


class ImageMacros(Macros):
    def render(self, post):
        t = """<a href="{image}"><img src="{image}" class="align-center"/></a>"""
        image = url(post.url, self.body, last=False)
        return t.format(image=image)


class Reader:
    ICON = re.compile('icon\{\s*[\w\./-]+\s*}')
    IMAGE = re.compile('image\{\s*[\w\./-]+\s*}')

    def read(self, path):
        with open(path, encoding='utf8') as f:
            raw = f.read().strip()

        meta, text = raw.split('\n\n', maxsplit=1)
        meta = meta.replace('#', '')
        meta = Meta.fromDict(yaml.load(meta))

        post = Post(path, meta, text.strip())
        post.resources = self.find_macros(text, post)
        return post

    def find_macros(self, text, post):
        """
        :type text: str
        :rtype: str
        """
        macros = [IconMacros(i, post) for i in self.ICON.findall(text)]
        macros.extend(ImageMacros(i, post) for i in self.IMAGE.findall(text))
        return macros
