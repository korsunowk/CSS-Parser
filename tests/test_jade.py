import unittest
import templanisator.jade_template as jade_
import files
import os


class TestJadeProcessor(unittest.TestCase):
    def test_includes(self):
        files_to_jade = []

        for path in os.walk(os.getcwd()+'/test_jade_project'):
            if path[2]:
                for path_ in path[2]:
                    if path_.find('.css') == -1:
                        files_to_jade.append(files.JadeFile(path[0].__str__() + '/' + path_))
        results_files = [
            '<!DOCTYPE html><html lang="en">  <head>{% block title %}{% endblock %}  </head>  <body>    '
            '<h1 class="title">Jade - node template engine</h1>    <div id="container">      <p>Get on it!</p>   '
            ' </div>  </body>{% block content %}{% endblock %}</html>',
            '<!DOCTYPE html><html lang="en">  <head>{% block title %}<2 class="jade"></2>{% endblock %}{% endblock %} '
            ' </head>  <body>    <h1 class="title">Jade - node template engine</h1>    <div id="container">      '
            '<p>Get on it!</p>    </div>  </body>{% block content %}<h1>my 2.jade</h1>{% endblock %}'
            '{% endblock %}</html>',
            '<!DOCTYPE html><html lang="en">  <head>{% block title %}<title>444444444444444444444444</title>'
            '{% endblock %}'
            '{% endblock %}  </head>  <body>    <h1 class="title">Jade - node template engine</h1>    '
            '<div id="container">      '
            '<p>Get on it!</p>    </div>  </body>{% block content %}<h1>4444444444444444444444444  '
            '<div class="included">    '
            '<h1>THIS IS FOLDER/5555555</h1>    <FOLDER>444 eqglp 		44444</FOLDER>  '
            '</div></h1>{% endblock %}{% endblock %}</html>',
            '<EW>,GWOEMGOPWEMGOWOPMEGMOWOPEGOPWMGOPMEOPEMGMOP</EW>',
            '<HTML>FILE NAME 6</HTML>',
            '<div class="included">  <h1>THIS IS FOLDER/5555555</h1>  <FOLDER>444 eqglp'
            ' 		44444</FOLDER></div><FOLDER>3 ERLPG ERGELR GQ Q QQ Q Q Q</FOLDER>',
            '<FOLDER>444 eqglp 		44444</FOLDER>',
            '<FOLDER>3 ERLPG ERGELR GQ Q QQ Q Q Q</FOLDER>',
        ]

        for new_file in jade_.JadeTemplateProcessor(files_to_jade).files:
            if new_file.string_version.replace('\n', '') in results_files:
                results_files.pop(results_files.index(new_file.string_version.replace('\n', '')))
        self.assertEqual([], results_files)
