import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_eq(self):
        node = HTMLNode(props = {"href":"www.google.com"})
        self.assertEqual(node.props_to_html(), ' href: "www.google.com"')
    
    
    def test_props_not_eq(self):
        node = HTMLNode(props = {"href":"www.google.com"})
        self.assertNotEqual(node.props_to_html(), ' href: "www.cheg.com"')
    
    def test_mult_props_eq(self):
        node = HTMLNode(props = {"href":"www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href: "www.google.com" target: "_blank"')
    
    def test_mult_props_not_eq(self):
        node = HTMLNode(props = {"href":"www.google.com", "target": "_blank"})
        self.assertNotEqual(node.props_to_html(), ' href: "www.boot.dev" target: "_blank"')

    def test_leaf_node(self):
        node = LeafNode("p", "I am a paragraph")
        self.assertEqual(node.to_html(), "<p>I am a paragraph</p>")

    def test_leaf_node_empty(self):
        node = LeafNode(value="I am plain text")
        self.assertEqual(node.to_html(), "I am plain text")


if __name__ == "__main__":
    unittest.main()