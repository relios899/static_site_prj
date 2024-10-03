import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_no_value(self):
        node = LeafNode(None,None,None)
        with self.assertRaises(ValueError):
            node.to_html()
    def test_no_tag(self):
        node = LeafNode(None,"test test", None)
        self.assertEqual(node.to_html(), "test test")
    def test_html_no_props(self):
        node = LeafNode( "p","test",None)
        self.assertEqual(node.to_html(), "<p>test</p>")
    def test_html_w_props(self):
        node = LeafNode("a", "Click me!", {"href":"https://www.google.com"})
        self.assertEqual(node.to_html(), """<a href="https://www.google.com">Click me!</a>""")
