# -*- coding: utf-8 -*-
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from time import time

import baker

from isudo import conf
from isudo.main import StaticBlog
from isudo.speller import YandexSpeller
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
    # blog.gzip_content()


@baker.command
def deploy(profile=None, region=None, endpoint=None):
    """
    Run aws cmd to copy files to S3
    """
    blog = StaticBlog()
    blog.deploy(profile, region, endpoint)


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
def vault():
    """
    Encrypt conf.py file for playbook.yml conf_py variable
    """
    os.system('ansible-vault encrypt conf.py --output conf.py.vault')


@baker.command
def new(url):
    """
    Create new post file. Get url name of new post.
    """
    blog = StaticBlog()
    blog.create_post(url)


@baker.command
def speller(url, fix=False):
    """
    Print mistakes for post, or if `fix` override it
    """
    speller = YandexSpeller(path=url)
    if fix:
        speller.fix()
    else:
        speller.check()


try:
    t = time()
    baker.run()
    print('# done {0:.4f} second'.format(time() - t))
except BlogError as e:
    print('#! Error:', e)
