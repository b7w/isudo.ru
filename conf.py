# -*- coding: utf-8 -*-

# Classes that generate something
WRITERS = [
    'IndexWriter',
    'ResourcesWriter',
    'PostWriter',
    'TagsPageWriter',
    'TagsWriter',
    'CategoriesWriter',
]

# Path where html template exists
TEMPLATE_PATH = 'template'

# If you want something like http://isudo.ru/blog/
DOMAIN_SUB_FOLDER = 'blog'

TEMPLATE_KWARGS = {
    'title': 'Black&White’s Blog',
    'google_plus': '114553589811306443494',
    'canonical': 'http://isudo.ru/',
}

# Path where to put generated files
DEPLOY_PATH = 'deploy'

# Path where to get posts
POST_PATH = 'posts'

# Main POSTS
POST_PER_PAGE = 4

# Two colors to make nice transition from most used tags to less used.
# Type (r,g,b),(r,g,b)
TAG_CLOUD_FONT_COLOR = (168, 168, 196), (102, 102, 204)
