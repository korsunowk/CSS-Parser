import sys
import os

sys.setrecursionlimit(10900)

css_files = []
html_files = []


def find_dirs(home_directory, start=True, iteration=2, home='', old_dir=-1):
    global css_files
    global html_files

    if start:
        home = home_directory.replace("/"+home_directory.split('/')[-1], "")

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
                    css_files.append(os.getcwd() + '/' + item)                          # cобираем все css в один.

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
            return True


project_dir = '/home/incode7/Desktop/TheRealGleb'             # путь к проекту для тестирования.

find_dirs(project_dir)

classesArray = []

for file in css_files:
    with open(file, 'r+') as f:
        cssArray = [line for line in f if line.isspace() is False]
        for line in range(len(cssArray)):
            if cssArray[line].find('{') >= 0:
                if len(cssArray[line].rstrip()) == 1 or cssArray[line].find('\t{') >= 0 or cssArray[line].find(';') > 0:
                    if cssArray[line - 1].rstrip() not in classesArray:
                        classesArray.append(cssArray[line - 1].rstrip())
                else:
                    if cssArray[line].find('@media') == -1:
                        if cssArray[line].rstrip()[:-2].replace('\t', '') not in classesArray:
                            classesArray.append(cssArray[line].rstrip()[:-2].replace('\t', ''))

classesArray1 = []

for line in range(len(classesArray)):
    if classesArray[line].find('::') < 0 and classesArray[line].find(':') < 0:
        classesArray1.append(classesArray[line])

# classesArray1 = массив css классов без префиксов.

htmlArray = []
for file in html_files:
    with open(file, 'r+') as f:
        for line in [line for line in f if line.isspace() is False]:
            if line not in htmlArray:
                htmlArray.append(line)


usedClasses = []
for htmlLine in htmlArray:
    for cssClass in classesArray1:
        if (htmlLine.find(cssClass) > 0 or htmlLine.find(cssClass[1:]) > 0)\
                and cssClass not in usedClasses:
            usedClasses.append(cssClass)


finalArray = []
for cssClass in classesArray1:
    if cssClass not in usedClasses and cssClass.find('  ') < 0:
        finalArray.append(cssClass)


for i in finalArray:
    print(i)
