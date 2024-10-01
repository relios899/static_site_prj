import unittest

from textnode import TextNode


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

if __name__ == "__main__":
    unittest.main()
