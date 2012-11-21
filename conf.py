# -*- coding: utf-8 -*-

# Classes that generate something
WRITERS = [
    'isudo.writer.IndexWriter',
    'isudo.writer.ResourcesWriter',
    'isudo.writer.PostWriter',
    'isudo.writer.TagsPageWriter',
    'isudo.writer.TagsWriter',
    'isudo.writer.CategoriesWriter',
]

# Path where html template exists
TEMPLATE_PATH = 'template'

# If you want something like http://isudo.ru/blog/
DOMAIN_SUB_FOLDER = ''

TEMPLATE_KWARGS = {
    'title': 'Black&White’s Blog',
    'google_plus': '114553589811306443494',
    'canonical': 'http://isudo.ru/',
}

# Path where to put generated files
DEPLOY_PATH = 'deploy'

# Path where to get posts
POST_PATH = 'posts'

# Default url style, for new posts.
# To override use absolute utl in post meta info.
# Use date variable of datetime type, `{date.year}`.
POST_PATH_STYLE = '/{date.year}/{date.month}'

# Main POSTS
POST_PER_PAGE = 4

# Two colors to make nice transition from most used tags to less used.
# Type (r,g,b),(r,g,b)
TAG_CLOUD_FONT_COLOR = (168, 168, 196), (102, 102, 204)
