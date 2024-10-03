import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        node = ParentNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_single_leaf(self):
        leaf_node = LeafNode("b", "Bold text", {})
        node = ParentNode("p", [leaf_node])
        self.assertEqual(node.to_html(),"""<p><b>Bold text</b></p>""")

    def test_multiple_leaf_nodes(self):
        leaf_nodes = [
            LeafNode("b", "Bold text", {}),
            LeafNode(None, "Normal text", {}),
            LeafNode("i", "italic text", {}),
            LeafNode(None, "Normal text", {}),
        ]
        node = ParentNode("p", leaf_nodes)
        self.assertEqual(node.to_html(), """<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>""")

    def test_one_parent_w_leaf(self):
        leaf_node = [LeafNode("b", "Bold text", {})]
        parent_node = ParentNode("p", leaf_node)
        node = ParentNode("p", [parent_node])
        self.assertEqual(node.to_html(), """<p><p><b>Bold text</b></p></p>""")


    def test_many_leaf_w_props(self):
        leaf_nodes = [
            LeafNode("b", "Bold text", {"href":"www.test.com"}),
        ]
        node = ParentNode("p", leaf_nodes)
        self.assertEqual(node.to_html(), """<p><b href="www.test.com">Bold text</b></p>""")
