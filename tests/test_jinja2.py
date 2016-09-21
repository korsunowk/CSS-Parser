import unittest


class TestJinja2Processor(unittest.TestCase):
    def test_includes(self):
        import templanisator.jinja_template as jinja_
        import files
        import pathlib
        import os

        files_to_jinja = []
        for path in pathlib.Path(os.getcwd()).glob('test_jinja_project/templates/*'):
            if os.path.isfile(path.__str__()):
                files_to_jinja.append(files.HTMLFile(path.__str__()))
            else:
                for second_path in os.listdir(path.__str__()):
                    files_to_jinja.append(files.HTMLFile(path.__str__() + '/' + second_path))

        results_files = [
            '{% load static %}{% load i18n %}<!DOCTYPE html><html><head><title>Base html</title></head><body>      '
            'INDEX HTML<div class="vacancy">    9999999999999999999 </div>9999999999999999999'
            '{% endblock %}</body></html>',
            '{% load static %}{% load i18n %}<!DOCTYPE html><html><head><title>Base html</title></head><body>      '
            '<div class="content"><div class="vacancy">    9999999999999999999 </div></div>'
            '{% endblock %}</body></html>',
            '{% load static %}{% load i18n %}<!DOCTYPE html><html><head><title>Base html</title></head><body>      '
            '<div class="all_vacancies"><p>All vacancies</p></div>{% endblock %}</body></html>'
        ]
        for new_file in jinja_.Jinja2TemplateProcessor().do_template_processor(files_to_jinja):
            if new_file.string_version in results_files:
                results_files.pop(results_files.index(new_file.string_version))

        self.assertEqual([], results_files)
