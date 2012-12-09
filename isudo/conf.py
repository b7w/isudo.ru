# -*- coding: utf-8 -*-
import conf
from pytz import timezone


# Classes that generate something
WRITERS = getattr(conf, 'WRITERS',
    [
        'isudo.writer.IndexWriter',
        'isudo.writer.ResourcesWriter',
        'isudo.writer.PostWriter',
        'isudo.writer.TagsPageWriter',
        'isudo.writer.TagsWriter',
        'isudo.writer.CategoriesWriter',
        'isudo.writer.FeedWriter',
    ]
)

BLOG_URL = getattr(conf, 'BLOG_URL')

BLOG_TITLE = getattr(conf, 'BLOG_TITLE', 'BLOG TITLE')

BLOG_DESCRIPTION = getattr(conf, 'BLOG_DESCRIPTION', '')

BLOG_KEYWORDS = getattr(conf, 'BLOG_KEYWORDS', '')

GOOGLE_PLUS = getattr(conf, 'GOOGLE_PLUS', None)

# Path where html template exists
TEMPLATE_PATH = getattr(conf, 'TEMPLATE_PATH', 'template')

# Return TzInfo object, default 'UTC'
TIME_ZONE = timezone(getattr(conf, 'TIME_ZONE', 'UTC'))

# If you want something like http://isudo.ru/blog/
DOMAIN_SUB_FOLDER = getattr(conf, 'DOMAIN_SUB_FOLDER', '')

TEMPLATE_KWARGS = getattr(conf, 'TEMPLATE_KWARGS',
    {
        'BLOG_URL': BLOG_URL,
        'BLOG_TITLE': BLOG_TITLE,
        'BLOG_DESCRIPTION': BLOG_DESCRIPTION,
        'BLOG_KEYWORDS': BLOG_KEYWORDS,
        'GOOGLE_PLUS': GOOGLE_PLUS,
    }
)

# Path where to put generated files
DEPLOY_PATH = getattr(conf, 'DEPLOY_PATH', 'deploy')

# Path where to get posts
POST_PATH = getattr(conf, 'POST_PATH', 'posts')

# Default url style, for new posts.
# To override use absolute utl in post meta info.
# Use date variable of datetime type, `{date.year}`.
POST_PATH_STYLE = getattr(conf, 'POST_PATH_STYLE', '/{date.year}/{date.month:02d}')

# Main POSTS
POST_PER_PAGE = getattr(conf, 'POST_PER_PAGE', 8)

# Two colors to make nice transition from most used tags to less used.
# Type (r,g,b),(r,g,b)
TAG_CLOUD_FONT_COLOR = getattr(conf, 'TAG_CLOUD_FONT_COLOR',
    ((168, 168, 196), (102, 102, 204))
)
