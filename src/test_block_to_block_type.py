import unittest

from block_to_block_type import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_level_1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_level_6(self):
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_invalid_heading_without_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("##Heading"), BlockType.PARAGRAPH)

    def test_code_block_multiline(self):
        block = "```\ncode line 1\ncode line 2\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_unclosed_code_block_is_paragraph(self):
        block = "```\ncode line 1\ncode line 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block_multiline(self):
        block = ">quote one\n> quote two"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_with_non_quote_line_is_paragraph(self):
        block = ">quote\nnot quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- one\n- two\n- three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_with_bad_line_is_paragraph(self):
        block = "- one\ntwo"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start_is_paragraph(self):
        block = "2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_increment_is_paragraph(self):
        block = "1. one\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_fallback(self):
        block = "This is a normal paragraph with **inline** markdown."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
