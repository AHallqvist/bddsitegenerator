import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_single_line(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_multiline_document(self):
        md = """Some intro text

# My Page Title

More text here
"""
        self.assertEqual(extract_title(md), "My Page Title")

    def test_extract_title_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_extract_title_ignores_h2(self):
        md = """## Not H1

# Real H1
"""
        self.assertEqual(extract_title(md), "Real H1")

    def test_extract_title_raises_when_missing_h1(self):
        md = """No title here

## Only H2

Paragraph text
"""
        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
