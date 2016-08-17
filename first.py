import sys
import os
import re


sys.setrecursionlimit(10000)

css_files = []
html_files = []
ignore = []


def load_ignore_files(path_to_project_folder):
    global ignore
    ignore.clear()
    os.chdir(path_to_project_folder)
    with open('files to ignore.txt', 'r+') as f:
        for line in f:
            ignore.append(line.rstrip())


def css_separation(minified_css_file):
    only_classes = []
    for match in re.finditer(u"{[^}]+}", minified_css_file):
        if match.group().count('{') > 1:
            only_classes.append(match.group().split('{')[1])
            minified_css_file = minified_css_file.replace(match.group(), "¿")
        else:
            minified_css_file = minified_css_file.replace(match.group(), '¿')

    minified_css_file = only_classes + minified_css_file.replace("}", '')[:-1].split('¿')
    media_count = [i for i in minified_css_file if i.find('@') >= 0]

    for i in media_count:
        minified_css_file.pop(minified_css_file.index(i))

    tmp_classes = []
    for i in minified_css_file:
        if i.find(':') >= 0:
            tmp = i
            for match in re.finditer(u":[a-z]+", i):
                tmp = tmp.replace(match.group(), '')
            minified_css_file.append(tmp)
            tmp_classes.append(i)
    for i in tmp_classes:
        minified_css_file.pop(minified_css_file.index(i))

    clean_css_classes = []
    for i in minified_css_file:
        if i not in clean_css_classes:
            clean_css_classes.append(i)

    print(clean_css_classes)
    return clean_css_classes


def css_minification(pathlist):
    fullcss, finalcss = '', ''
    for file in pathlist:
        with open(file, 'r+') as f:
            fullcss += f.read()

    fullcss = fullcss.replace("\t","").replace("\n","")     # Удаляем табуляцию и переход на новую строку.

    for match in re.finditer(u"\/*[^}]+\*/", fullcss):
        fullcss = fullcss.replace(match.group(), "")    # Удаляем комментарии.

    space, media = False, False

    for i in range(len(fullcss)):
        if fullcss[i].isspace() is True and fullcss[i+1] == '{' or fullcss[i].isspace() is True and fullcss[i-1] == ':':
            continue
        elif fullcss[i] == '@' and fullcss[i:i+6] == '@media':
            media = True
        elif fullcss[i] == '{' and media is False:
            space = True
        elif fullcss[i] == '}':
            space = False

        if space is True:
            finalcss += fullcss[i].rstrip()
        else:
            finalcss += fullcss[i]

    print(finalcss)
    return css_separation(finalcss)


def find_dirs(home_directory, start=True, iteration=2, home='', old_dir=-1):
    global css_files
    global html_files

    if start:
        home = home_directory.replace("/"+home_directory.split('/')[-1], "")
        load_ignore_files(home_directory)

        return find_dirs(
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
                    if item not in ignore:
                        print(item)
                        css_files.append(os.getcwd() + '/' + item)                          # cобираем все css в один.
                    else:
                        print('IGNORE: ' + item)
                elif os.path.isfile(os.getcwd() + '/' + item) and (item[-4:] == 'html' or item[-3:] == 'htm'):
                    html_files.append(os.getcwd() + '/' + item)                         # собираем все html в один.

                if os.path.isdir(os.getcwd() + '/' + item) and item != 'venv' and item != '.git':
                    os.chdir(os.getcwd() + '/' + item)
                    iteration += 2

                    return find_dirs(
                        os.getcwd(),
                        start=False,
                        iteration=iteration,
                        home=home,
                    )
            os.chdir('../')
            if home_directory is None:
                return css_minification(css_files)
            else:
                old_dir = os.listdir(os.getcwd()).index(home_directory.split('/')[-1])
                iteration -= 2

            return find_dirs(
                os.getcwd(),
                start=False,
                iteration=iteration,
                home=home,
                old_dir=old_dir,
            )

        else:
            return css_minification(css_files)


if __name__ == '__main__':

    project_dir = '/home/incode7/PycharmProjects/incodeParsing'
    find_dirs(project_dir)
