# -*- coding: utf-8 -*-
import os
from datetime import datetime
from itertools import chain
from shutil import copyfile

from jinja2 import Environment, FileSystemLoader

from isudo import conf
from isudo.utils import filejoin, TagCloud, Paginator, dash, url


class BaseWriter:
    name = 'BaseWriter, override'

    def __init__(self, draft=False):
        self.draft = draft
        self._jinja = Environment(loader=FileSystemLoader(conf.TEMPLATE_PATH), trim_blocks=True)
        self._jinja.filters['dash'] = dash
        self.default = conf.TEMPLATE_KWARGS
        self.default['url'] = url

    def render(self, path, template, **kwargs):
        default = self.default.copy()
        default.update(kwargs)
        self.mkdir(os.path.dirname(path))
        with open(filejoin(conf.DEPLOY_PATH, path), mode='w', encoding='utf8') as f:
            html = self._jinja.get_template(template).render(**default)
            f.write(html)

    def mkdir(self, url, *args):
        try:
            os.makedirs(filejoin(conf.DEPLOY_PATH, url, *args))
        except OSError:
            pass

    def build(self, posts):
        """
        Hook to add default kwargs for render

        :type posts: list of isudo.post.Post
        """
        self.default['today'] = datetime.now(tz=conf.TIME_ZONE)
        self.default['categories'] = sorted(set(chain(*list(i.meta.categories for i in posts))))
        # need to call in template with font_max, font_min
        tags = chain(*list(i.meta.tags for i in posts))
        self.default['tags'] = TagCloud(tags)
        # remove all drafts
        if not self.draft:
            posts = list(filter(lambda x: x.meta.draft is False, posts))
        self.write(posts)

    def write(self, posts):
        """
        Need to override, called on `build`

        :type posts: list of isudo.post.Post
        """
        raise NotImplementedError()


class IndexWriter(BaseWriter):
    name = 'Index writer'

    def write(self, posts):
        posts = filter(lambda x: x.meta.type == 'post', posts)
        pages = Paginator(posts, conf.POST_PER_PAGE).pages()

        first = next(pages)
        self.render('index.html', 'list.html',
            posts=first.entries,
            page=first
        )
        for page in pages:
            self.render('page/{0}/index.html'.format(page.current), 'list.html',
                posts=page.entries,
                page=page,
            )


class ErrorWriter(BaseWriter):
    name = 'Error writer'

    def write(self, posts):
        self.render('error.html', 'error.html')


class RobotsTxtWriter(BaseWriter):
    name = 'Robots.txt writer'

    def write(self, posts):
        path = filejoin(conf.DEPLOY_PATH, 'robots.txt')
        with open(path, mode='w', encoding='utf8') as f:
            f.write(conf.ROBOTS_TXT)


class ResourcesWriter(BaseWriter):
    name = 'Resources writer'

    def write(self, posts):
        """
        Make links to resources
        """
        for post in posts:
            if post.resources:
                folder = os.path.dirname(post.path)
                for res in post.resources:
                    r = os.path.abspath(filejoin(folder, res.body))
                    if os.path.exists(r):
                        self.mkdir(post.furl, os.path.dirname(res.body))
                        s = filejoin(conf.DEPLOY_PATH, post.furl, res.body)
                        if not os.path.lexists(s):
                            os.symlink(r, s)
                    else:
                        print('#! No resource found: {0}'.format(r))


class PostWriter(BaseWriter):
    name = 'Post writer'

    def write(self, posts):
        posts = filter(lambda x: x.meta.type == 'post', posts)
        for post in posts:
            self.render(filejoin(post.furl, 'index.html'), 'post.html',
                post=post,
            )


class TagsPageWriter(BaseWriter):
    name = 'Tags page writer'

    def write(self, posts):
        self.render(filejoin('tags', 'index.html'), 'tags.html')


class TagsWriter(BaseWriter):
    name = 'Tags writer'

    def write(self, posts):
        tags = set(chain(*map(lambda post: post.meta.tags, posts)))
        posts = {tag: list(filter(lambda post: tag in post.meta.tags, posts)) for tag in tags}

        for tag, items in posts.items():
            self.render('tag/{0}/index.html'.format(dash(tag)), 'titles.html',
                message='Tag "{0}"'.format(tag),
                posts=items,
            )


class CategoriesWriter(BaseWriter):
    name = 'Categories writer'

    def write(self, posts):
        tags = set(chain(*map(lambda post: post.meta.categories, posts)))
        posts = {tag: list(filter(lambda post: tag in post.meta.categories, posts)) for tag in tags}

        for tag, items in posts.items():
            self.render('category/{0}/index.html'.format(dash(tag)), 'titles.html',
                message='Category "{0}"'.format(tag),
                posts=items,
            )


class FeedWriter(BaseWriter):
    name = 'Feed writer'

    def write(self, posts):
        posts = filter(lambda x: x.meta.type == 'post', posts)
        posts = sorted(posts, key=lambda x: x.meta.time, reverse=True)

        self.render('feed/index.html', 'feed.xml',
            today=datetime.now(tz=conf.TIME_ZONE),
            posts=posts[:conf.POST_PER_PAGE],
        )