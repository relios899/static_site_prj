import unittest

from textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)
    def test_url(self):
        node = TextNode("This is a node", "bold", "test.com")
        node2 = TextNode("This is a node", "bold", "test.com")
        assert node.url == "test.com"
        assert node2.url == "test.com"
    def test_convert_text(self):
        node = TextNode("test", "text")
        self.assertEqual(str(text_node_to_html_node(node)), """HTMLNode(None, test, None, None)""")
    def test_convert_bold(self):
        node = TextNode("test", "bold")
        self.assertEqual(str(text_node_to_html_node(node)), """HTMLNode(b, test, None, None)""")
    def test_convert_italic(self):
        node = TextNode("test", "italic")
        self.assertEqual(str(text_node_to_html_node(node)), """HTMLNode(i, test, None, None)""")
    def test_convert_code(self):
        node = TextNode("test", "code")
        self.assertEqual(str(text_node_to_html_node(node)), """HTMLNode(code, test, None, None)""")
    def test_convert_link(self):
        node = TextNode("test", "link", "test.com")
        self.assertEqual(str(text_node_to_html_node(node)), """HTMLNode(a, test, None, {'href': 'test.com'})""")
    def test_convert_image(self):
        node = TextNode("test", "image", "test.com")
        self.assertEqual(str(text_node_to_html_node(node)), """HTMLNode(img, , None, {'src': 'test.com', 'alt': 'test'})""")
    def test_bad_type(self):
        node = TextNode("test", "notatype")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
