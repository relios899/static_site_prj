import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        self.assertIsNone(node.props)
    def test_props_to_html(self):
        props= {
            "href":"https://www.google.com",
            "target":"_blank"
        }
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), ''' href="https://www.google.com" target="_blank"''')
    def test_obj_print(self):
        node = HTMLNode("p","test",[],{})
        self.assertEqual(str(node),"HTMLNode(p, test, [], {})")

if __name__ == "__main__":
    unittest.main()
