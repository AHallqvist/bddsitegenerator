import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("\n```"):
        return BlockType.CODE

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    ordered_list_match = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            ordered_list_match = False
            break

    if ordered_list_match:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
