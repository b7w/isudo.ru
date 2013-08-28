# -*- coding: utf-8 -*-
import os

import requests

from isudo import conf
from isudo.utils import BlogError


class Options(object):
    IGNORE_UPPERCASE = 1
    IGNORE_DIGITS = 2
    IGNORE_URLS = 4
    FIND_REPEAT_WORDS = 8
    IGNORE_LATIN = 16
    NO_SUGGEST = 32
    FLAG_LATIN = 128
    BY_WORDS = 256
    IGNORE_CAPITALIZATION = 512

    @staticmethod
    def default():
        val = Options.IGNORE_UPPERCASE
        val += Options.IGNORE_DIGITS
        val += Options.IGNORE_URLS
        val += Options.FIND_REPEAT_WORDS
        return val


class YandexSpeller(object):
    def __init__(self, text=None, path=None, lang=None, options=None, text_format=None):
        """
        :param lang: default "ru,en", possible values - ru | uk | en
        :param options: sum of options
        :param text_format: plain | html
        """
        self.text = text
        self.path = os.path.join(conf.POST_PATH, path)
        if path:
            with open(self.path, encoding='utf8') as f:
                self.text = f.read()
        self.lang = lang
        self.options = Options.default() if options is None else options
        self.text_format = text_format

    def load(self):
        params = dict(text=self.text)
        if self.lang:
            params['lang'] = self.lang
        if self.text_format:
            params['format'] = self.text_format
        if self.options is not None:
            params['options'] = self.options
        r = requests.post('http://speller.yandex.net/services/spellservice.json/checkText', data=params)
        if r.status_code == 200:
            return r.json()
        raise BlogError('Error in requests, code {0}'.format(r.status_code))

    def format(self):
        report = self.load()
        out = []
        for item in report:
            word = item['word']
            hints = item['s']
            position = item['pos']
            length = item['len']
            left = position - 20 if position > 20 else 0
            right = position + length + 20 if position + length + len(self.text) > 20 else len(self.text)
            text = self.text[left:right].replace('\n', ' ')
            text = text.replace(word, '*' + word + '*')
            out.append((text, hints,))
        return out

    def check(self):
        report = self.format()
        for text, hints in report:
            print(text)
            print(', '.join(hints) if hints else 'No hints')
            print()

        print('Found {0} mistakes'.format(len(report)))

    def fix(self):
        report = self.load()
        count = 0
        correction = 0
        for item in report:
            word = item['word']
            length = item['len']
            if len(item['s']) == 1:
                count += 1
                hint = item['s'][0]
                position = item['pos'] + correction
                self.text = self.text[:position] + hint + self.text[position + length:]
                # after replace pos change for other word, calculate it
                correction += len(hint) - length
                print('fix "{0}" to "{1}"'.format(word, hint))
            else:
                print('Can fix "{0}"'.format(word))
        with open(self.path, mode='w', encoding='utf8') as f:
            f.write(self.text)

        print('Found {0} mistakes'.format(len(report)))
        print('Fix {0} mistakes'.format(count))