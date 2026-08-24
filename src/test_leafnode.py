import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Page Title")
        self.assertEqual(node.to_html(), "<h1>Page Title</h1>")

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "inline text")
        self.assertEqual(node.to_html(), "<span>inline text</span>")

    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "bold text")
        self.assertEqual(node.to_html(), "<b>bold text</b>")

    def test_leaf_to_html_italic(self):
        node = LeafNode("i", "italic text")
        self.assertEqual(node.to_html(), "<i>italic text</i>")

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "print('hello')")
        self.assertEqual(node.to_html(), "<code>print('hello')</code>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "boot.dev", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">boot.dev</a>')

    def test_leaf_to_html_raw_text_when_no_tag(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")

    def test_leaf_to_html_raises_when_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr_excludes_children(self):
        node = LeafNode("p", "hello", {"class": "intro"})
        self.assertEqual(node.__repr__(), 'LeafNode("p","hello","{\'class\': \'intro\'}")')


if __name__ == "__main__":
    unittest.main()
