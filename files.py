# -*- coding: utf-8 -*-

import re


class MyFile:
    def __init__(self, path):
        self.path = path
        self.name = path.split('/')[-1]
        self.extention = path.split('/')[-1].split('.')[-1]

    def __str__(self):
        return 'File ' + self.name

    def __unicode__(self):
        return 'File ' + self.name

    def __repr__(self):
        return 'File ' + self.name


class CSSFile(MyFile):
    def __init__(self, path, minified):
        self.minified_version = minified
        super().__init__(path)

    def __str__(self):
        return 'CSSFile ' + self.name

    def __unicode__(self):
        return 'CSSFile ' + self.name

    def __repr__(self):
        return 'CSSFile ' + self.name


class HTMLFile(MyFile):
    def __init__(self, path):
        with open(path, 'r+') as f:
            self.html = f.read().replace('\t', '')
        self.opened_and_closed_tags_check = False
        super().__init__(path)

    def check_tags(self, html_file_as_string):
        optional_tags = ['html', 'head', 'body', 'li', 'dt',
                         'dd', 'p', 'colgroup', 'thead', 'tbody',
                         'tfoot', 'tr', 'th', 'td', 'rt', 'rp',
                         'optgroup', 'option', 'area', 'base', 'br',
                         'col', 'command', 'embed', 'hr', 'img', 'input',
                         'keygen', 'link', 'meta', 'param', 'source',
                         'track', 'wbr', 'ins', 'del']
        optional_tags = frozenset(optional_tags)
        opened_tags_count, closed_tags_count = 0, 0

        for find in re.findall(u"<.*?>", html_file_as_string):
            if find.find('<!') == 0:
                    continue
            else:
                if find.count('</') == 1:
                    if find.split(' ')[0][2:].replace('>', '') not in optional_tags:
                        closed_tags_count += 1
                else:
                    if find.split(' ')[0][1:].replace('>', '') not in optional_tags:
                        opened_tags_count += 1

        if opened_tags_count == closed_tags_count:
            self.opened_and_closed_tags_check = True

    def __str__(self):
        return 'HTMLFile ' + self.name

    def __unicode__(self):
        return 'HTMLFile ' + self.name

    def __repr__(self):
        return 'HTMLFile ' + self.name
