# -*- coding: utf-8 -*-

import re
# from css_selectors import AloneCSSSelector, CSSSelector
import css_selectors


class CSSRectifierFinderError(Exception):
    pass


class Check:
    @staticmethod
    def check_letter(letter):
        if letter.isspace() is True or letter == ',' or letter == '>' or letter == '+' or letter == '~':
            return True

        return False

    @staticmethod
    def check_word(word):
        if word == '':
            return False
        for i in word:
            if Check.check_letter(i) is True:
                return False
        return True

    @staticmethod
    def find_not_for_check_pseudo(selector_with_pseudo):
        if selector_with_pseudo.find(':not') >= 0:
            return True
        return False

    @staticmethod
    def check_pseudo(selector_with_pseudo):
        if selector_with_pseudo.find('::') >= 0 and Check.find_not_for_check_pseudo(selector_with_pseudo) is False:
            return False
        return True


class Finder:
    ignore = list()

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
            new_selector2.append(problem_selector[1][problem_selector[1].find('=') + 1:])

        return new_selector2

    @staticmethod
    def load_ignore_pseudo():
        try:
            with open('pseudo classes to ignore.txt', 'r+') as f:
                for line in f:
                    Finder.ignore.append(line.rstrip())
        except FileNotFoundError:
            with open('pseudo classes to ignore.txt', 'w') as f:
                for line in [':visited', ':valid', ':root',
                             ':link', ':indeterminate', ':hover',
                             ':focus', ':default', ':checked',
                             ':active', ':invalid', ':value',
                             ':reveal', ':expand', ':fill'
                             ':clear', ':check', ':browse',
                             ':before', ':after', ':selection']:
                    f.write(str(line)+'\n')
            Finder.load_ignore_pseudo()

    @staticmethod
    def find_selector_with_equal(combo_selector, new_selector, html_file_as_string,
                                 return_find=False, multiple=False, return_findall=False):
        return_findall_list = list()
        if new_selector[1][new_selector[1].find('=') - 1] in ['~', '*', '$', '^']:
            problem_selector = Finder.parsing_problem_selector(new_selector, True)
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
                            if multiple is True:
                                return True
                            if return_find is not False:
                                return find
                            elif return_findall is True:
                                return_findall_list.append(find)
                            else:
                                combo_selector.usage = True
                elif problem_selector[2] == '*=':
                    if problem_selector[1][-1] != '-':
                        if find.find(problem_selector[1]) > 0 \
                                and find.find(problem_selector[3][1:-1]) > 0:
                            if multiple is True:
                                return True
                            if return_find is not False:
                                return find
                            elif return_findall is True:
                                return_findall_list.append(find)
                            else:
                                combo_selector.usage = True
                    else:
                        if find.find(problem_selector[3][1:-1]) > 0 \
                                and find.find(problem_selector[1]) > 0:
                            if multiple is True:
                                return True
                            if return_find is not False:
                                return find
                            elif return_findall is True:
                                return_findall_list.append(find)
                            else:
                                combo_selector.usage = True

                elif problem_selector[2] == '$=':
                    str_to_search = u'%s="[^"]+"' \
                                    % (problem_selector[1])
                    clean_find = re.search(str_to_search, find).group()[
                                 len(problem_selector[1] + '="'):-1]

                    if clean_find.endswith(problem_selector[3][1:-1]) is True:
                        if multiple is True:
                            return True
                        if return_find is not False:
                            return find
                        elif return_findall is True:
                            return_findall_list.append(find)
                        else:
                            combo_selector.usage = True
                elif problem_selector[2] == '^=':
                    str_to_search = u'%s="[^"]+"' \
                                    % (problem_selector[1])
                    if re.search(str_to_search, find).group()[
                       len(problem_selector[1] + '="'):].find(
                            problem_selector[3][1:-1]) == 0:
                        if multiple is True:
                            return True
                        if return_find is not False:
                            return find
                        elif return_findall is True:
                            return_findall_list.append(find)
                        else:
                            combo_selector.usage = True
        else:
            problem_selector = Finder.parsing_problem_selector(new_selector)
            if problem_selector[0].find('.') == 0:
                str_to_search = u'%s[^>]+>' % Finder.find_class_selector(problem_selector[0][1:],
                                                                         html_file_as_string, return_find)
            elif problem_selector[0].find('#') == 0:
                str_to_search = u'%s[^>]+>' % Finder.find_id_selector(problem_selector[0][1:],
                                                                      html_file_as_string, return_find)
            else:
                str_to_search = u'<%s[^>]+>' % (problem_selector[0])

            for find in re.findall(str_to_search, html_file_as_string):
                if find.find(problem_selector[1] + problem_selector[2]) > 0 \
                        and find.find(problem_selector[3]) > 0:
                    if multiple is True:
                        return True
                    if return_find is not False:
                        return find
                    elif return_findall is True:
                        return_findall_list.append(find)
                    else:
                        combo_selector.usage = True
        if return_find is True:
            return return_findall_list

    @staticmethod
    def find_class_selector(alone_selector, html_file_as_string,
                            return_find=False, return_findall=False):
        findall_list = list()
        for find in re.findall(u'class="[^"]+"', html_file_as_string):
            for one_class in find.replace('class=', '')[1:-1].split(' '):
                if one_class == alone_selector:
                    if return_find is True:
                        return find
                    elif return_findall is True:
                        findall_list.append(find)
                    else:
                        return True
        if return_findall is True:
            return findall_list

        return False

    @staticmethod
    def find_id_selector(alone_selector, html_file_as_string, return_find=False, return_findall=False):
        return_findall_list = list()
        for find in re.findall(u'id="[^"]+"', html_file_as_string):
            for one_id in find.replace('id=', '')[1:-1].split(' '):
                if one_id == alone_selector:
                    if return_find is True:
                        return find
                    elif return_findall is True:
                        return_findall_list.append(find)
                    else:
                        return True
        if return_find is True:
            return return_findall_list
        return False

    @staticmethod
    def find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector, html_file_as_string,
                                           find_word, find_range, multiple=False, return_find=False):
        if alone_selector[0][0] != '.' and alone_selector[0][0] != '#':
            str_to_find = u'<%s>' % alone_selector[0]
            array_to_find = re.findall(str_to_find, html_file_as_string)
            find_iter = False
            for find in array_to_find:
                if find.find(find_word) in find_range:
                    if multiple is True:
                        return True
                    elif return_find is True:
                        return find
                    find_iter = True
                    combo_selector.usage = True
            if find_iter is not True:
                str_to_find = u'<%s[^>]+>' % alone_selector[0]
                array_to_find = re.findall(str_to_find, html_file_as_string)
                for find in array_to_find:
                    if find.find(find_word) in find_range:
                        if multiple is True:
                            return True
                        elif return_find is True:
                            return find
                        combo_selector.usage = True
        else:
            if alone_selector[0][0] == '.':
                if multiple is True:
                    return Finder.find_class_selector(alone_selector[0][1:], html_file_as_string)
                elif return_find is True:
                    return Finder.find_class_selector(alone_selector[0][1:], html_file_as_string, return_find=True)
                else:
                    result = Finder.find_class_selector(alone_selector[0][1:], html_file_as_string)
                    if result is True:
                        combo_selector.usage = result
            elif alone_selector[0][0] == '#':
                if multiple is True:
                    return Finder.find_id_selector(alone_selector[0][1:], html_file_as_string)
                elif return_find is True:
                    return Finder.find_id_selector(alone_selector[0][1:], html_file_as_string, return_find=True)
                else:
                    result = Finder.find_id_selector(alone_selector[0][1:], html_file_as_string)
                    if result is True:
                        combo_selector.usage = result

    @staticmethod
    def find_hard_not_ignore_pseudo_helper(combo_selector, analyzed_alone_selector, html_file_as_string,
                                           return_find=True):
        if analyzed_alone_selector[0] == '.':
            return Finder.find_class_selector(analyzed_alone_selector[1:], html_file_as_string, return_find)
        elif analyzed_alone_selector[0] == '#':
            return Finder.find_id_selector(analyzed_alone_selector[1:], html_file_as_string, return_find)
        else:
            return Finder.find_trivial_selector(combo_selector, analyzed_alone_selector, html_file_as_string,
                                                return_find)

    @staticmethod
    def find_hard_not_ignore_pseudo(combo_selector, analyzed_alone_selector, html_file_as_string, multiple=False,
                                    return_find=False):

        if analyzed_alone_selector[1].find(':') == -1 and analyzed_alone_selector[0].find(':') == -1:
            if analyzed_alone_selector[1] == 'empty':
                str_to_find = u'<%s></%s>' % (analyzed_alone_selector[0], analyzed_alone_selector[0])
                for find in re.findall(str_to_find, html_file_as_string):
                    if find:
                        if multiple is True:
                            return True
                        elif return_find is True:
                            return find
                        else:
                            combo_selector.usage = True
            elif analyzed_alone_selector[1] in ['first-child', 'last-child']\
                    or analyzed_alone_selector[1].find('nth-child') > 0\
                    or analyzed_alone_selector[1].find('nth-last-child') > 0:
                result = Finder.find_hard_not_ignore_pseudo_helper(combo_selector,
                                                                   analyzed_alone_selector[0], html_file_as_string)

                if result is not False:
                    str_to_find = '%s[^/]+/' % result
                    if str_to_find:
                        for find in re.findall(str_to_find, html_file_as_string):
                            if find.count('>') > 1 or find.find('<img') > 0:
                                if multiple is True:
                                    return True
                                elif return_find is True:
                                    return find
                                else:
                                    combo_selector.usage = True
            elif analyzed_alone_selector[1] in ['first-of-type', 'last-of-type']\
                    or analyzed_alone_selector[1].find('nth-of-type') > 0\
                    or analyzed_alone_selector[1].find('nth-last-of-type') > 0:

                result = Finder.find_hard_not_ignore_pseudo_helper(combo_selector,
                                                                   analyzed_alone_selector[0], html_file_as_string)
                if result is not False and result is not None:
                    if result[-1] != '/':
                        str_to_find = '<[^/]+%s' % result
                        for find in re.findall(str_to_find, html_file_as_string):
                            str_to_find2 = find
                            for i in range(html_file_as_string.find(find) + len(find), len(html_file_as_string)):
                                str_to_find2 += html_file_as_string[i]
                                if str_to_find2.find('</') > 0:
                                    if multiple is True:
                                        return True
                                    elif return_find is True:
                                        return find
                                    else:
                                        combo_selector.usage = True
                                    break
                    else:
                        str_to_find = result
                        for i in range(html_file_as_string.find(result) + len(result), len(html_file_as_string)):
                            str_to_find += html_file_as_string[i]
                            if str_to_find.count('</') > 1:
                                if multiple is True:
                                    return True
                                elif return_find is True:
                                    return result
                                else:
                                    combo_selector.usage = True
                                break
            elif analyzed_alone_selector[1] in ['only-child', 'only-of-type']:
                result = Finder.find_hard_not_ignore_pseudo_helper(combo_selector,
                                                                   analyzed_alone_selector[0], html_file_as_string)
                if result is not False and result is not None:
                    str_to_find = result
                    if analyzed_alone_selector[1] == 'only-child':
                        for i in range(html_file_as_string.find(str_to_find) + len(str_to_find),
                                       len(html_file_as_string)):
                            str_to_find += html_file_as_string[i]
                            if str_to_find.find('</') > 0:
                                if multiple is True:
                                    return True
                                elif return_find is True:
                                    return True
                                else:
                                    combo_selector.usage = True
                                break
                    else:
                        begin_str, end_str = '', ''
                        for i in reversed(range(html_file_as_string.find(str_to_find))):
                            begin_str += html_file_as_string[i]
                            if begin_str.find('</') >= 0:
                                break
                            else:
                                if begin_str.find('<') >= 0:
                                    for j in range(html_file_as_string.find(str_to_find)+len(str_to_find),
                                                   len(html_file_as_string)):
                                        end_str += html_file_as_string[j]
                                        if end_str.find('<') >= 0:
                                            if html_file_as_string[j+1] == '/':
                                                if multiple is True:
                                                    return True
                                                elif return_find is True:
                                                    return True
                                                else:
                                                    combo_selector.usage = True
                                                break
                                            else:
                                                break
                                    break

            elif analyzed_alone_selector[1].find('not') >= 0:
                if analyzed_alone_selector[1].find('[') > 0:
                    hard_selector_in_bracket = analyzed_alone_selector[1][4:-1]

                    if hard_selector_in_bracket.find('=') > 0:
                        result = Finder.find_selector_with_equal(combo_selector,
                                                                 [analyzed_alone_selector[0],
                                                                  hard_selector_in_bracket[1:-1]],
                                                                 html_file_as_string, return_find=True)
                    else:
                        result = Finder.find_selector_without_equal(combo_selector,
                                                                    hard_selector_in_bracket,
                                                                    html_file_as_string, return_find=True)
                    if result:
                        if result.find(hard_selector_in_bracket):
                            if multiple is True:
                                return True
                            elif return_find is True:
                                return result
                            else:
                                combo_selector.usage = True
                else:

                    selector_in_bracket = analyzed_alone_selector[1][4:-1]
                    if selector_in_bracket[0] != '.' and selector_in_bracket[0] != '#':
                        # Если : или :: в скобках not().
                        if selector_in_bracket.find('::') >= 0:
                            dot = '::'
                        else:
                            dot = ':'
                        if ':' + analyzed_alone_selector[1].split(dot)[1][:-1] not in Finder.ignore:
                            Finder.find_easy_not_ignore_pseudo(combo_selector,
                                                               [analyzed_alone_selector[0],
                                                                analyzed_alone_selector[1].split(dot)[1][:-1]],
                                                               html_file_as_string)
                        else:
                            Finder.find_trivial_selector(combo_selector, analyzed_alone_selector[0],
                                                         html_file_as_string)
                    else:
                        if selector_in_bracket[0] == '.':
                            result = Finder.find_class_selector(selector_in_bracket[1:],
                                                                html_file_as_string, return_find=True)
                            if result:
                                str_to_search = '%s[^>]+>' % analyzed_alone_selector[0]
                                for find in re.findall(str_to_search, html_file_as_string):
                                    if find.find(result) >= 0:
                                        if multiple is True:
                                            return True
                                        elif return_find is True:
                                            return find
                                        else:
                                            combo_selector.usage = True
                        elif selector_in_bracket[0] == '#':
                            result = Finder.find_id_selector(selector_in_bracket[1:],
                                                             html_file_as_string, return_find=True)
                            if result:
                                str_to_search = '%s[^>]+>' % analyzed_alone_selector[0]
                                for find in re.findall(str_to_search, html_file_as_string):
                                    if find.find(result) >= 0:
                                        if multiple is True:
                                            return True
                                        elif return_find is True:
                                            return find
                                        else:
                                            combo_selector.usage = True

            elif analyzed_alone_selector[1].find('lang') >= 0:
                lang = analyzed_alone_selector[1].replace(')', '').split('(')
                lang = lang[0]+'="'+lang[1]+'"'
                result = Finder.find_hard_not_ignore_pseudo_helper(combo_selector,
                                                                   analyzed_alone_selector[0], html_file_as_string)
                if result is not False:
                    str_to_find = '%s[^>]+>' % result
                    for find in re.findall(str_to_find, html_file_as_string):
                        if find.find(lang) > 0:
                            if multiple is True:
                                return True
                            elif return_find is True:
                                return find
                            else:
                                combo_selector.usage = True
            elif analyzed_alone_selector[1] == 'target':
                if analyzed_alone_selector[0].find('.') != 0 and analyzed_alone_selector[0].find('#') != 0:
                    str_to_search = '<%s[^>]+>' % analyzed_alone_selector[0]
                    for find in re.findall(str_to_search, html_file_as_string):
                        if find.find('id=') > 0:
                            if multiple is True:
                                return True
                            elif return_find is True:
                                return find
                            else:
                                combo_selector.usage = True
                else:
                    result = Finder.find_hard_not_ignore_pseudo_helper(combo_selector,
                                                                       analyzed_alone_selector[0], html_file_as_string)
                    if result:
                        str_to_search = u'<[^>]+>'
                        for find in re.findall(str_to_search, html_file_as_string):
                            if find.find(result) > 0 and find.count('id=') > 1:
                                if multiple is True:
                                    return True
                                elif return_find is True:
                                    return find
                                else:
                                    combo_selector.usage = True
            elif analyzed_alone_selector[1] == 'first-letter' or analyzed_alone_selector[1] == 'first-line':
                result = Finder.find_hard_not_ignore_pseudo_helper(combo_selector,
                                                                   analyzed_alone_selector[0], html_file_as_string)
                if result:
                    str_to_search = u'%s[^/]+/' % result
                    for find in re.findall(str_to_search, html_file_as_string):
                        if find[find.rfind('>')+1:find.rfind('</')].find('>') == -1\
                                or find[find.rfind('>')+1:find.rfind('</')].find('<') == -1:
                            if len(find[find.rfind('>')+1:find.rfind('</')]) != 0:
                                if multiple is True:
                                    return True
                                elif return_find is True:
                                    return find
                                else:
                                    combo_selector.usage = True
            else:
                if multiple is True:
                    return False

        else:
            alone_pseudos = list()
            if analyzed_alone_selector[0].find(':') >= 0:
                alone_pseudos.append(analyzed_alone_selector[0].split(':')[1])
                alone_pseudos.append(analyzed_alone_selector[1])
            elif analyzed_alone_selector[1].find(':') >= 0:
                for alone_pseudo in analyzed_alone_selector[1].split(':'):
                    alone_pseudos.append(alone_pseudo)
            results = list()
            for alone_pseudo in alone_pseudos:
                if ':' + alone_pseudo in Finder.ignore:
                    results.append(Finder.find_trivial_selector(combo_selector, analyzed_alone_selector[0],
                                                                html_file_as_string, False, True))
                else:
                    if Finder.find_easy_not_ignore_pseudo(combo_selector, [analyzed_alone_selector[0],
                                                                           alone_pseudo], html_file_as_string) is False:
                        results.append(Finder.find_hard_not_ignore_pseudo(combo_selector,
                                                                          [analyzed_alone_selector[0], alone_pseudo],
                                                                          html_file_as_string, multiple=True))

            if None not in results:
                combo_selector.usage = True

    @staticmethod
    def find_easy_not_ignore_pseudo(combo_selector, alone_selector, html_file_as_string,
                                    multiple=False, return_find=False):
        # :read - only и :read - write
        # :disabled и :enabled
        # ::-moz - placeholder ::-webkit - input - placeholder
        # :optional и :required
        # ::selection

        if alone_selector[1].find('read-write') >= 0:
            if multiple is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'readonly', [-1], multiple=True)
            elif return_find is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'readonly',
                                                                 [-1], return_find=True)
            else:
                Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                          html_file_as_string, 'readonly', [-1])

        elif alone_selector[1].find('read-only') >= 0:
            if multiple is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'readonly',
                                                                 [i for i in range(999)], multiple=True)
            elif return_find is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'readonly',
                                                                 [i for i in range(999)], return_find=True)
            else:
                Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                          html_file_as_string, 'readonly', [i for i in range(999)])

        elif alone_selector[1].find('enabled') >= 0:
            if multiple is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'disabled', [-1], multiple=True)
            elif return_find is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'disabled',
                                                                 [-1], return_find=True)
            else:
                Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                          html_file_as_string, 'disabled', [-1])
        elif alone_selector[1].find('disabled') >= 0:
            if multiple is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'disabled',
                                                                 [i for i in range(999)], multiple=True)
            elif return_find is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'disabled',
                                                                 [i for i in range(999)], return_find=True)
            else:
                Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                          html_file_as_string, 'disabled', [i for i in range(999)])
        elif alone_selector[1].find('placeholder') >= 0:
            if multiple is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'placeholder',
                                                                 [i for i in range(999)], multiple=True)
            elif return_find is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'placeholder',
                                                                 [i for i in range(999)], return_find=True)
            else:
                Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                          html_file_as_string, 'placeholder', [i for i in range(999)])
        elif alone_selector[1].find('optional') >= 0:
            if multiple is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'required', [-1], multiple=True)
            elif return_find is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'required',
                                                                 [-1], return_find=True)
            else:
                Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                          html_file_as_string, 'required', [-1])
        elif alone_selector[1].find('required') >= 0:
            if multiple is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'required',
                                                                 [i for i in range(999)], multiple=True)
            elif return_find is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'required',
                                                                 [i for i in range(999)], return_find=True)
            else:
                Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                          html_file_as_string, 'required', [i for i in range(999)])
        elif alone_selector[1].find('selection') >= 0:
            if multiple is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'selection',
                                                                 [i for i in range(999)], multiple=True)
            elif return_find is True:
                return Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                                 html_file_as_string, 'selection',
                                                                 [i for i in range(999)], return_find=True)
            else:
                Finder.find_easy_not_ignore_pseudo_helper(alone_selector, combo_selector,
                                                          html_file_as_string, 'selection', [i for i in range(999)])
        else:
            return False

    @staticmethod
    def find_pseudo_selector(combo_selector, alone_selector, html_file_as_string,
                             multiple=False, return_find=False):
        if Check.check_pseudo(alone_selector.name) is True:
            analyzed_alone_selector = alone_selector.name.split(':', 1)
            if analyzed_alone_selector[0] != '':
                if ':' + analyzed_alone_selector[1] in Finder.ignore:
                    combo_selector.alone_selectors.pop()
                    combo_selector.alone_selectors.append(css_selectors.AloneCSSSelector(analyzed_alone_selector[0]))

                    if multiple is True:
                        return Finder.find_selectors_in_html(html_file_as_string, combo_selector, multiple=True)
                    elif return_find is True:
                        return Finder.find_selectors_in_html(html_file_as_string, combo_selector, return_find=True)
                    else:
                        Finder.find_selectors_in_html(html_file_as_string, combo_selector)
                else:
                    if analyzed_alone_selector[1] in ['read-write', 'required', 'optional', 'placeholder',
                                                      'disabled', 'enabled', 'read-only']:
                        if multiple is True:
                            return Finder.find_easy_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                                                                      html_file_as_string, multiple=True)
                        elif return_find is True:
                            return Finder.find_easy_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                                                                      html_file_as_string, return_find=True)
                        else:
                            Finder.find_easy_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                                                               html_file_as_string)
                    else:
                        if multiple is True:
                            return Finder.find_hard_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                                                                      html_file_as_string, multiple=True)
                        elif return_find is True:
                            return Finder.find_hard_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                                                                      html_file_as_string, return_find=True)
                        else:
                            Finder.find_hard_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                                                               html_file_as_string)

            else:
                # Если псевдокласс указывается без селектора, то он будет применяться ко всем элементам документа.
                if multiple is True:
                    return True
                else:
                    combo_selector.usage = True
        else:
            analyzed_alone_selector = alone_selector.name.split('::')

            if analyzed_alone_selector[1] in ['read-write', 'required', 'optional', 'placeholder',
                                              'disabled', 'enabled', 'read-only'] \
                    or analyzed_alone_selector[1].find('placeholder') > 0:
                # Например ::-moz - placeholder ::-webkit - input - placeholder
                if multiple is True:
                    return Finder.find_easy_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                                                              html_file_as_string, multiple=True)
                elif return_find is True:
                    return Finder.find_easy_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                                                              html_file_as_string, return_find=True)
                else:
                    Finder.find_hard_not_ignore_pseudo(combo_selector, analyzed_alone_selector, html_file_as_string)
            else:
                # Finder.find_hard_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                #                                       html_file_as_string)
                ignored = False
                for ignore in Finder.ignore:
                    if analyzed_alone_selector[1].find(ignore[1:]) >= 0 and analyzed_alone_selector[1].find(':') == -1\
                                and analyzed_alone_selector[1].find('::') == -1:
                        ignored = True
                        if multiple is True:
                            return Finder.find_easy_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                                                                      html_file_as_string, multiple=True)
                        elif return_find is True:
                            return Finder.find_easy_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                                                                      html_file_as_string, return_find=True)
                        else:
                            Finder.find_easy_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                                                               html_file_as_string)
                if ignored is False:
                    if multiple is True:
                        return Finder.find_hard_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                                                                  html_file_as_string, multiple=True)
                    elif return_find is True:
                        return Finder.find_hard_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                                                                  html_file_as_string, return_find=True)
                    else:
                        Finder.find_hard_not_ignore_pseudo(combo_selector, analyzed_alone_selector,
                                                           html_file_as_string)

    @staticmethod
    def find_trivial_selector(combo_selector, alone_selector, html_file_as_string,
                              return_find=False, multiple=False, return_findall=False):
        if alone_selector.find('#') > 0 or alone_selector.find('.') > 0:
            if alone_selector.find('#') > 0 and alone_selector.find('.') > 0:
                if alone_selector.find('#') < alone_selector.find('.'):
                    # id and class in one selector
                    trivial_selector = alone_selector[0:alone_selector.find('#')]
                    selector_id = alone_selector[len(trivial_selector):][
                                  :alone_selector.find('.') - len(trivial_selector)]
                    selector_classes = alone_selector[len(trivial_selector)+len(selector_id):]
                else:
                    trivial_selector = alone_selector[0:alone_selector.find('.')]
                    selector_id = str()
                    for i in range(len(alone_selector[alone_selector.find('#'):])):
                        if alone_selector[alone_selector.find('#'):][i] == '.':
                            selector_id = alone_selector[alone_selector.find('#'):alone_selector.find('#')+i]
                            break
                    selector_classes = alone_selector.replace(trivial_selector, '').replace(selector_id, '')

                if selector_classes.count('.') > 1:
                    clean_selector_classes = list()
                    for selector_class in selector_classes.split('.'):
                        if selector_class != "":
                            clean_selector_classes.append(selector_class)
                else:
                    clean_selector_classes = [selector_classes[1:]]

                finded_id = False
                finded_classes = list()
                str_to_find = u'<%s[^>]+>' % trivial_selector
                for find in re.findall(str_to_find, html_file_as_string):
                    if find.find('class=') > 0 and find.find('id=') > 0:
                        for find_class in re.findall(u'class="[^"]+"', find):
                            for one_class in clean_selector_classes:
                                if find_class.find(one_class) > 0:
                                    finded_classes.append(True)
                                else:
                                    continue
                        for find_id in re.findall(u'id="[^"]+"', find):
                            if find_id.find(selector_id[1:]) > 0:
                                finded_id = True
                                break

                if len(finded_classes) == len(clean_selector_classes) and finded_id is True:
                    if multiple is True:
                        return True
                    else:
                        combo_selector.usage = True
                else:
                    return None
            else:
                # id or class in selector
                if alone_selector.find('#') > 0:
                    find_id = Finder.find_id_selector(alone_selector[alone_selector.find('#')+1:],
                                                      html_file_as_string, True)
                    for find in re.findall(u'%s[^>]+>' % alone_selector[:alone_selector.find('#')],
                                           html_file_as_string):
                            if find_id is not False and find.find(find_id) > 0:
                                if multiple is True:
                                    return True
                                elif return_find is True:
                                    return find
                                else:
                                    combo_selector.usage = True
                elif alone_selector.find('.') > 0:
                    find_class = Finder.find_class_selector(alone_selector[alone_selector.find('.')+1:],
                                                            html_file_as_string, True)
                    for find in re.findall(u'%s[^>]+>' % alone_selector[:alone_selector.find('.')],
                                           html_file_as_string):
                        if find_class is not False and find.find(find_class) > 0:
                            if multiple is True:
                                return True
                            elif return_find is True:
                                return find
                            else:
                                combo_selector.usage = True
        else:
            try:
                if return_find is False and return_findall is False:
                    if html_file_as_string.find('<' + alone_selector) > 0 \
                            or html_file_as_string.rfind('<' + alone_selector) > 0:
                        if multiple is True:
                            return True
                        else:
                            combo_selector.usage = True
                else:
                    return_findall_list = list()
                    str_to_find = u'<%s[^<]+<' % alone_selector
                    for find in re.findall(str_to_find, html_file_as_string):
                        if return_findall is True:
                            return_findall_list.append(find)
                        else:
                            return find
                    if return_findall is True:
                        return return_findall_list
            except AttributeError:
                pass
        return False

    @staticmethod
    def find_selector_without_equal(combo_selector, alone_selector, html_file_as_string,
                                    return_find=False, multiple=False, return_findall=False):
        return_findall_list = list()
        new_selector = alone_selector.replace(']', '').split('[')
        str_to_search = u'<%s[^>]+>' % (new_selector[0])
        if new_selector[1].find('-*'):
            str_to_find = new_selector[1].replace('*', '')
        else:
            str_to_find = new_selector[1]
        for find in re.findall(str_to_search, html_file_as_string):
            if find.find(str_to_find) > 0:
                if return_find is not False:
                    return find
                elif return_findall is True:
                    return_findall_list.append(find)
                else:
                    if multiple is True:
                        return True
                    else:
                        combo_selector.usage = True
        if return_find is True:
            return return_findall_list
        return False

    @staticmethod
    def find_selectors_in_html(html_file_as_string, combo_selector,
                               multiple=False, return_find=False, return_findall=False):
        try:
            if len(combo_selector.alone_selectors) == 1:
                alone_selector = combo_selector.alone_selectors[0]
                if alone_selector.name in ['¿', '+', '>', '~', ',']:
                    return None
                if alone_selector.name != '*':
                    if alone_selector.pseudo is False:
                        if alone_selector.name[0] != '.' and alone_selector.name[0] != '#':
                            if alone_selector.name.find('[') == -1:
                                if multiple is True:
                                    return Finder.find_trivial_selector(combo_selector, alone_selector.name,
                                                                        html_file_as_string, multiple=True)
                                elif return_find is True:
                                    return Finder.find_trivial_selector(combo_selector, alone_selector.name,
                                                                        html_file_as_string, return_find=True)
                                elif return_findall is True:
                                    return Finder.find_trivial_selector(combo_selector, alone_selector.name,
                                                                        html_file_as_string, return_findall=True)
                                else:
                                    Finder.find_trivial_selector(combo_selector, alone_selector.name,
                                                                 html_file_as_string)
                            else:
                                new_selector = alone_selector.name.replace(']', '').split('[')
                                if new_selector[1].find('=') > 0:
                                    if multiple is True:
                                        return Finder.find_selector_with_equal(combo_selector, new_selector,
                                                                               html_file_as_string, multiple=True)
                                    elif return_find is True:
                                        return Finder.find_selector_with_equal(combo_selector, new_selector,
                                                                               html_file_as_string, return_find=True)
                                    elif return_findall is True:
                                        return Finder.find_selector_with_equal(combo_selector, new_selector,
                                                                               html_file_as_string, return_findall=True)
                                    else:
                                        Finder.find_selector_with_equal(combo_selector, new_selector,
                                                                        html_file_as_string)
                                else:
                                    if multiple is True:
                                        return Finder.find_selector_without_equal(combo_selector, alone_selector.name,
                                                                                  html_file_as_string, multiple=True)
                                    elif return_find is True:
                                        return Finder.find_selector_without_equal(combo_selector, alone_selector.name,
                                                                                  html_file_as_string, return_find=True)
                                    elif return_findall is True:
                                        return Finder.find_selector_without_equal(combo_selector, alone_selector.name,
                                                                                  html_file_as_string,
                                                                                  return_findall=True)
                                    else:
                                        Finder.find_selector_without_equal(combo_selector,
                                                                           alone_selector.name,
                                                                           html_file_as_string)
                        else:
                            if alone_selector.name[0] == '.':
                                usage = Finder.find_class_selector(alone_selector.name[1:],
                                                                   html_file_as_string)
                                if multiple is True:
                                    return usage
                                elif return_find is True:
                                    return Finder.find_class_selector(alone_selector.name[1:],
                                                                      html_file_as_string, return_find=True)
                                elif return_findall is True:
                                    return Finder.find_class_selector(alone_selector.name[1:],
                                                                      html_file_as_string, return_findall=True)
                                else:
                                    if usage:
                                        combo_selector.usage = True

                            elif alone_selector.name[0] == '#':
                                usage = Finder.find_id_selector(alone_selector.name[1:],
                                                                html_file_as_string)
                                if multiple is True:
                                    return usage
                                elif return_find is True:
                                    return Finder.find_id_selector(alone_selector.name[1:],
                                                                   html_file_as_string, return_find=True)
                                elif return_findall is True:
                                    return Finder.find_id_selector(alone_selector.name[1:],
                                                                   html_file_as_string, return_findall=True)
                                else:
                                    if usage is True:
                                        combo_selector.usage = True
                    else:
                        if multiple is True:
                            return Finder.find_pseudo_selector(combo_selector, alone_selector,
                                                               html_file_as_string, multiple=True)
                        elif return_find is True:
                            return Finder.find_pseudo_selector(combo_selector, alone_selector,
                                                               html_file_as_string, return_find=True)
                        elif return_findall is True:
                            return Finder.find_pseudo_selector(combo_selector, alone_selector,
                                                               html_file_as_string)
                        else:
                            Finder.find_pseudo_selector(combo_selector, alone_selector,
                                                        html_file_as_string)
                else:
                    combo_selector.usage = True
            else:
                Finder.find_multiple_selectors(combo_selector, html_file_as_string)

        except CSSRectifierFinderError:
            pass
        except IndexError:
            pass

    @staticmethod
    def find_multiple_selectors(combo_selector, html_file_as_string):
        results = list()
        results_with_plus = list()
        results_with_gr = list()

        for alone_selector in combo_selector.alone_selectors:
            fake_combo_selector = css_selectors.CSSSelector(combo_selector.name, 'fake_file')
            fake_combo_selector.alone_selectors.append(alone_selector)
            try:
                tmp_result = Finder.find_selectors_in_html(html_file_as_string,
                                                           fake_combo_selector, multiple=True)
                results.append(tmp_result)
                if tmp_result is True:
                    if alone_selector.name[0] == '.' or alone_selector.name[0] == '#':
                        alone_selector.alone_usage = True
                        alone_selector.alone_usage_for_file = True
                        combo_selector.kind_usage = True
            except CSSRectifierFinderError:
                results.append(False)
            except IndexError:
                break

            del fake_combo_selector

        if False not in results:
            str_to_search = str()
            space = False
            greater = False
            for group_selector in combo_selector.alone_selectors:
                if group_selector.name in ['¿', '+', '>', '~', ',']:
                    fake_combo_selector = css_selectors.CSSSelector(combo_selector.name, 'fake_file')

                    try:
                        fake_alone_selector = combo_selector.alone_selectors[
                            combo_selector.alone_selectors.index(group_selector)-1
                        ]
                        fake_combo_selector.alone_selectors.append(fake_alone_selector)

                    except CSSRectifierFinderError:
                        break

                    if group_selector.name == '¿':
                        if space is True:
                            result1 = Finder.get_alone_selector_from_full_code(fake_combo_selector, str_to_search)
                        else:
                            result1 = Finder.find_selectors_in_html(html_file_as_string, fake_combo_selector,
                                                                    return_find=True)

                        str_to_search = Finder.get_full_code_on_selector(result1, html_file_as_string)

                        fake_combo_selector.alone_selectors.clear()
                        fake_combo_selector.alone_selectors.append(
                            combo_selector.alone_selectors[combo_selector.alone_selectors.index(group_selector) + 1]
                        )

                        result3 = Finder.find_selectors_in_html(str_to_search, fake_combo_selector, multiple=True)
                        if result3 is False:
                            for second_find in Finder.helper_with_full_code_searching(result1, html_file_as_string):
                                if Finder.find_selectors_in_html(second_find,
                                                                 fake_combo_selector, multiple=True) is True:
                                    result3 = True
                                    break
                            else:
                                result3 = False
                        results.append(result3)

                        space = True
                        if result3 is False:
                            continue
                    elif group_selector.name == ',':
                        space = False
                        greater = False
                    elif group_selector.name == '+' or group_selector.name == '~':
                        result = list(Finder.find_selectors_in_html(html_file_as_string,
                                                                    fake_combo_selector, return_findall=True))

                        fake_combo_selector.alone_selectors.clear()
                        fake_combo_selector.alone_selectors.append(
                            combo_selector.alone_selectors[combo_selector.alone_selectors.index(group_selector) + 1]
                        )

                        for str_to_search in result:
                            neighbor = Finder.get_full_code_on_selector(str_to_search, html_file_as_string,
                                                                        return_neighbor=True)
                            neighbor = neighbor[0].replace(neighbor[1], '')
                            if Finder.find_selectors_in_html(neighbor, fake_combo_selector, multiple=True) is True:
                                results_with_plus.append(True)
                                break
                        else:
                            results_with_plus.append(False)

                    elif group_selector.name == ">":
                        if space is True or greater is True:
                            result = [Finder.get_alone_selector_from_full_code(fake_combo_selector,
                                                                               str_to_search)]
                        else:
                            result = list(Finder.find_selectors_in_html(html_file_as_string,
                                                                        fake_combo_selector, return_findall=True))

                        fake_combo_selector.alone_selectors.clear()
                        fake_combo_selector.alone_selectors.append(
                            combo_selector.alone_selectors[combo_selector.alone_selectors.index(group_selector) + 1]
                        )

                        for str_to_search_ in result:
                            find = Finder.get_full_code_on_selector(str_to_search_, html_file_as_string)
                            if Finder.find_selectors_in_html(find, fake_combo_selector, multiple=True) is True:
                                results_with_gr.append(True)
                                str_to_search = find
                                break
                        else:
                            results_with_gr.append(False)
                            break
                        greater = True
                    del fake_combo_selector
        if False not in results and False not in results_with_plus and False not in results_with_gr:
            combo_selector.usage = True

    @staticmethod
    def helper_with_full_code_searching(str_to_search, html_file_as_string):
        if str_to_search:
            for find in Finder.get_full_code_on_selector(str_to_search, html_file_as_string, return_list=True):
                yield Finder.get_full_code_on_selector(find, html_file_as_string, twice_play=True)

    @staticmethod
    def get_alone_selector_from_full_code(combo_selector, str_to_search):
        kind_of_str_to_search = Finder.find_selectors_in_html(str_to_search, combo_selector,
                                                              return_find=True)

        return Finder.get_full_code_on_selector(kind_of_str_to_search, str_to_search)

    @staticmethod
    def get_full_code_on_selector(selector_to_search, html_file_as_string,
                                  return_neighbor=False, twice_play=False, return_list=False):
        try:
            if selector_to_search:
                if selector_to_search.find('<') == 0 and selector_to_search.find('</') > 0 \
                        and return_neighbor is False and twice_play is False:
                    return selector_to_search

                str_to_search = ''
                if selector_to_search[0] != '<':
                    for i in range(len(html_file_as_string[html_file_as_string.find(selector_to_search):])):
                        str_to_search += html_file_as_string[html_file_as_string.find(selector_to_search) - i - 1]
                        if html_file_as_string[html_file_as_string.find(selector_to_search) - i - 1] == '<':
                            break

                str_to_search = str_to_search[::-1] + selector_to_search
                for i in range(html_file_as_string.find(str_to_search) + len(str(str_to_search)),
                               len(html_file_as_string)):

                    str_to_search += html_file_as_string[i]
                    if html_file_as_string[i] == '>':
                        break
                str_to_search_begin, str_to_search_end = '', ''

                for i in str_to_search:
                    if i == ' ':
                        break
                    else:
                        str_to_search_end += i
                str_to_search_begin = str_to_search_end
                str_to_search_end = '</%s>' % str_to_search_end[1:]

                if str_to_search_begin.find('</') == 0:
                    str_to_search_begin = str_to_search_begin.replace(
                        re.match(u'</[^>]+>', str_to_search_begin).group(), ''
                    )
                    str_to_search_end = '</%s>' % str_to_search_begin[1:]
                if str_to_search_end.count('>') > 1:
                    str_to_search_end = str_to_search_end[:-1]

                broken_loop = 0
                for_return_list = list()
                for find in re.findall(u'%s.*?%s' % (str_to_search, str_to_search_end), html_file_as_string):
                    if find.count(str_to_search_begin) == find.count(str_to_search_end):
                        str_to_search = find
                        break
                    else:
                        if return_list:
                            for_return_list.append(find)
                            continue
                        loop = True
                        while loop is True:
                            if broken_loop == 25:
                                break
                            for second_find in re.findall(u'%s.*?%s' % (str_to_search, str_to_search_end),
                                                          html_file_as_string):
                                if second_find.count(str_to_search_begin) \
                                        == second_find.count(str_to_search_end):
                                    str_to_search = second_find
                                    loop = False
                                    break
                                str_to_search = second_find
                            if loop is False:
                                break
                            broken_loop += 1
                        if loop is False:
                            break
                if broken_loop == 25:
                    str_to_search = Finder.get_full_code_on_selector_helper(str_to_search, html_file_as_string,
                                                                            str_to_search_begin, str_to_search_end)

                if return_neighbor is True:
                    new_str_to_search = str_to_search + html_file_as_string[
                                                        html_file_as_string.find(str_to_search)+len(str_to_search):
                                                        html_file_as_string.find(str_to_search)+len(str_to_search)+5]

                    return Finder.get_full_code_on_selector(
                        new_str_to_search, html_file_as_string, twice_play=True), \
                        new_str_to_search

                if return_list:
                    return for_return_list
                return str_to_search
            else:
                return ''

        except AttributeError:
            pass

    @staticmethod
    def get_full_code_on_selector_helper(str_to_search, html_file_as_string, str_to_search_begin, str_to_search_end):
        for i in range(html_file_as_string.find(str_to_search)+len(str_to_search), len(html_file_as_string)):
            str_to_search += html_file_as_string[i]
            if str_to_search.count(str_to_search_begin) == str_to_search.count(str_to_search_end):
                break
        return str_to_search
