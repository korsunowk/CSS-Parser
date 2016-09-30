class AbstractTemplate:
    def __init__(self, files):
        self.files = files
        self.do_template_processor()

    def do_template_processor(self):
        pass

    def get_file_to_include(self, name_of_file):
        for file in self.files:
            if file.path == name_of_file:
                return file
        print('Included file %s does not exist.' % name_of_file)
        exit()

    def include(self, file):
        pass

    @staticmethod
    def path_generator(file_path, path):
        from pathlib import Path
        import os
        return Path(os.path.dirname(file_path)).glob(path)
