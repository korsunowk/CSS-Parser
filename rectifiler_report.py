import sys
import subprocess
import jinja2
import os
import rectifiler

BASEDIR = os.path.dirname(
        os.path.realpath(sys.argv[0])
    )

try:
    report_path = os.path.realpath(sys.argv[sys.argv.index('--report') + 1])
except Exception:
    report_path = os.getcwd()
    pass


class RectifilerReport:
    def __init__(self, **kwargs):
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(BASEDIR))
        try:
            self.template = self.env.get_template('report_template.html').render(
                {
                    'percent': kwargs['percent'],
                    'selectors': kwargs['selectors'],
                    'html': kwargs['html'],
                    'html_files': kwargs['html_files']
                }
            )
            self.create_report()
        except jinja2.TemplateNotFound:
            print('Template not found. Programm close.')
            exit()

    def create_report(self):
        name_report_file = report_path + '/' + 'Report file from CSS Rectifiler.html'
        with open(name_report_file, 'w+') as report_file:
            report_file.write(self.template)
            self.open_file(name_report_file)

    @staticmethod
    def open_file(filename):
        if sys.platform == "win32":
            os.startfile(filename)
            pass
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])
