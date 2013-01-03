# -*- coding: utf-8 -*-
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from time import time

import baker

from isudo import conf
from isudo.main import StaticBlog
from isudo.utils import BlogError


@baker.command
def build(pattern=None, draft=False):
    """
    Build static site
    """
    blog = StaticBlog()
    blog.load(pattern=pattern)
    blog.copy_static()
    blog.build(draft=draft)


@baker.command
def server(port=8000):
    """
    Run test web server
    """
    if not os.path.exists(conf.DEPLOY_PATH):
        os.mkdir(conf.DEPLOY_PATH)
    os.chdir(conf.DEPLOY_PATH)

    httpd = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print('# server at http://127.0.0.1:{0}'.format(port))
    httpd.serve_forever()


@baker.command
def clear():
    """
    Remove deploy directory
    """
    blog = StaticBlog()
    blog.clear()


@baker.command
def hg(arg):
    """
    Some tools to work with mercurial.

    hg up - check, update, full rebuild.
    """
    blog = StaticBlog()
    if arg == 'up' or arg == 'update':
        check = os.system('hg incoming --quiet')
        if check == 0:
            print('# Found changes, loading')
            os.system('hg pull -u --quiet')
            blog.clear()
            blog.load()
            blog.copy_static()
            blog.build()
        else:
            print('# No changes')


@baker.command
def new(url):
    """
    Create new post file. Get url name of new post.
    """
    blog = StaticBlog()
    blog.create_post(url)


try:
    t = time()
    baker.run()
    print('# done {0:.4f} second'.format(time() - t))
except BlogError as e:
    print('#! Error:', e)