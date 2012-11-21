# -*- coding: utf-8 -*-
import os
from shutil import copytree, rmtree

import conf
from isudo.reader import Reader
from isudo.utils import filejoin


class StaticBlog:
    """
    Main class to generate static blog
    """

    def __init__(self, writers=None):
        self.reader = Reader()
        self.posts = []
        self.writers = writers or conf.WRITES

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

