import unittest

from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_full_mixed_markdown(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_plain_text(self):
        self.assertListEqual(
            [TextNode("just plain text", TextType.TEXT)],
            text_to_textnodes("just plain text"),
        )

    def test_only_image(self):
        text = "![cat](https://example.com/cat.png)"
        self.assertListEqual(
            [TextNode("cat", TextType.IMAGE, "https://example.com/cat.png")],
            text_to_textnodes(text),
        )

    def test_only_link(self):
        text = "[Boot.dev](https://boot.dev)"
        self.assertListEqual(
            [TextNode("Boot.dev", TextType.LINK, "https://boot.dev")],
            text_to_textnodes(text),
        )

    def test_multiple_same_delimiter_types(self):
        text = "**a** and **b** and _c_ and _d_"
        self.assertListEqual(
            [
                TextNode("a", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("c", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("d", TextType.ITALIC),
            ],
            text_to_textnodes(text),
        )

    def test_code_processed_before_bold_and_italic(self):
        text = "`**not bold**` and `_not italic_`"
        self.assertListEqual(
            [
                TextNode("**not bold**", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("_not italic_", TextType.CODE),
            ],
            text_to_textnodes(text),
        )

    def test_unclosed_bold_raises(self):
        with self.assertRaises(Exception):
            text_to_textnodes("This is **broken")

    def test_unclosed_code_raises(self):
        with self.assertRaises(Exception):
            text_to_textnodes("This is `broken")


if __name__ == "__main__":
    unittest.main()
