import pyjade
import os
import re
from templanisator import abstract_template, jinja_template


class JadeTemplateProcessor(abstract_template.AbstractTemplate):
    def do_template_processor(self, html_with_jade_files):
        for file in html_with_jade_files:
            if file.extention == 'jade':
                if file.string_version.find('extends') == 0:
                    extention = False
                    extend = re.search(u'extends.*?\n', file.string_version).group().split(' ')
                    if len(extend) != 1:
                        tmp = extend[1].rstrip()
                        extend.pop()
                        extend.append(tmp)
                        file.add_base_name(extend[1])

                        if str(extend[1]).find('.') > 0:
                            extention = extend[1][str(extend[1]).find('.')+1:]
                        if extention:
                            base_file = self.get_file_to_include(
                                html_with_jade_files, extend[1], extention
                            )
                        else:
                            base_file = self.get_file_to_include(
                                html_with_jade_files, extend[1]
                            )
                        base_file.base = True

                if file.string_version.find('include') > 0:
                    for find in re.findall(u'include.*?\n', file.string_version):
                        extention = False
                        include = find.split(' ')
                        if len(include) != 1:
                            tmp = include[1].rstrip()
                            include.pop()
                            include.append(tmp)
                            if str(include[1]).find('.') > 0:
                                extention = include[1][str(include[1]).find('.')+1:]
                            if extention:
                                included_file = self.get_file_to_include(
                                    html_with_jade_files, include[1], extention
                                )
                            else:
                                included_file = self.get_file_to_include(
                                    html_with_jade_files, include[1]
                                )
                            file.add_include(included_file, find)
            else:
                continue

        return self.template_build(html_with_jade_files)

    def template_build(self, html_with_jade_files):
        return_list = list()
        not_alone_files = list()
        for file in html_with_jade_files:
            if len(file.includes) > 0:
                for include in file.includes:
                    try:
                        file.string_version = file.string_version.replace(include[1],
                                                                          include[0].string_version + '\n', 1)
                    except AttributeError:
                        file.string_version = file.string_version.replace(include[1], '\n', 1)

                    if file not in return_list:
                        return_list.append(file)

                    if file not in not_alone_files:
                        not_alone_files.append(file)
                    if include[0] not in not_alone_files:
                        not_alone_files.append(include[0])

        for file in html_with_jade_files:
            if file.base is False:
                if file.extention == 'jade' and file.string_version.find('extends') == 0:
                    if file.base_name != '':
                        file.string_version = file.string_version\
                            .replace('extends %s' % file.base_name, '{% ' + 'extends "%s"' % file.base_name + ' %}')
            else:
                return_list.append(file)
                not_alone_files.append(file)
            try:
                file.string_version = pyjade.simple_convert(file.string_version)
            except Exception as e:
                print(e)
                exit()

        for file in html_with_jade_files:
            if file not in not_alone_files:
                return_list.append(file)

        for file in html_with_jade_files:
            file.clear_all()

        return jinja_template.Jinja2TemplateProcessor().do_template_processor(return_list)

    def get_file_to_include(self, html_with_jade_files, name_of_file, extention=False):
        name_of_file = os.path.basename(name_of_file)
        for file in html_with_jade_files:
            if extention:
                if file.name == name_of_file:
                    return file
            else:
                if file.name_without_extention == name_of_file:
                    return file

    def template_check_helper(self, find):
        pass
