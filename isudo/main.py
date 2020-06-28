# -*- coding: utf-8 -*-
import gzip
import os
import shutil
from datetime import datetime
from glob import glob
from importlib import import_module

from isudo import conf
from isudo.reader import Reader
from isudo.utils import filejoin


class StaticBlog:
    """
    Main class to generate static blog
    """

    def __init__(self, writers=None):
        self.reader = Reader()
        self.posts = []
        self.writers = writers or list(map(self._get_class, conf.WRITERS))

    def _get_class(self, package):
        """
        get string package name to class and return link for it
        """
        dot = package.rindex('.')
        module, class_name = package[:dot], package[dot + 1:]
        mod = import_module(module)
        return getattr(mod, class_name)

    def load(self, pattern=None):
        """
        Load all markdown files to memory
        """
        if pattern:
            for path in glob(filejoin(conf.POST_PATH, pattern + '.md')):
                self.posts.append(self.reader.read(path))
        else:
            for root, folder, files in os.walk(conf.POST_PATH):
                for name in files:
                    if name.endswith('.md'):
                        path = filejoin(root, name)
                        self.posts.append(self.reader.read(path))
        self.posts.sort(key=lambda x: x.meta.time, reverse=True)

    def build(self, draft=False):
        """
        For all Writes classes run build, and generate blog in deploy folder
        """
        for cls in self.writers:
            writer = cls(draft=draft)
            print('# {0}'.format(writer.name))
            writer.build(self.posts)

    def deploy(self, profile, region):
        bucket = conf.BLOG_URL.replace('http://', '').replace('https://', '')
        os.system('find -L deploy -name ".DS_Store" -exec rm -rf {} \;')
        cmd = 'aws s3 {} {} sync deploy s3://{}'
        p = '--profile {}'.format(profile) if region else ''
        r = '--region {}'.format(region) if region else ''
        os.system(cmd.format(p, r, bucket))

    def copy_static(self):
        """
        Make link to static directory
        """
        template = os.path.abspath(filejoin(conf.TEMPLATE_PATH, 'static'))
        deploy = filejoin(conf.DEPLOY_PATH, 'static')
        if not os.path.exists(conf.DEPLOY_PATH):
            os.makedirs(conf.DEPLOY_PATH)
        if not os.path.lexists(deploy):
            print('# Deploy static')
            shutil.copytree(template, deploy)

    def create_post(self, url):
        """
        Create new post file. Get url name of new post.

        :type url: str
        """
        time = datetime.now(tz=conf.TIME_ZONE)
        folder = conf.POST_PATH_STYLE.format(date=time)
        fname = '{date.year}-{date.month}-{date.day}-{name}.md'.format(date=time, name=url)
        path = filejoin(conf.POST_PATH, folder, fname)
        try:
            os.makedirs(filejoin(conf.POST_PATH, folder))
        except OSError:
            pass

        print('# creating new post..')
        print('# file: {0} '.format(path))
        with open(path, 'w', encoding='utf8') as f:
            f.write('# title: {0}\n'.format(url))
            f.write('# url: {0}\n'.format(url))
            f.write('# categories: []\n')
            f.write('# tags: []\n')
            f.write('# time: {0}\n'.format(time))
            f.write('\n![left](~logo.png)\nHello world\n')
            f.write('\n[more]\n\nend')

    def gzip_content(self):
        content = []
        for root, folder, files in os.walk(conf.DEPLOY_PATH):
            for name in files:
                if any(name.endswith(i) for i in ('.js', '.css', '.html')):
                    path = filejoin(root, name)
                    content.append(path)
        for fname in content:
            with open(fname, 'rb') as fin:
                with gzip.open(fname + '.gz', 'wb') as fout:
                    fout.writelines(fin)

    def clear(self):
        shutil.rmtree(conf.DEPLOY_PATH, ignore_errors=True)
