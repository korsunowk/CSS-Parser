with open('css_file', 'r+') as css_file:
    cssArray = [line for line in css_file if line.isspace() is False]

classesArray = [line.rstrip()[:-2] for line in cssArray if line.find('{') > 0]   \

#    Для файлов, в которых соблюдены стандарты.

classesArray = []
for line in range(len(cssArray)):
    if cssArray[line].find('{') >= 0:
        if len(cssArray[line].rstrip()) == 1 or cssArray[line].find('\t{') >= 0 or cssArray[line].find(';') > 0:
                classesArray.append(cssArray[line-1].rstrip())
        else:
            if cssArray[line].find('@media') == -1:
                classesArray.append(cssArray[line].rstrip()[:-2].replace('\t', ''))

# Для файлов, в которых не соблюдены стандарты.
