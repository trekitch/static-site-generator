import re
from enum import Enum
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING =  "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        original_text = old_node.text
        if not extract_markdown_images(original_text):
            new_nodes.append(old_node)
            continue
        while extract_markdown_images(original_text):
            images = extract_markdown_images(original_text)
            img_alt = images[0][0]
            img_txt = images[0][1]
            sections = original_text.split(f"![{img_alt}]({img_txt})", 1)
            original_text = sections[1]
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_txt))
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes




def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        original_text = old_node.text
        if not extract_markdown_links(original_text):
            new_nodes.append(old_node)
            continue
        while extract_markdown_links(original_text):
            images = extract_markdown_links(original_text)
            link_txt = images[0][0]
            link_url = images[0][1]
            sections = original_text.split(f"[{link_txt}]({link_url})", 1)
            original_text = sections[1]
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_txt, TextType.LINK, link_url))
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

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
    
            


            
            
    


