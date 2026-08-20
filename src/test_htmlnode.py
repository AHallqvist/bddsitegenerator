import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a HTML node")
        node2 = HTMLNode("p", "This is a HTML node")
        self.assertEqual(node, node2)
    def test_not_eq_text(self):
        node = HTMLNode("p", "This is a HTML node")
        node2 = HTMLNode("p", "This is another HTML node")
        self.assertNotEqual(node, node2)
    def test_not_eq_type(self):
        node = HTMLNode("p", "This is a HTML node")
        node2 = HTMLNode("h1", "This is a HTML node")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()