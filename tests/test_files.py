import unittest
import files


class TestMyFile(unittest.TestCase):
    def test_object(self):
        test_my_file = files.MyFile('/path/to/css/file/my.file')
        self.assertEqual(test_my_file.path, '/path/to/css/file/my.file')
        self.assertEqual(test_my_file.name, 'my.file')
        self.assertEqual(test_my_file.extention, 'file')


class TestWEBFile(unittest.TestCase):
    def test_check_tags(self):
        test_web_file = files.WEBFile()
        with open('report_template.html', 'r+') as file:
            test_web_file.check_tags(
                file.read()
            )
        self.assertTrue(test_web_file.opened_and_closed_tags_check)
