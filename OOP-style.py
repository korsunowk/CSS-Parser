import sys
import os
import re


class CSSRectifierFinderError(Exception):
    pass


class Check:
    @staticmethod
    def check_letter(letter):
        if letter.isspace() is True or letter == ',' or letter == '>' or letter == '~' or letter == '+':
            return True
        return False

    @staticmethod
    def check_word(word):
        for i in word:
            if Check.check_letter(i) is True:
                return False
        return True

    @staticmethod
    def parsing_problem_selector(problem_selector, kind=False):
        new_selector2 = list()
        if kind is True:
            new_selector2.append(problem_selector[0])
            new_selector2.append(problem_selector[1][:problem_selector[1].find('=') - 1])
            new_selector2.append(problem_selector[1][problem_selector[1].find('=') - 1] + '=')
            new_selector2.append(problem_selector[1][problem_selector[1].find('=') + 1:])
        else:
            new_selector2.append(problem_selector[0])
            new_selector2.append(problem_selector[1][:problem_selector[1].find('=')])
            new_selector2.append('=')
            new_selector2.append(problem_selector[1][problem_selector[1].find('=')+1:])

        return new_selector2


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
        super().__init__(path)

    def __str__(self):
        return 'HTMLFile ' + self.name

    def __unicode__(self):
        return 'HTMLFile ' + self.name

    def __repr__(self):
        return 'HTMLFile ' + self.name


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

        self.add_file(file)

    def change_usage(self):
        self.usage = True

    def add_file(self, file):
        self.files.append(file)

    def add_selector(self, selector_to_add):
        self.alone_selectors.append(AloneCSSSelector(selector_to_add))

    def normalize_alone_selectors(self):
        tmp = list()

        for index_alone_selector in range(len(self.alone_selectors)):
            if index_alone_selector > 0:
                if Check.check_word(self.alone_selectors[index_alone_selector-1].name) is True and \
                                Check.check_word(self.alone_selectors[index_alone_selector].name) is True:
                    tmp.append(AloneCSSSelector('¿'))
            tmp.append(self.alone_selectors[index_alone_selector])

        self.alone_selectors = tmp

    def parsing_alone_selectors(self):
        if self.parsed is False:
            first_bad_letter = 0
            word = ''
            if self.is_alone() is True:
                self.alone_selectors.append(AloneCSSSelector(self.name))
            else:
                for i in range(len(self.name)):
                    if Check.check_letter(self.name[i]) is True:
                        if Check.check_word(word[:-1]) is True:
                            if self.name[first_bad_letter:i].isspace() is False:
                                self.add_selector(self.name[first_bad_letter:i])
                        first_bad_letter = i
                        word = ''
                    else:
                        word += self.name[i]

                self.add_selector(self.name[first_bad_letter:])
            self.normalize_alone_selectors()
            self.parsed = True

    def is_alone(self):
        if self.name.find(' ') < 0 and self.name.find(',') < 0 and self.name.find('<') < 0\
                and self.name.find('~') < 0:
            return True
        if self.name.find('~=') > 0 or self.name.find('^=') > 0 or self.name.find('$=') > 0\
                or self.name.find('*=') > 0:
            return True

        return False

    def add_line(self, file):
        index = 0

        with open(file.path, 'r+') as f:
            for line in f:
                if line.find(self.name) >= 0 and line.find('{') > 0:
                    self.lines.append((index+1, file))
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

    def has_pseudo(self):
        if self.name.find(':') > 0:
            return True
        return False

    def __str__(self):
        return "AloneCSSSelector: '" + self.name + "'"

    def __unicode__(self):
        return "AloneCSSSelector: '" + self.name + "'"

    def __repr__(self):
        return "AloneCSSSelector: '" + self.name + "'"


class CSSRectifier:
    def __init__(self):
        self.ignore = list()
        self.files = list()
        self.css_files, self.html_files = list(), list()
        self.css_selectors = list()

    def get_css_files(self):
        files = list()
        for file in self.files:
            if file.extention == 'css':
                files.append(file)
        return files

    def get_html_files(self):
        files = list()
        for file in self.files:
            if file.extention == 'html' or file.extention == 'htm':
                files.append(file)
        return files

    def add_selector(self, _selector, css_file):
        if len(self.css_selectors) > 0:
            tmp = list()
            for i in self.css_selectors:
                tmp.append(i.name)
            if _selector not in tmp:
                new_selector = CSSSelector(_selector, css_file)
                new_selector.add_line(css_file)
                self.css_selectors.append(new_selector)
            else:
                i = tmp.index(_selector)
                self.css_selectors[i].add_file(css_file)
                self.css_selectors[i].add_line(css_file)
        else:
            self.css_selectors.append(CSSSelector(_selector, css_file))

    def load_ignore_files(self):
        try:
            with open('files to ignore.txt', 'r+') as f:
                for line in f:
                    self.ignore.append(line.rstrip())
        except FileNotFoundError:
            with open('files to ignore.txt', 'w') as f:
                for line in ['bootstrap.css', 'bootstrap.min.css', 'bootstrap-responsive.css',
                             'bootstrap-responsive.min.css', 'font-awesome.css']:
                    f.write(line+'\n')
            self.load_ignore_files()

    def do_rectifier(self, home_directory, start=True, iteration=2, home='', old_dir=-1):
        if start:
            home = home_directory.replace("/" + home_directory.split('/')[-1], "")
            self.load_ignore_files()
            return self.do_rectifier(
                os.chdir(home_directory),
                start=False,
                home=home,
            )
        else:
            if home_directory != home:
                directory = os.listdir(os.getcwd())
                for item in directory:
                    if directory.index(item) <= old_dir:
                        continue
                    if os.path.isfile(os.getcwd() + '/' + item) and item[-3:] == 'css':
                        if item not in self.ignore:
                            # print(item)
                            self.files.append(MyFile(path=(os.getcwd() + '/' + item)))
                        # else:
                        #     print('IGNORE: ' + item)

                    elif os.path.isfile(os.getcwd() + '/' + item) and (item[-4:] == 'html' or item[-3:] == 'htm'):
                        self.files.append(MyFile(path=(os.getcwd() + '/' + item)))

                    if os.path.isdir(os.getcwd() + '/' + item) and item != 'venv' and item != '.git':
                        os.chdir(os.getcwd() + '/' + item)
                        iteration += 2

                        return self.do_rectifier(
                            os.getcwd(),
                            start=False,
                            iteration=iteration,
                            home=home,
                        )
                os.chdir('../')

                if home_directory is None:
                    return self.css_minification()
                else:
                    old_dir = os.listdir(os.getcwd()).index(home_directory.split('/')[-1])
                    iteration -= 2

                return self.do_rectifier(
                    os.getcwd(),
                    start=False,
                    iteration=iteration,
                    home=home,
                    old_dir=old_dir,
                )

            else:
                return self.css_minification()

    def css_minification(self):
        for file in self.get_css_files():
            with open(file.path, 'r+') as f:
                css_file = f.read()
                css_file = css_file.replace("\t", "").replace("\n", "")

            for match in re.finditer(u"/*[^}]+\*/", css_file):
                css_file = css_file.replace(match.group(), "")

            space, media = False, False
            final_css = str()
            for i in range(len(css_file)):
                if css_file[i].isspace() is True and css_file[i + 1] == '{' or \
                        css_file[i].isspace() is True and css_file[i - 1] == ':':
                    continue
                elif css_file[i] == '@' and css_file[i:i + 6] == '@media':
                    media = True
                elif css_file[i] == '{' and media is False:
                    space = True
                elif css_file[i] == '}':
                    space = False

                if space is True:
                    final_css += css_file[i].rstrip()
                else:
                    final_css += css_file[i]

            self.css_files.append(CSSFile(file.path, final_css))
        self.css_separation()

    def css_separation(self):
        for css_file in self.css_files:
            only_classes = []
            minified_version = css_file.minified_version
            for match in re.finditer(u"{[^}]+}", minified_version):
                if match.group().count('{') > 1:
                    only_classes.append(str(match.group()).split('{')[1])
                    minified_version = minified_version.replace(match.group(), "¿")
                else:
                    minified_version = minified_version.replace(match.group(), '¿')

            minified_version = only_classes + minified_version.replace("}", '')[:-1].split('¿')
            media_count = [i for i in minified_version if i.find('@') >= 0]

            for i in media_count:
                minified_version.pop(minified_version.index(i))

            clean_css_classes = []
            for i in minified_version:
                if i not in clean_css_classes:
                    clean_css_classes.append(i)

            for clean_selector in clean_css_classes:
                self.add_selector(clean_selector, css_file)

            for clean_selector in self.css_selectors:
                clean_selector.parsing_alone_selectors()

        self.find_selectors_in_html()

    def create_html_files(self):
        self.html_files = [HTMLFile(file.path) for file in self.get_html_files()]
        return self.html_files

    def find_selectors_in_html(self):
        for html_file in self.create_html_files():
            with open(html_file.path) as html:
                html = html.read().replace('\t', '').replace('\n', '')
                html = html.replace(re.search(u'<head>(.+?)</head>', html).group(), '')
                for combo_selector in self.css_selectors:
                    self.find_combo_selector_in_html(html, combo_selector)

    @staticmethod
    def find_combo_selector_in_html(html_file_as_string, combo_selector):
        try:
            if len(combo_selector.alone_selectors) == 1:
                alone_selector = combo_selector.alone_selectors[0]
                if alone_selector.name != '*':
                    if alone_selector.pseudo is False:
                        if alone_selector.name[0] != '.' and alone_selector.name[0] != '#':
                            if alone_selector.name.find('[') == -1:
                                if html_file_as_string.find('<'+alone_selector.name) > 0:
                                    combo_selector.usage = True
                                else:
                                    combo_selector.usage = False
                            else:
                                new_selector = alone_selector.name.replace(']', '').split('[')
                                if new_selector[1].find('=') > 0:
                                    if new_selector[1][new_selector[1].find('=')-1] in ['~', '*', '$', '^']:
                                        problem_selector = Check.parsing_problem_selector(new_selector, True)
                                        str_to_search = u'<%s[^>]+>' % (problem_selector[0])
                                        for find in re.findall(str_to_search, html_file_as_string):
                                            if problem_selector[2] == '~=':
                                                str_to_search = u'%s="[^"]+"' \
                                                                % (problem_selector[1])
                                                clean_find = re.search(str_to_search, find).group()[
                                                    len(problem_selector[1] + '="'):-1
                                                ]
                                                for for_tilda in clean_find.split(' '):
                                                    if for_tilda == problem_selector[3][1:-1]:
                                                        combo_selector.usage = True
                                                        break
                                            elif problem_selector[2] == '*=':
                                                if problem_selector[1][-1] != '-':
                                                    if find.find(problem_selector[1]) > 0 \
                                                            and find.find(problem_selector[3][1:-1]) > 0:
                                                        combo_selector.usage = True
                                                        break
                                                else:
                                                    if find.find(problem_selector[3][1:-1]) > 0 \
                                                            and find.find(problem_selector[1]) > 0:
                                                        combo_selector.usage = True
                                                        break

                                            elif problem_selector[2] == '$=':
                                                str_to_search = u'%s="[^"]+"' \
                                                                % (problem_selector[1])
                                                clean_find = re.search(str_to_search, find).group()[
                                                   len(problem_selector[1] + '="'):-1]

                                                if clean_find.endswith(problem_selector[3][1:-1]) is True:
                                                    combo_selector.usage = True
                                                    break
                                            elif problem_selector[2] == '^=':
                                                str_to_search = u'%s="[^"]+"' \
                                                                % (problem_selector[1])
                                                if re.search(str_to_search, find).group()[
                                                        len(problem_selector[1]+'="'):].find(
                                                        problem_selector[3][1:-1]) == 0:
                                                    combo_selector.usage = True
                                                    break
                                    else:
                                        problem_selector = Check.parsing_problem_selector(new_selector)
                                        str_to_search = u'<%s[^>]+>' % (problem_selector[0])

                                        for find in re.findall(str_to_search, html_file_as_string):
                                            if find.find(problem_selector[1]+problem_selector[2]) > 0 \
                                                    and find.find(problem_selector[3]) > 0:
                                                combo_selector.usage = True
                                                break
                                else:

                                    new_selector = alone_selector.name.replace(']', '').split('[')
                                    str_to_search = u'<%s[^>]+>' % (new_selector[0])

                                    for find in re.findall(str_to_search, html_file_as_string):
                                        if find.find(new_selector[1]) > 0:
                                            combo_selector.usage = True
                                            break
                        else:
                            if alone_selector.name[0] == '.':
                                for find in re.findall(u'class="[^"]+"', html_file_as_string):
                                    for one_class in find.replace('class=', '')[1:-1].split(' '):
                                        if one_class == alone_selector.name[1:]:
                                            combo_selector.usage = True
                                            break
                            elif alone_selector.name[0] == '#':
                                for find in re.findall(u'id="[^"]+"', html_file_as_string):
                                    for one_class in find.replace('id=', '')[1:-1].split(' '):
                                        if one_class == alone_selector.name[1:]:
                                            combo_selector.usage = True
                                            break
                    else:
                        # has pseudo
                        pass
                else:
                    combo_selector.usage = True
            else:
                # multiple classes
                pass

        except Exception:
            raise CSSRectifierFinderError('Something went wrong with find.')
        return True

if __name__ == '__main__':
    sys.setrecursionlimit(10000)

    project_dir = '/home/incode7/PycharmProjects/incodeParsing'

    test_rectifier = CSSRectifier()
    test_rectifier.do_rectifier(project_dir)

    for selector in test_rectifier.css_selectors:
        print(str(selector) + ' ' + str(selector.usage))
