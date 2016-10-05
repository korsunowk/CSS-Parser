import re
import templanisator.abstract_template as abs_temp
import os


class EJSTemplateProcessor(abs_temp.AbstractTemplate):
    def __init__(self, files):
        super().__init__(files)

    def do_template_processor(self):
        for file in self.files:
            self.include(file)

    def include(self, file):
        for include in re.findall(u'<% include .*? %>', file.string_version):
            include_string = str()
            for path in super().path_generator(file.path, include.replace('<% include ', '').split()[0]):
                if os.path.isfile(path.__str__()) is False or file.path == path.__str__():
                    continue
                include_file = self.get_file_to_include(path.__str__())
                if include_file.string_version.find('<% include') >= 0:
                    self.include(include_file)
                include_string += include_file.string_version
            file.string_version = file.string_version.replace(include, include_string)
