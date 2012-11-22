# -*- coding: utf-8 -*-
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

import baker

import conf
from isudo.main import StaticBlog


@baker.command
def build():
    """
    Build static site
    """
    blog = StaticBlog()
    blog.load()
    blog.copy_static()
    blog.build()


@baker.command
def server(port=8000):
    """
    Run test web server
    """
    if not os.path.exists(conf.DEPLOY_PATH):
        os.mkdir(conf.DEPLOY_PATH)
    os.chdir(conf.DEPLOY_PATH)

    httpd = HTTPServer(('127.0.0.1', port), SimpleHTTPRequestHandler)
    httpd.serve_forever()


@baker.command
def new(url):
    """
    Create new post file. Get url name of new post.
    """
    blog = StaticBlog()
    blog.create_post(url)


baker.run()