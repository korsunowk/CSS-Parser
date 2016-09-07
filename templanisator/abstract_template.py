from abc import ABCMeta, abstractclassmethod


class AbstractTemplate(metaclass=ABCMeta):
    @abstractclassmethod
    def do_template_processor(self, html_files):
        pass

    @abstractclassmethod
    def template_build(self, html_files):
        pass

    @abstractclassmethod
    def get_html_file_to_include(self, html_files, name_of_file):
        pass

    @abstractclassmethod
    def template_check_helper(self, find):
        pass
