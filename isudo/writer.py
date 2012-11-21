# -*- coding: utf-8 -*-
import os
from datetime import datetime
from itertools import chain
from shutil import copyfile

from jinja2 import Environment, FileSystemLoader

import conf
from isudo.utils import filejoin, TagCloud, Paginator, dash


class BaseWriter:
    name = 'BaseWriter, override'

    def __init__(self):
        self._jinja = Environment(loader=FileSystemLoader(conf.TEMPLATE_PATH), trim_blocks=True)
        self._jinja.filters['dash'] = dash
        self.default = conf.TEMPLATE_KWARGS

    def render(self, path, template, **kwargs):
        default = self.default.copy()
        default.update(kwargs)
        self.mkdir(os.path.dirname(path))
        with open(filejoin(conf.DEPLOY_PATH, path), mode='w', encoding='utf8') as f:
            html = self._jinja.get_template(template).render(**default)
            f.write(html)

    def mkdir(self, url):
        os.makedirs(filejoin(conf.DEPLOY_PATH, url), exist_ok=True)

    def build(self, posts):
        """
        Hook to add default kwargs for render

        :type posts: list of isudo.post.Post
        """
        self.default['today'] = datetime.now()
        self.default['categories'] = sorted(set(chain(*list(i.meta.categories for i in posts))))
        # need to call in template with font_max, font_min
        tags = chain(*list(i.meta.tags for i in posts))
        self.default['tags'] = TagCloud(tags)
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
        paging = Paginator(posts, conf.POST_PER_PAGE)

        first, *tail = paging.pages()
        self.render('index.html', 'list.html',
            posts=first.entries,
            page=first
        )
        for page in tail:
            self.render('page/{0}/index.html'.format(page.current), 'list.html',
                posts=page.entries,
                page=page,
            )


class ResourcesWriter(BaseWriter):
    name = 'Resources writer'

    def write(self, posts):
        for post in posts:
            if post.resources:
                self.mkdir(post.furl)
                folder = os.path.dirname(post.path)
                for res in post.resources:
                    r = filejoin(folder, res.body)
                    s = filejoin(conf.DEPLOY_PATH, post.furl, res.body)
                    if not os.path.exists(s):
                        copyfile(r, s)


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

    def _posts_per_tag(self, posts):
        """
        Get posts and return map with tag -> list of posts

        :type posts: list of isudo.post.Post
        :rtype: dict
        """
        tags = {}
        for post in posts:
            for tag in post.meta.tags:
                if tag in tags:
                    tags[tag].append(post)
                else:
                    tags[tag] = [post]
        return tags

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