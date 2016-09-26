import pyjade
import os
import re
from templanisator import jinja_template
import templanisator.abstract_template as abc_temp


class JadeTemplateProcessor(abc_temp.AbstractTemplate):
    def __init__(self, files):
        super().__init__(files)

    def do_template_processor(self):
        for file in self.files:
            self.include(file)
            self.extend(file)
            file.string_version = pyjade.simple_convert(file.string_version)

        self.files = jinja_template.Jinja2TemplateProcessor(self.files).files

    def include(self, file):
        for include in re.findall(u'include .*?\n', file.string_version):
            included_string = str()
            include_path = include.replace('include ', '').strip()
            if os.path.basename(include_path).find("*") == -1:
                if os.path.isfile(include_path) is False:
                    include_path += '.jade'
            for path in super().path_generator(file.path, include_path):
                if path.__str__() == file.path:
                    continue
                if os.path.isfile(path.__str__()):
                    included_file = self.get_file_to_include(path.__str__())
                    included_file.check_string_version()
                    if included_file.string_version.find('include ') > 0:
                        self.include(included_file)
                    included_string += included_file.string_version
            file.string_version = file.string_version.replace(include, included_string)

    @staticmethod
    def extend(file):
        if file.string_version.find('extends ') >= 0:
            extend_string = re.search(u'extends .*?\n', file.string_version).group()
            file.string_version = file.string_version.replace(extend_string,
                                                              '{%s extends "%s" %s}'
                                                              % ('%', extend_string.replace('extends ', "")
                                                                 .strip() + '.jade', '%'))
