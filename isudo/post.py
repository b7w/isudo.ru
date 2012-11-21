# -*- coding: utf-8 -*-
from datetime import datetime

from markdown import markdown

import conf
from isudo.utils import urljoin, filejoin


class Meta:
    def __init__(self):
        self.title = None
        self.url = None
        self.tags = []
        self.categories = []
        self.type = 'post'
        self.time = datetime.now()


    @classmethod
    def fromDict(cls, value):
        """
        :type value: dict
        :rtype: Meta
        """
        m = Meta()
        m.title = value['title']
        m.url = value['url']
        m.tags = value.get('tags', [])
        m.categories = value.get('categories', [])
        m.type = value.get('type', m.type)
        m.time = value['time']
        assert isinstance(m.time, datetime)
        return m

    def __repr__(self):
        return 'Meta{{{0}}}'.format(self.title)


class Post:
    def __init__(self, path, meta, post):
        """
        :type meta: Meta
        :type post: str
        """
        self.path = path
        self.meta = meta
        self.post = post
        self.resources = []

    def render(self):
        return self._render(self.post.replace('[more]', ''))

    def render_short(self):
        index = self.post.find('[more]')
        if index > 0:
            return self._render(self.post[0:index])
        return self.render()

    def _render(self, text):
        for res in self.resources:
            text = res.replace(text)
        return markdown(text)

    @property
    def title(self):
        return self.meta.title

    def _url(self, func):
        """
        http abs url
        """
        if self.meta.url.startswith('/'):
            return self.meta.url
        folder = conf.POST_PATH_STYLE.format(date=self.meta.time)
        return func(*(folder, self.meta.url))

    @property
    def url(self):
        """
        http abs url
        """
        return self._url(urljoin)

    @property
    def furl(self):
        """
        file relative url
        """
        return self._url(filejoin)

    def __repr__(self):
        return "Post{{{0},{1}}}".format(self.meta, self.post)