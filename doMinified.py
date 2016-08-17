def minification(pathlist):
    fullcss, finalcss = '', ''
    for file in pathlist:
        with open(file, 'r+') as f:
            fullcss += f.read()

    fullcss = fullcss.replace("\t","").replace("\n","")

    for match in re.finditer(u"\/*[^}]+\*/", fullcss):
        fullcss = fullcss.replace(match.group(), "")

    space,media = False, False
    
    for i in range(len(fullcss)):
        if fullcss[i].isspace() is True and fullcss[i+1] == '{' or fullcss[i].isspace() is True and fullcss[i-1] == ':':
            continue
        elif fullcss[i] == ',' and fullcss[i+1].isspace() is True:
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
