# -*- coding: utf-8 -*-

import css_selectors
import files
import templanisator.jinja_template as jinja_
import templanisator.jade_template as jade_
import templanisator.jsp_template as jsp_
import templanisator.ejs_template as ejs_
import static_classes
import rectifiler_report
import sys
import os
import re
import time

start_time = time.time()


class CSSRectifier:
    def __init__(self):
        self.ignore, self.files = list(), list()
        self.css_files, self.html_files = list(), list()

        self.css_selectors = list()
        self.percent_of_usage = str()

    def get_some_files(self, *extentions):
        return [file for file in self.files if file.extention in extentions]

    def add_selector(self, _selector, css_file):
        if len(self.css_selectors) > 0:
            tmp = list()
            for i in self.css_selectors:
                tmp.append(i.name)
            if _selector not in tmp:
                new_selector = css_selectors.CSSSelector(_selector, css_file)
                new_selector.add_line(css_file)
                self.css_selectors.append(new_selector)
            else:
                i = tmp.index(_selector)
                self.css_selectors[i].add_file(css_file)
                self.css_selectors[i].add_line(css_file)
        else:
            self.css_selectors.append(css_selectors.CSSSelector(_selector, css_file))

    def load_custom_ignore_files(self, dir_to_project):
        try:
            with open(dir_to_project+'/rectifiler_ignore.txt', 'r+') as f:
                for line in f:
                    if line[0] != '#':
                        self.ignore.append(line.rstrip())
        except FileNotFoundError:
            pass

    def load_ignore_files(self, dir_to_project):
        try:
            self.load_custom_ignore_files(dir_to_project)
            with open(BASEDIR + '/files to ignore.txt', 'r+') as f:
                for line in f:
                    if line.rstrip() not in self.ignore:
                        self.ignore.append(line.rstrip())
        except FileNotFoundError:
            with open(BASEDIR + '/files to ignore.txt', 'w') as f:
                for line in ['bootstrap.css', 'bootstrap.min.css', 'bootstrap-responsive.css',
                             'bootstrap-responsive.min.css', 'font-awesome.css',
                             'node_modules', 'venv', 'tmp',
                             'bootstrap.css.map', 'bootstrap.min.css.map',
                             'bootstrap.theme.css', 'bootstrap.theme.css.map',
                             'bootstrap.theme.min.css', 'bootstrap.theme.min.css.map']:
                    f.write(str(line)+'\n')
            self.load_ignore_files(dir_to_project)

    def do_rectifier(self, home_directory):
        self.load_ignore_files(dir_to_project=home_directory)
        static_classes.Finder.load_ignore_pseudo()

        for root, dirs, files_ in os.walk(home_directory):
            for one_dir in dirs:
                if one_dir in self.ignore:
                    dirs.remove(one_dir)

            for file in files_:
                if (file[-4:] == 'html' or file[-3:] == 'htm' or file[-3:] == 'css'
                        or file[-4:] == 'jade' or file[-3:] == 'jsp' or file[-3:] == 'ejs') \
                        and file not in self.ignore:
                    self.files.append(files.MyFile(path=os.path.join(root, file)))
        return self.css_minification()

    def css_minification(self):
        print('Start minification....')
        for file in self.get_some_files('css'):
            with open(file.path, 'r+') as f:
                css_file = f.read()
                css_file = css_file.replace("\t", "").replace("\n", "")

            for match in re.finditer(u"/*[^/]+\*/", css_file):
                css_file = css_file.replace(match.group(), "")

            space, media = False, False
            final_css = str()
            for i in range(len(css_file)):
                if css_file[i].isspace() and (css_file[i + 1] == '{' or css_file[i - 1] == ':'
                                              or css_file[i + 1] == '+' or css_file[i + 1] == '~'
                                              or css_file[i + 1] == '>' or css_file[i - 1] == ','):
                    continue
                elif css_file[i] == '@' and css_file[i:i + 6] == '@media'\
                        or css_file[i] == '@' and css_file[i:i+9] == '@-webkit-'\
                        or css_file[i] == '@' and css_file[i:i+6] == '@-moz-':
                    media = True
                elif css_file[i] == '{' and media is False:
                    space = True
                elif css_file[i] == '}':
                    space = False

                if space is True:
                    final_css += css_file[i].rstrip()
                else:
                    final_css += css_file[i]

            self.css_files.append(files.CSSFile(file.path, final_css))
        self.css_separation()

    def css_separation(self):
        print('Start separation....')
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
                    if i[0] == ';':
                        clean_css_classes.append(i[1:])
                    else:
                        clean_css_classes.append(i)

            for clean_selector in clean_css_classes:
                self.add_selector(clean_selector, css_file)

            for clean_selector in self.css_selectors:
                clean_selector.parsing_alone_selectors()

        self.find_selectors_in_html()

    def create_html_files(self):
        self.html_files = [files.HTMLFile(file.path) for file in self.get_some_files('html', 'htm')]
        if template:
            print('Do Template Processor...')
            if template.lower() == 'jinja2':
                self.html_files = jinja_.Jinja2TemplateProcessor(self.html_files).files
            elif template.lower() == 'jade':
                self.html_files = jade_.JadeTemplateProcessor(
                    self.html_files + [files.JadeFile(file.path) for file in self.get_some_files('jade')]
                ).files
            elif template.lower() == "jsp":
                self.html_files = jsp_.JSPTemplateProcessor(
                    self.html_files + [files.JSPFile(file.path) for file in self.get_some_files('jsp')]
                ).files
            elif template.lower() == "ejs":
                self.html_files = ejs_.EJSTemplateProcessor(
                    self.html_files + [files.EJSFile(file.path) for file in self.get_some_files('ejs')]
                ).files
            else:
                print('Enter correct Template Processor.')
                exit()
        return self.html_files

    def find_selectors_in_html(self):
        print('Start find selectors....')
        for html_file in self.create_html_files():
            html_file.check_tags(html_file.string_version)
            for combo_selector in self.css_selectors:
                try:
                    static_classes.Finder.find_selectors_in_html(html_file.string_version, combo_selector)
                    if combo_selector.usage is False and combo_selector.kind_usage is True:
                        for alone_selector in combo_selector.alone_selectors:
                            if alone_selector.alone_usage_for_file is True:
                                alone_selector.usage_files.append(html_file)
                                alone_selector.alone_usage_for_file = False
                    else:
                        continue
                except TypeError:
                    continue

        self.calculate_percent_of_usage()

    def do_report(self):
        not_used_selectors = list()
        for not_used_selector in self.css_selectors:
            if not_used_selector.usage is False:
                not_used_selectors.append(not_used_selector)

        html = False
        html_files = list()

        for html_file in self.html_files:
            if html_file.opened_and_closed_tags_check is False:
                html_files.append(html_file)
                html = True

        rectifiler_report.RectifilerReport(
            percent=self.percent_of_usage,
            selectors=not_used_selectors,
            html=html,
            html_files=html_files
        )

    def calculate_percent_of_usage(self):
        usage_selectors = list()
        for selector_ in self.css_selectors:
            if selector_.usage:
                usage_selectors.append(selector_)
        try:
            self.percent_of_usage = 'Percent of usage: %s' \
                                    % str(round(len(usage_selectors)/len(self.css_selectors) * 100, 2)) + '%'
        except ZeroDivisionError:
            self.percent_of_usage = 'Percent of usage: 0%'


if __name__ == '__main__':
    sys.setrecursionlimit(10000)

    BASEDIR = os.path.dirname(
        os.path.realpath(sys.argv[0])
    )
    project_dir = os.getcwd()
    report, template = False, False

    args = sys.argv[1:]
    if '--path' in args:
        try:
            project_dir = os.path.realpath(args[args.index('--path')+1])
        except IndexError:
            pass
    if '--report' in args:
        report = True
    if '--template' in args:
        try:
            template = args[args.index('--template')+1]
        except IndexError:
            print('Input Template processor')
            template = None
    list_to_output = list()

    rectifier = CSSRectifier()
    rectifier.do_rectifier(project_dir)

    if report:
        rectifier.do_report()
    else:
        for css_selector in rectifier.css_selectors:
            if not css_selector.usage:
                print(css_selector)
    print("--- %s seconds ---" % (time.time() - start_time))
