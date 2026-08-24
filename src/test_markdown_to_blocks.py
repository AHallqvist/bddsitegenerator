import unittest

from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading_paragraph_list_blocks(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_strips_block_whitespace(self):
        md = """   first block   

   second block   """
        self.assertEqual(markdown_to_blocks(md), ["first block", "second block"])

    def test_removes_empty_blocks_from_extra_newlines(self):
        md = """first



second


third"""
        self.assertEqual(markdown_to_blocks(md), ["first", "second", "third"])

    def test_empty_markdown_returns_empty_list(self):
        self.assertEqual(markdown_to_blocks(""), [])


if __name__ == "__main__":
    unittest.main()
