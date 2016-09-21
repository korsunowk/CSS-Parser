import unittest


class TestJinja2Processor(unittest.TestCase):
    def test_includes(self):
        import templanisator.jinja_template as jinja_

        jinja_.Jinja2TemplateProcessor().do_template_processor(
            []
        )
