import unittest
from markdownnode import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        )


    def test_markdown_to_blocks_newlines(self):
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

    def test_block_to_block_type_heading(self):
        md = "# This is a heading"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.HEADING)

    def test_block_to_block_type_heading_2(self):
        md = "### This is a heading"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        md = "```This is code```"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        md = """>this is a quote\n>quote 2\n>quote 3"""
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.QUOTE)

    def test_block_to_block_type_ul(self):
        md = """- this is a quote\n- quote 2\n- quote 3"""
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ol(self):
        md = """1. this is a quote\n2. quote 2\n3. quote 3"""
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.ORDERED_LIST)

    def test_block_to_block_type_not_ol(self):
        md = """1. this is a quote\n1. quote 2\n3. quote 3"""
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.PARAGRAPH)

    def test_block_to_block_type_not_para(self):
        md = "This is a paragrapgh"
        block = block_to_block_type(md)
        self.assertEqual(block, BlockType.PARAGRAPH)


    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

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

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
        # this is an h1

        this is paragraph text

        ## this is an h2
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
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

        


if __name__ == "__main__":
    unittest.main()