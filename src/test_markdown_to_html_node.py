import unittest

from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# Heading with **bold**"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><h1>Heading with <b>bold</b></h1></div>")

    def test_quote_block(self):
        md = "> first line\n> second line with _italic_"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>first line second line with <i>italic</i></blockquote></div>",
        )

    def test_unordered_list_block(self):
        md = "- one\n- two with `code`"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one</li><li>two with <code>code</code></li></ul></div>",
        )

    def test_ordered_list_block(self):
        md = "1. first\n2. second with [link](https://boot.dev)"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            '<div><ol><li>first</li><li>second with <a href="https://boot.dev">link</a></li></ol></div>',
        )

    def test_full_document(self):
        md = """# Title

Paragraph with ![img](https://example.com/img.png) and [link](https://boot.dev).

- Item one
- Item two

> quoted line
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            '<div><h1>Title</h1><p>Paragraph with <img src="https://example.com/img.png" alt="img"></img> and <a href="https://boot.dev">link</a>.</p><ul><li>Item one</li><li>Item two</li></ul><blockquote>quoted line</blockquote></div>',
        )


if __name__ == "__main__":
    unittest.main()
