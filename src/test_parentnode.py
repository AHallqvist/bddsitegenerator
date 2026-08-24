import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_raises_without_tag(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_raises_without_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_empty_children(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_with_props(self):
        node = ParentNode("section", [LeafNode("p", "hello")], {"class": "hero"})
        self.assertEqual(node.to_html(), '<section class="hero"><p>hello</p></section>')

    def test_to_html_with_deep_nesting(self):
        level3 = LeafNode("em", "deep")
        level2 = ParentNode("span", [level3])
        level1 = ParentNode("div", [level2])
        root = ParentNode("article", [level1])
        self.assertEqual(
            root.to_html(),
            "<article><div><span><em>deep</em></span></div></article>",
        )

    def test_to_html_preserves_child_order(self):
        node = ParentNode(
            "div",
            [
                LeafNode("span", "first"),
                LeafNode("span", "second"),
                LeafNode("span", "third"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><span>first</span><span>second</span><span>third</span></div>",
        )

    def test_nested_parent_siblings(self):
        left = ParentNode("li", [LeafNode(None, "A")])
        right = ParentNode("li", [LeafNode(None, "B")])
        node = ParentNode("ul", [left, right])
        self.assertEqual(node.to_html(), "<ul><li>A</li><li>B</li></ul>")


if __name__ == "__main__":
    unittest.main()
