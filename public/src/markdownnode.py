import re
from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING =  "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    cleaned_blocks = []
    blocks = markdown.strip().split("\n\n")  # Split by double line breaks (paragraphs)

    for block in blocks:
        if block == "":
            continue
        # Clean up leading/trailing spaces from each line inside the block
        lines = [line.strip() for line in block.strip().split("\n")]
        cleaned_block = "\n".join(lines)
        cleaned_blocks.append(cleaned_block)

    return cleaned_blocks

def block_to_block_type(text):
    lines = text.split("\n")
    if text.startswith("```") and text.endswith("```"):
        return BlockType.CODE
    if re.search(r"^#{1,6} .+", text):
        return BlockType.HEADING
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    if all(line.startswith(f"{idx}. ") for idx, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return create_paragraph_node(block)
    if block_type == BlockType.HEADING:
        return create_heading_node(block)
    if block_type == BlockType.CODE:
        return create_code_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return create_ordered_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return create_unordered_node(block)
    if block_type == BlockType.QUOTE:
        return create_quote_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def create_heading_node(block):
    heading_level = 0
    for char in block:
        if char == "#":
            heading_level += 1
        else:
            break
    if heading_level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {heading_level}")
    text = block[heading_level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{heading_level}", children)

def create_code_node(block):
    if not block.startswith("```") or not block.startswith("```"):
        raise Exception("not a code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    children = text_node_to_html_node(raw_text_node)
    child = ParentNode("code", [children])
    return ParentNode("pre", [child])

def create_paragraph_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def create_unordered_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def create_ordered_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def create_quote_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)