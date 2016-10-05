# -*- coding: utf-8 -*-

import static_classes


class CSSSelector:
    def __init__(self, name, file):
        i = 0
        for space in name:
            if space.isspace() is True:
                i += 1
            else:
                break
        j = len(name)
        for space in name[::-1]:
            if space.isspace() is True:
                j -= 1
            else:
                break

        self.name = name[i:j]
        self.files = list()
        self.lines = list()
        self.alone_selectors = list()
        self.parsed = False
        self.usage = False
        self.kind_usage = False

        self.add_file(file)

    def change_usage(self):
        self.usage = True

    def add_file(self, file):
        if file not in self.files:
            self.files.append(file)

    def add_selector(self, selector_to_add):
        if selector_to_add != '':
            self.alone_selectors.append(AloneCSSSelector(selector_to_add))

    def normalize_alone_selectors(self):
        tmp = list()

        for index_alone_selector in range(len(self.alone_selectors)):
            if self.alone_selectors[index_alone_selector].name == '':
                if self.alone_selectors[index_alone_selector-1].name not in ['+', '~', ',', '>']:
                    tmp.append(AloneCSSSelector('¿'))
            else:
                tmp.append(self.alone_selectors[index_alone_selector])

        self.alone_selectors = tmp

    def parsing_alone_selectors(self):
        if self.parsed is False:
            first_bad_letter = 0
            word = ''
            if self.is_alone() is True and self.name != '':
                self.alone_selectors.append(AloneCSSSelector(self.name))
            else:
                for i in range(len(self.name)):
                    if self.name[i] == '~' and self.name[i+1] == '=':
                        continue
                    if static_classes.Check.check_letter(self.name[i]) is True:
                        if static_classes.Check.check_word(word) is True:
                            if self.name[first_bad_letter:i].isspace() is False:
                                self.add_selector(self.name[first_bad_letter:i])
                        self.add_selector(self.name[i])
                        first_bad_letter = i+1
                        word = ''
                    else:
                        word += self.name[i]

                self.add_selector(self.name[first_bad_letter:])

            self.normalize_alone_selectors()
            self.parsed = True

    def is_alone(self):
        if self.name.find(' ') < 0 and self.name.find(',') < 0 and self.name.find('>') < 0\
                and self.name.find('~') < 0 and self.name.find('+') < 0:
            return True
        if self.name.find('~=') > 0 or self.name.find('^=') > 0 or self.name.find('$=') > 0\
                or self.name.find('*=') > 0:
            return False

        return False

    def add_line(self, file):
        index = 1
        with open(file.path, 'r+') as f:
            for line in f:
                if line.find(self.name) >= 0 and line.find('{') > 0:
                    self.lines.append((index, file))
                index += 1

    def __str__(self):
        return "CSSSelector: '" + self.name + "'"

    def __unicode__(self):
        return "CSSSelector: '" + self.name + "'"

    def __repr__(self):
        return "CSSSelector: '" + self.name + "'"


class AloneCSSSelector:
    def __init__(self, name):
        self.name = name.lstrip()
        self.pseudo = self.has_pseudo()
        self.alone_usage, self.alone_usage_for_file = False, False
        self.usage_files = list()

    def has_pseudo(self):
        return True if self.name.find(':') >= 0 else False

    def __str__(self):
        if self.alone_usage:
            return "AloneCSSSelector: '" + self.name + "' " + str(self.usage_files)
        else:
            return "AloneCSSSelector: '" + self.name + "'"

    def __unicode__(self):
        if self.alone_usage:
            return "AloneCSSSelector: '" + self.name + "' " + str(self.usage_files)
        else:
            return "AloneCSSSelector: '" + self.name + "'"

    def __repr__(self):
        if self.alone_usage and len(self.usage_files) > 0:
            return "AloneCSSSelector: '" + self.name + "' " + str(self.usage_files)
        else:
            return "AloneCSSSelector: '" + self.name + "'"
