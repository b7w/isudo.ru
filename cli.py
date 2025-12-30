# -*- coding: utf-8 -*-
import os
from fire import Fire
from http.server import HTTPServer, SimpleHTTPRequestHandler
from time import time

from isudo import conf
from isudo.main import StaticBlog
from isudo.speller import YandexSpeller
from isudo.utils import BlogError


class Application:

    def build(self, pattern=None, draft=False):
        """
        Build static site
        """
        blog = StaticBlog()
        blog.load(pattern=pattern)
        blog.copy_static()
        blog.build(draft=draft)
        # blog.gzip_content()

    def deploy(self, profile=None, region=None, endpoint=None):
        """
        Run aws cmd to copy files to S3
        """
        blog = StaticBlog()
        blog.deploy(profile, region, endpoint)

    def server(self, port=8000):
        """
        Run test web server
        """
        if not os.path.exists(conf.DEPLOY_PATH):
            os.mkdir(conf.DEPLOY_PATH)
        os.chdir(conf.DEPLOY_PATH)

        httpd = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
        print('# server at http://127.0.0.1:{0}'.format(port))
        httpd.serve_forever()

    def clear(self):
        """
        Remove deploy directory
        """
        blog = StaticBlog()
        blog.clear()

    def vault(self):
        """
        Encrypt conf.py file for playbook.yml conf_py variable
        """
        os.system('ansible-vault encrypt conf.py --output conf.py.vault')

    def new(self, url):
        """
        Create new post file. Get url name of new post.
        """
        blog = StaticBlog()
        blog.create_post(url)

    def speller(self, url, fix=False):
        """
        Print mistakes for post, or if `fix` override it
        """
        speller = YandexSpeller(path=url)
        if fix:
            speller.fix()
        else:
            speller.check()


def main():
    try:
        t = time()
        Fire(Application)
        print('# done {0:.4f} second'.format(time() - t))
    except BlogError as e:
        print('#! Error:', e)


if __name__ == '__main__':
    main()
