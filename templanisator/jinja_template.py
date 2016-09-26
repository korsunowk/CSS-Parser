import re
import templanisator.abstract_template as abc_temp
import os
import files


class Jinja2TemplateProcessor(abc_temp.AbstractTemplate):
    def __init__(self, html_files):
        super().__init__(html_files)

    def do_template_processor(self):
        for html_file in self.files:
            self.include(html_file)
            self.extends(html_file)

        return self.files

    def include(self, html_file):
        for find_include in re.findall(u'{% include [^}]+}', html_file.string_version):
            include_string = str()
            for path in super().path_generator(html_file.path,
                                               find_include[find_include.find('"') + 1:find_include.rfind('"')]):
                if html_file.path == path.__str__():
                    continue
                if os.path.isfile(path.__str__()):
                    included_file = self.get_file_to_include(name_of_file=path.__str__())
                    if included_file.string_version.find('{% include') > 0:
                        self.include(included_file)
                    include_string += included_file.string_version
            else:
                html_file.string_version = html_file.string_version.replace(find_include, include_string)

    def extends(self, html_file):
        for find_include in re.findall(u'{% extends [^}]+}', html_file.string_version):
            for path in abc_temp.AbstractTemplate.path_generator(html_file.path,
                                                                 find_include[
                                                                    find_include.find('"') + 1: find_include.rfind(
                                                                     '"')]):
                if os.path.isfile(os.path.realpath(path.__str__())):
                    base_file = self.get_file_to_include(name_of_file=os.path.realpath(path.__str__()))
                    tmp = base_file.string_version
                    if isinstance(html_file, files.JadeFile):
                        html_file.string_version = html_file.string_version.replace('\n', '')
                    for block in re.findall(u'{% block .*? %}.*?{% endblock %}', html_file.string_version):
                        tmp = \
                            tmp.replace(block[block.find('{%'):block.find('%}') + 2], block)
                    html_file.string_version = tmp
