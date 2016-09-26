# CSS-Rectifier
Python script for parsing css and html files.

Скрипт написанный языком Python 3.4, который выполняет поиск всех css и html файлов в выбранной директории (поиск проводится также в субдиректориях выбранной папки) и отслеживает на используемость каждого css-стиля в файлах html. 

Требования : 

1. Python 3.x

2. jinja2

3. pyjade

Возможности : 

1. Поиск любых css селекторов в html. 

2. Вывод неиспользуемых либо неправильно записанных селекторов.

3. Проверка каждого html файла на соотношение закрытых тегов к открытым.

4. Наличие конфигурационного файла для игнорирования определенных css файлов или директорий (node_modules).

5. Наличие опций при запуске скрипта (--path full/path/to/project/). Если путь не указан скрипт будет отрабатывать в директории из которой был вызван скрипт.

6. Вычисление % используемости всех css селекторов.

7. Минификация всех css файлов (включая удаление комментариев).

8. Возможность получить информацию по всем селекторам (в каком файле находится и номер строки в файле).

9. Если селектор описан не правильно и лишь часть его правильно описана, существует возможность узнать в каком файле html существует селектор, который правильно описан (работает только для id и class).

10. Создание отчета по неиспользуемым селекторам в виде html страницы.

11. Возможность указать в каком виде нужно вывести данные: список, либо отчет.

12. Добавлена опция --report path, с помощью которой скрипт создаст файл отчета в <path>, если <path> не задан, тогда файл отчета будет создан в папке вызова скрипта.

13. Добавлена опция --template name_of_template_processor, с помощью которой скрипт соеденит воедино нужные шаблоны по заданному шаблонизатору.

14. Добавлена возможность парсинга html страниц использующих шаблонизатор jinja2.

15. Добавлена возможность парсинга html страниц использующих шаблонизатор jade.

16. Добавлена возможность парсинга html страниц использующих шаблонизатор JSP.



# CSS-Rectifier
Python script for parsing css and html files.

The script written by Python language 3.4, which finds all the css and html files in the selected directory (the search is also made in the sub-folders of the selected folders) and tracks on the usability of each css-style in html files.

Requirements:

1. Python 3.x

2. jinja2

3. pyjade

Capabilities :

1. Search for any css selectors to html.

2. Conclusion of unused or improperly recorded selectors.

3. Check each html file on the ratio of the closed to the open tag.

4. The presence of the configuration file to ignore certain css files or directories (node_modules).

5. Available options when you run the script (--path full / path / to / project /). If not specified the script will work in a directory from which the script was called.

6. Calculation% usage of css selectors.

7. Minification all css files (including the removal of comments).

8. Ability to obtain information on all the selectors (where the file is located and the line number in the file).

9. If the selector is not properly described, and only part of it properly described, it is possible to know which file in html there selector, which correctly described (only works for id and class).

10. Create a report on unused selectors in an html page.

11. Ability to specify the need to display data in any form: a list or report.

12. Added option --report path, through which the script creates a log file in <path>, if <path> is not specified, then the log file will be created in the folder of the script call.

13. Added option --template name_of_template_processor, by which script string any together the desired patterns for a given template engine.

14. Added the ability to parse html pages using the template jinja2.

15. Added the ability to parse html pages using the template jade.

16. Added the ability to parse html pages using the JSP template.
