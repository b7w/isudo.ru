# -*- coding: utf-8 -*-
import os
from shutil import copytree, rmtree
from importlib import import_module

import conf
from isudo.reader import Reader
from isudo.utils import filejoin
from isudo.writer import IndexWriter, ResourcesWriter, PostWriter, TagsPageWriter, TagsWriter, CategoriesWriter


class StaticBlog:
    """
    Main class to generate static blog
    """

    def __init__(self):
        self.reader = Reader()
        self.posts = []
        self.writers = [IndexWriter, ResourcesWriter, PostWriter, TagsPageWriter, TagsWriter, CategoriesWriter]

    def get_backend(self):
        """
        Return file serving backend
        """
        #TODO: make support for string imports
        import_path = conf.VIEWER_SERVE['BACKEND']
        dot = import_path.rindex('.')
        module, class_name = import_path[:dot], import_path[dot + 1:]
        mod = import_module(module)
        return getattr(mod, class_name)

    def load(self):
        """
        Load all markdown files to memory
        """
        for root, folder, files in os.walk(conf.POST_PATH):
            for name in files:
                if name.endswith('.md'):
                    path = filejoin(root, name)
                    self.posts.append(self.reader.read(path))
        self.posts.sort(key=lambda x: x.meta.time, reverse=True)

    def build(self):
        """
        For all Writes classes run build, and generate blog in deploy folder
        """
        for cls in self.writers:
            writer = cls()
            print('# {0}'.format(writer.name))
            writer.build(self.posts)

    def copy_static(self, override=False):
        """
        Copy static directory from template to deploy folder.
        If `override` deploy will be removed first!
        """
        template = filejoin(conf.TEMPLATE_PATH, 'static')
        deploy = filejoin(conf.DEPLOY_PATH, 'static')
        if not os.path.exists(conf.DEPLOY_PATH):
            os.makedirs(conf.DEPLOY_PATH)
        if os.path.exists(deploy) and override:
            rmtree(deploy)
        if not os.path.exists(deploy):
            print('# Deploy static')
            copytree(template, deploy)

