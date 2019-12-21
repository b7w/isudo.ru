# -*- coding: utf-8 -*-
import re
from datetime import datetime

from markdown import markdown

from isudo import conf
from isudo.utils import urljoin, filejoin, BlogError


class Meta:
    def __init__(self):
        self.title = None
        self.draft = False
        self.url = None
        self.tags = []
        self.categories = []
        self.type = 'post'
        self.time = datetime.now(tz=conf.TIME_ZONE)

    @classmethod
    def from_dict(cls, value):
        """
        :type value: dict
        :rtype: Meta
        """
        m = Meta()
        m.title = value['title']
        m.draft = value.get('draft', m.draft)
        m.url = value['url']
        m.tags = value.get('tags', [])
        m.categories = value.get('categories', [])
        m.type = value.get('type', m.type)
        m.time = value['time']
        assert isinstance(m.time, datetime)
        m.time = m.time.replace(tzinfo=conf.TIME_ZONE)
        return m

    def __repr__(self):
        return 'Meta{{{0}}}'.format(self.title)


class Post:
    def __init__(self, path, meta, text):
        """
        :type meta: Meta
        :type text: str
        """
        self.path = path
        self.meta = meta
        self.text = text
        self.resources = []

    def render(self):
        text = self.text.replace('[more]', '')
        text = text.replace('[clear]', '<div class="fixed"></div>')
        return self._render(text)

    def render_short(self, images=True):
        """
        If `images=False` - `![]()` will be removed
        If not tag more - BlogError will be raised
        """
        text = self.text.replace('[clear]', '')
        if not images:
            text = re.sub(r'!\[\w+\]\(~[\w./-]+\)', '', text)
        index = text.find('[more]')
        if index > 0:
            return self._render(text[0:index])
        raise BlogError('Need tag [more] in post "{0}"'.format(self.path))

    def _render(self, text):
        for res in self.resources:
            text = res.replace(text)
        return markdown(text, ['codehilite(noclasses=True)'])

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
        return "Post{{{0},{1}}}".format(self.meta, self.text)
