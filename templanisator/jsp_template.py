import re
from templanisator import abstract_template


class JSPTemplateProcessor(abstract_template.AbstractTemplate):
    def do_template_processor(self, html_files):
        includes = dict()
        for file in html_files:
            self.check_file(file)
            for find in re.findall(u'<%@[^>]+%>', file.string_version):
                if find.find('include') > 0:
                    if file.name in includes.keys():
                        includes[file.name] = includes[file.name] + ', ' + find
                    else:
                        includes[file.name] = find
        for html_file in html_files:
            if html_file.name in includes.keys():
                html_file.includes = includes[html_file.name]
        return self.template_build(html_files)

    def template_build(self, html_files):
        include_list = list()
        for html_file in html_files:
            if html_file.extention == "html" and html_file.includes:
                for include_string in html_file.includes.split(', '):
                    include_strings = ""
                    for i in super().path_generator(html_file.path, self.template_check_helper(
                            include_string.replace('"', "'"))):
                        include_file = self.get_file_to_include(html_files, i.__str__())
                        include_list.append(include_file.name)
                        include_strings += include_file.string_version
                    html_file.string_version = html_file.string_version.replace(include_string,
                                                                                include_strings)
        for file in html_files:
            if re.search(u'<%@ include[^>]+%>', file.string_version):
                html_files = self.do_template_processor(html_files)
                break
        return [html_file for html_file in html_files if html_file.name not in include_list]

    def get_file_to_include(self, html_files, name_of_file):
        for file in html_files:
            if file.path == name_of_file:
                return file

    def template_check_helper(self, include_string):
        return re.search(u"'.*?'", include_string).group().replace("'", '')

    @staticmethod
    def check_file(file):
        for find in re.findall(u'<jsp:[include page="][^>]+>', file.string_version):
            file.string_version = file.string_version.replace(
                find, "<%@ include file='" + re.search(
                    u'".*?"', find).group().replace('"', '') + "' %>"
            )
