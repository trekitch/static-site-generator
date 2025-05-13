import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_eq(self):
        node = HTMLNode(props = {"href":"www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="www.google.com"')
    
    
    def test_props_not_eq(self):
        node = HTMLNode(props = {"href":"www.google.com"})
        self.assertNotEqual(node.props_to_html(), ' href="www.cheg.com"')
    
    def test_mult_props_eq(self):
        node = HTMLNode(props = {"href":"www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="www.google.com" target="_blank"')
    
    def test_mult_props_not_eq(self):
        node = HTMLNode(props = {"href":"www.google.com", "target": "_blank"})
        self.assertNotEqual(node.props_to_html(), ' href="www.boot.dev" target="_blank"')

    def test_leaf_node(self):
        node = LeafNode("p", "I am a paragraph")
        self.assertEqual(node.to_html(), "<p>I am a paragraph</p>")

    def test_leaf_node_empty(self):
        node = LeafNode(None, "I am plain text")
        self.assertEqual(node.to_html(), "I am plain text")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )        


if __name__ == "__main__":
    unittest.main()