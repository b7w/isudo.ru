# -*- coding: utf-8 -*-
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

import baker

import conf
from isudo.main import StaticBlog

@baker.command
def build():
    blog = StaticBlog()
    blog.load()
    blog.copy_static()
    blog.build()


@baker.command
def server():
    if not os.path.exists(conf.DEPLOY_PATH):
        os.mkdir(conf.DEPLOY_PATH)
    os.chdir(conf.DEPLOY_PATH)

    httpd = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()

baker.run()