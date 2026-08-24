import unittest

from split_nodes_delimiter import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodesImageLink(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_image_keeps_non_text_nodes(self):
        nodes = [
            TextNode("![image](https://example.com/a.png)", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/a.png"),
                TextNode("already bold", TextType.BOLD),
            ],
            split_nodes_image(nodes),
        )

    def test_split_link_keeps_non_text_nodes(self):
        nodes = [
            TextNode("[one](https://example.com)", TextType.TEXT),
            TextNode("already code", TextType.CODE),
        ]
        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "https://example.com"),
                TextNode("already code", TextType.CODE),
            ],
            split_nodes_link(nodes),
        )

    def test_split_image_no_match_returns_original_text_node(self):
        nodes = [TextNode("plain text", TextType.TEXT)]
        self.assertListEqual(nodes, split_nodes_image(nodes))

    def test_split_link_no_match_returns_original_text_node(self):
        nodes = [TextNode("plain text", TextType.TEXT)]
        self.assertListEqual(nodes, split_nodes_link(nodes))

    def test_split_image_with_text_before_and_after(self):
        node = TextNode("a ![img](https://x.com/y.png) z", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://x.com/y.png"),
                TextNode(" z", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_link_with_text_before_and_after(self):
        node = TextNode("a [site](https://x.com) z", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://x.com"),
                TextNode(" z", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_image_multiple_nodes(self):
        nodes = [
            TextNode("first ![a](https://a.com/a.png)", TextType.TEXT),
            TextNode("second ![b](https://b.com/b.png)", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("first ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "https://a.com/a.png"),
                TextNode("second ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "https://b.com/b.png"),
            ],
            split_nodes_image(nodes),
        )

    def test_split_link_multiple_nodes(self):
        nodes = [
            TextNode("first [a](https://a.com)", TextType.TEXT),
            TextNode("second [b](https://b.com)", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("first ", TextType.TEXT),
                TextNode("a", TextType.LINK, "https://a.com"),
                TextNode("second ", TextType.TEXT),
                TextNode("b", TextType.LINK, "https://b.com"),
            ],
            split_nodes_link(nodes),
        )

    def test_split_link_ignores_image_markdown(self):
        node = TextNode("![img](https://x.com/y.png) and [site](https://x.com)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("![img](https://x.com/y.png) and ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://x.com"),
            ],
            split_nodes_link([node]),
        )

    def test_split_image_with_empty_alt_text(self):
        node = TextNode("photo ![](https://x.com/y.png)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("photo ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://x.com/y.png"),
            ],
            split_nodes_image([node]),
        )


if __name__ == "__main__":
    unittest.main()
