import unittest


class TestAloneSelectors(unittest.TestCase):
    def test_pseudo(self):
        import css_selectors
        self.assertTrue(css_selectors.AloneCSSSelector('.test_class:hover').has_pseudo())
        self.assertTrue(css_selectors.AloneCSSSelector('#test_id::moz-placeholder').has_pseudo())
        self.assertFalse(css_selectors.AloneCSSSelector('#test_id').has_pseudo())


class TestCSSSelector(unittest.TestCase):
    def test_combo_selectors(self):
        import css_selectors
        import files

        def check_alone_selectors(test_css_selector, test_selectors):
            test_css_selector.parsing_alone_selectors()
            for alone_selector in test_css_selector.alone_selectors:
                if alone_selector.name in test_selectors:
                    test_selectors.pop(
                        test_selectors.index(alone_selector.name)
                    )

            return [] == test_selectors

        self.assertTrue(check_alone_selectors(css_selectors.CSSSelector(
            '.class #id a:hover>.div + a.class',
            files.CSSFile('/path/css.css', 'minified')
        ), '.class ¿ #id ¿ a:hover > .div + a.class'.split()))

        self.assertTrue(check_alone_selectors(css_selectors.CSSSelector(
            '.class > div:first-child + a#id.class:focus, .class2 .class3 p > img.image',
            files.CSSFile('/path/css.css', 'minified')
        ), '.class > div:first-child + a#id.class:focus , .class2 ¿ .class3 p > img.image'.split()))
