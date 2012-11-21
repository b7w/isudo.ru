# -*- coding: utf-8 -*-
import unittest
import conf

from isudo.utils import urljoin, url

class UtilsTestCase(unittest.TestCase):
    def test_url_join(self):
        self.assertEqual(urljoin('foo', 'bar'), '/foo/bar/')
        self.assertEqual(urljoin('/foo', 'bar'), '/foo/bar/')
        self.assertEqual(urljoin('foo', '/bar'), '/foo/bar/')
        self.assertEqual(urljoin('foo', 'bar/'), '/foo/bar/')
        self.assertEqual(urljoin('foo', 'bar.img', last=False), '/foo/bar.img')

        self.assertEqual(urljoin(''), '/')
        self.assertEqual(urljoin('/'), '/')

        conf.DOMAIN_SUB_FOLDER = None
        self.assertEqual(url('foo', 'bar'), '/foo/bar/')
        self.assertEqual(url(''), '/')
        self.assertEqual(url('/'), '/')

        conf.DOMAIN_SUB_FOLDER = 'blog/'
        self.assertEqual(url('foo', 'bar'), '/blog/foo/bar/')
        self.assertEqual(url(''), '/blog/')
        self.assertEqual(url('/'), '/blog/')


if __name__ == '__main__':
    unittest.main()
