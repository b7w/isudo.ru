# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest.mock import Mock
from isudo.reader import Resource


class ResourceTestCase(TestCase):
    def setUp(self):
        self.post = Mock()
        self.post.url = '/2013/01/'

    def test_find_RE(self):
        self.post.text = 'Foo ![title](~resource.png) bar'
        resources = Resource.RE.findall(self.post.text)
        self.assertEqual(len(resources), 1)

        self.post.post = 'Foo [~resource.png] bar'
        resources = Resource.RE2.findall(self.post.post)
        self.assertEqual(len(resources), 1)

    def test_findall(self):
        self.post.text = 'Foo ![title](~resource.png) bar [~resource2.png] foo [title2](~resource3.ln)'
        resources = Resource.findall(self.post)
        self.assertEqual(len(resources), 3)
        macros = sorted(map(lambda x: x.macros, resources))
        macros2 = sorted(['(~resource.png)', '[~resource2.png]', '(~resource3.ln)'])
        self.assertListEqual(macros, macros2)

    def test_replace(self):
        res = Resource("(~resource.png)", self.post, Resource.RE)
        self.assertEqual(res.link, 'resource.png')
        self.assertEqual(res.render(), '(/2013/01/resource.png)')
        self.assertEqual(res.replace('Foo (~resource.png) bar'), 'Foo (/2013/01/resource.png) bar')

        res = Resource("[~resource.png]", self.post, Resource.RE2)
        self.assertEqual(res.link, 'resource.png')
        self.assertEqual(res.render(), '/2013/01/resource.png')
        self.assertEqual(res.replace('Foo [~resource.png] bar'), 'Foo /2013/01/resource.png bar')