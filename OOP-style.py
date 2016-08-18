import sys
import os
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
    pass


class CSSSelector:
    def __init__(self, name, file):
        self.name = name
        self.files = list()
        self.usage = False

        self.add_file(file)

    def change_usage(self):
        self.usage = True

    def add_file(self, file):
        self.files.append(file)

    def __str__(self):
        return "'" + self.name + "'"

    def __unicode__(self):
        return "'" + self.name + "'"

    def __repr__(self):
        return "'" + self.name + "'"


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

    def add_selector(self, selector, css_file):
        if len(self.css_selectors) > 0:
            tmp = list()
            for i in self.css_selectors:
                tmp.append(i.name)
            if selector not in tmp:
                self.css_selectors.append(CSSSelector(selector, css_file))
            else:
                i = tmp.index(selector)
                self.css_selectors[i].add_file(css_file)
        else:
            self.css_selectors.append(CSSSelector(selector, css_file))

    def load_ignore_files(self):
        try:
            with open('files to ignore.txt', 'r+') as f:
                for line in f:
                    self.ignore.append(line.rstrip())
        except FileNotFoundError:
            with open('files to ignore.txt', 'w+') as f:
                for line in ['bootstrap.css', 'bootstrap.min.css', 'bootstrap-responsive.css',
                             'bootstrap-responsive.min.css', 'font-awesome.css]']:
                    f.write(line)
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
                            # print('IGNORE: ' + item)

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
                css_file = css_file.replace("\t", "").replace("\n", "")  # Удаляем табуляцию и переход на новую строку.

            for match in re.finditer(u"/*[^}]+\*/", css_file):
                css_file = css_file.replace(match.group(), "")  # Удаляем комментарии.

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
            tmp_classes = []
            for i in minified_version:
                if i.find(':') >= 0:
                    tmp = i
                    for match in re.finditer(u":[a-z]+", i):
                        tmp = tmp.replace(match.group(), '')
                    minified_version.append(tmp)
                    tmp_classes.append(i)
            for i in tmp_classes:
                minified_version.pop(minified_version.index(i))

            clean_css_classes = []
            for i in minified_version:
                if i not in clean_css_classes:
                    clean_css_classes.append(i)

            for selector in clean_css_classes:
                self.add_selector(selector, css_file)

        print('CSS separation display css_selectors: ' + str(self.css_selectors))


sys.setrecursionlimit(10000)

project_dir = '/home/incode7/PycharmProjects/incodeParsing'

test_rectifier = CSSRectifier()
test_rectifier.do_rectifier(project_dir)
