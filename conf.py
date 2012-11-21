# -*- coding: utf-8 -*-

from isudo.writer import IndexWriter, PostWriter, ResourcesWriter, TagsPageWriter, TagsWriter, CategoriesWriter

WRITES = [IndexWriter, ResourcesWriter, PostWriter, TagsPageWriter, TagsWriter, CategoriesWriter]

TEMPLATE_PATH = 'template'

TEMPLATE_KWARGS = {
    'title': 'Black&White’s Blog',
    'google_plus': '114553589811306443494',
    'canonical': 'http://isudo.ru/',
}

DEPLOY_PATH = 'deploy'

POST_PATH = 'posts'

POST_PER_PAGE = 4

TAG_CLOUD_FONT_COLOR = (168, 168, 196), (102, 102, 204)
