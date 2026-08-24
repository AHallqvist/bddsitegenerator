import re

from block_to_block_type import BlockType, block_to_block_type
from leafnode import LeafNode
from markdown_to_blocks import markdown_to_blocks
from parentnode import ParentNode
from text_to_textnodes import text_to_textnodes
from textnode import text_node_to_html_node


def text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def paragraph_to_html_node(block):
    paragraph_text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(paragraph_text))


def heading_to_html_node(block):
    heading_level = len(block) - len(block.lstrip("#"))
    heading_text = block[heading_level + 1 :]
    return ParentNode(f"h{heading_level}", text_to_children(heading_text))


def code_to_html_node(block):
    code_text = block[4:-3]
    return ParentNode("pre", [LeafNode("code", code_text)])


def quote_to_html_node(block):
    lines = block.split("\n")
    quote_text = " ".join(line[1:].lstrip() for line in lines)
    return ParentNode("blockquote", text_to_children(quote_text))


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    list_items = [ParentNode("li", text_to_children(line[2:])) for line in lines]
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    list_items = []

    for line in lines:
        match = re.match(r"^\d+\. (.*)$", line)
        if not match:
            raise ValueError("Invalid ordered list item")
        list_items.append(ParentNode("li", text_to_children(match.group(1))))

    return ParentNode("ol", list_items)


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)

    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)

    if block_type == BlockType.CODE:
        return code_to_html_node(block)

    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)

    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)

    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)

    raise ValueError("Unknown block type")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
