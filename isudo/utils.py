# -*- coding: utf-8 -*-
from collections import namedtuple
import os
from math import ceil
from itertools import groupby

import conf


def urljoin(*args, last=True):
    """
    Make absolute url with slash on end if `last`
    """
    url = '/' + '/'.join(map(str, args))
    if last:
        url += '/'
    return url.replace('//', '/')


def filejoin(*args):
    """
    Make relative file path
    """
    return os.path.join(*map(str, args))


def dash(name):
    """
    Get string and make better url from it

    :type name: str
    :rtype: str
    """
    return name.replace(' ', '-').lower()


class TagCloud():
    """
    Help to make tag cloud. All tags stored in `all` field.
    To get cloud list, call `cloud`.
    """
    TagValue = namedtuple('TagCloudValue', ('tag', 'font', 'color'))

    def __init__(self, tags):
        self.all = list(tags)
        self.color_min, self.color_max = conf.TAG_CLOUD_FONT_COLOR

    def cloud(self, font_min, font_max, size=None):
        """
        Return [TagValue(tag, font size, color),...]
        Color is in format of 'rgb(x,y,z)' List is sorted.

        :type font_max: int
        :type font_max: int
        :type font_max: int
        :rtype: list of (str, int, str)
        """
        if not self.all:
            return []

        weight = self._weight()
        lens = [l for k, l in weight]
        count = max(lens) - min(lens)

        font = self._font_eval(count, font_min, font_max)
        color = self._color_eval(count, self.color_min, self.color_max)
        result = []
        for value, l in weight:
            result.append(self.TagValue(value, font(l), color(l)))
        if size:
            return result[:size]
        return result

    def _font_eval(self, count, min, max):
        delta = (max - min) / count
        font = lambda x: min + delta * (x - 1)
        return font

    def _color_eval(self, count, min, max):
        delta0 = (max[0] - min[0]) / count
        delta1 = (max[1] - min[1]) / count
        delta2 = (max[2] - min[2]) / count

        def color(x):
            v0 = min[0] + delta0 * (x - 1)
            v1 = min[1] + delta1 * (x - 1)
            v2 = min[2] + delta2 * (x - 1)
            return 'rgb({0},{1},{2})'.format(round(v0), round(v1), round(v2))

        return color

    def _weight(self):
        """
        return [(tag, len),..]
        :rtype: list of (str, int)
        """
        weight = [(k, len(list(v))) for k, v in groupby(sorted(self.all))]
        return sorted(weight, key=lambda x: x[1], reverse=True)


class Page:
    """
    Simple class that store entries on this page,
    page number, next and previous pages.
    """

    def __init__(self, paginator, entries, current):
        self.paginator = paginator
        self.entries = entries
        self.current = current
        self.range_size = 4

    def count(self):
        return self.paginator.count()

    def has_next(self):
        return self.current < self.count()

    def next(self):
        return self.current + 1

    def next_range(self):
        forward = self.current + self.range_size
        end = forward if forward < self.count() else self.count()
        return range(self.next(), end + 1)

    def has_previous(self):
        return 1 < self.current

    def previous_range(self):
        back = self.current - self.range_size
        start = back if back > 0 else 1
        return range(start, self.current)

    def previous(self):
        return self.current - 1

    def __repr__(self):
        return 'Page{{{0},{1}}}'.format(self.current, self.entries)


class Paginator:
    """
    Factory to produce Page's
    """

    def __init__(self, entries, per_page):
        self.entries = list(entries)
        self.per_page = per_page
        self.size = len(self.entries)

    def pages(self):
        for i in range(0, self.size, self.per_page):
            current = round(i / self.per_page) + 1
            entries = self.entries[i:i + self.per_page]
            yield Page(self, entries, current)

    def count(self):
        return ceil(self.size / self.per_page)