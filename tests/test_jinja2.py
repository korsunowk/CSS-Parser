import unittest
import templanisator.jinja_template as jinja_
import files
import os


class TestJinja2Processor(unittest.TestCase):
    def test_includes(self):
        files_to_jinja = []
        for path in os.walk(os.getcwd()+'/tests/test_jinja_project'):
            if len(path[2]) > 0:
                for second_path in path[2]:
                    if second_path.find('css') >= 0:
                        continue
                    files_to_jinja.append(files.HTMLFile(path[0] + '/' + second_path))

        results_files = [
            '{% load static %}{% load i18n %}<!DOCTYPE html><html><head><title>{% block title %}Base HTML{% endblock %}'
            '</title></head><body>      {% block content %}<div class="content"><div class="vacancy">    '
            '9999999999999999999!!!!!!!TEST!!!!!!!!!!1 </div></div>{% endblock %}{% endblock %}</body></html>',
            '{% load static %}{% load i18n %}<!DOCTYPE html><html><head><title>{% block title %}Base HTML{% endblock %}'
            '</title></head><body>      {% block content %}<div class="all_vacancies"><p>All vacancies</p></div>'
            '{% endblock %}{% endblock %}</body></html>',
            '{% load static %}{% load i18n %}<!DOCTYPE html><html><head><title>{% block title %}Base HTML{% endblock %}'
            '</title></head><body>      {% block content %}9999999999999999999!!!!!!!TEST!!!!!!!!!!1'
            '<div class="vacancy">    9999999999999999999!!!!!!!TEST!!!!!!!!!!1 </div>{% endblock %}{% endblock %}'
            '</body></html>',
            '{% load static %}{% load i18n %}<!DOCTYPE html><html><head><title>{% block title %}Base HTML{% endblock %}'
            '</title></head><body>      {% block content %}{% endblock %}</body></html>',
            '9999999999999999999!!!!!!!TEST!!!!!!!!!!1',
            '<div class="vacancy">    9999999999999999999!!!!!!!TEST!!!!!!!!!!1 </div>',
            '!!!!!!!TEST!!!!!!!!!!1'
        ]

        for new_file in jinja_.Jinja2TemplateProcessor(files_to_jinja).files:
            if new_file.string_version in results_files:
                results_files.pop(results_files.index(new_file.string_version))

        self.assertEqual([], results_files)
