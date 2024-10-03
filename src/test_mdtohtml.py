import re
import unittest
from mdtohtml import *
from textnode import TextNode

class TestMDToHTML(unittest.TestCase):

    # test bad syntax
    def test_bad_md_syntax(self):
        node = TextNode("This is bad *syntax", "text")
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", "bold")

    # test delim string at start
    def test_delim_str_at_start(self):
        node = TextNode("*title title* at beginning", "text")
        new_nodes = split_nodes_delimiter([node], "*", "bold")
        self.assertEqual(new_nodes[0], TextNode("title title", "bold", None))
        self.assertEqual(new_nodes[1], TextNode(" at beginning", "text", None))

    # test delim string at end
    def test_delim_str_at_end(self):
        node = TextNode("at the end *title title*", "text")
        new_nodes = split_nodes_delimiter([node], "*", "bold")
        self.assertEqual(new_nodes[0], TextNode("at the end ", "text", None))
        self.assertEqual(new_nodes[1], TextNode("title title", "bold", None))

    # test delim string in middle
    def test_delim_in_middle(self):
        node = TextNode("the delim is **middle** in the string", "text")
        new_nodes = split_nodes_delimiter([node], "**", "italic")
        self.assertEqual(new_nodes[0], TextNode("the delim is ", "text", None))
        self.assertEqual(new_nodes[1], TextNode("middle", "italic", None))
        self.assertEqual(new_nodes[2], TextNode(" in the string", "text", None))

    # test when node is just text
    def test_node_just_text(self):
        node = TextNode("test test", "text")
        new_nodes = split_nodes_delimiter([node], "*", "bold")
        self.assertEqual(new_nodes[0], TextNode("test test", "text", None))
        self.assertEqual(len(new_nodes), 1)

    def test_both_bold_and_italics(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("italic", text_type_italic),
            ],
            new_nodes,
        )

    # test when there is both text and non-text
    def test_text_and_non_text(self):
        nodes = [TextNode("test test", "text"), TextNode("non text *text* here", "text", None)]
        new_nodes = split_nodes_delimiter(nodes, "*", "bold")
        self.assertEqual(new_nodes[0], TextNode("test test", "text", None))
        self.assertEqual(new_nodes[1], TextNode("non text ", "text", None))
        self.assertEqual(new_nodes[2], TextNode("text", "bold", None))
        self.assertEqual(new_nodes[3], TextNode(" here", "text", None))

    def test_delimiter_split(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", "text", None))
        self.assertEqual(new_nodes[1], TextNode("code block", "code", None))
        self.assertEqual(new_nodes[2], TextNode(" word", "text", None))
    # test just image
    def test_just_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"   
        self.assertEqual(extract_markdown_image(text),[("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_just_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_link(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    def test_link_in_front(self):
        text = "[test](www.test.com) test test"
        self.assertEqual(extract_markdown_link(text), [("test", "www.test.com")])

    # test neither
    def test_neither(self):
        text = "test test test"
        self.assertEqual(extract_markdown_link(text), [])
        self.assertEqual(extract_markdown_image(text),[])

    # test with both
    def test_both(self):
        text = "test test ![test](www.test.com) and [test2](www.test2.com) test test"
        self.assertEqual(extract_markdown_image(text), [("test", "www.test.com")])
        self.assertEqual(extract_markdown_link(text), [("test2", "www.test2.com")])


    # test single image at start
    def test_single_img_start(self):
        node = TextNode("![test](www.test.com) test test", text_type_text)
        self.assertEqual(split_nodes_image([node]), [TextNode("test", "image", "www.test.com"), TextNode(" test test", "text")])

    # test single image at end
    def test_single_img_end(self):
        node = TextNode("test test ![test](www.test.com)", text_type_text)
        self.assertEqual(split_nodes_image([node]), [TextNode("test test ", "text"), TextNode("test", "image", "www.test.com")])

    # test multiple images
    def test_no_images(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", "text")
        self.assertEqual(split_nodes_image([node]), [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", "text")])

    # test no images
    def test_multiple_images(self):
        node = TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", "text")
        self.assertEqual(split_nodes_image([node]), [
                         TextNode("This is text with a link ", text_type_text),
                         TextNode("to boot dev", "image" , "https://www.boot.dev"), 
                         TextNode(" and ", text_type_text),
                         TextNode("to youtube", "image", "https://www.youtube.com/@bootdotdev")
        ])
    # test text after images
    def test_text_after_images(self):
        node = TextNode("![test](www.test.com) test test", "text")
        self.assertEqual(split_nodes_image([node]), [
                        TextNode("test", "image", "www.test.com"),
                        TextNode(" test test", "text")
        ])
                        
    def test_single_link_start(self):
        node = TextNode("[test](www.test.com) test test", text_type_text)
        self.assertEqual(split_nodes_link([node]), [TextNode("test", "link", "www.test.com"), TextNode(" test test", "text")])

    # test single image at end
    def test_single_link_end(self):
        node = TextNode("test test [test](www.test.com)", text_type_text)
        self.assertEqual(split_nodes_link([node]), [TextNode("test test ", "text"), TextNode("test", "link", "www.test.com")])

    # test multiple images
    def test_no_link(self):
        node = TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", "text")
        self.assertEqual(split_nodes_link([node]), [TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", "text")])

    # test no images
    def test_multiple_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", "text")
        self.assertEqual(split_nodes_link([node]), [
                         TextNode("This is text with a link ", text_type_text),
                         TextNode("to boot dev", "link" , "https://www.boot.dev"), 
                         TextNode(" and ", text_type_text),
                         TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev")
        ])
    # test text after images
    def test_text_after_link(self):
        node = TextNode("[test](www.test.com) test test", "text")
        self.assertEqual(split_nodes_link([node]), [
                        TextNode("test", "link", "www.test.com"),
                        TextNode(" test test", "text")
        ])

    def test_text_to_textnodes(self):
        output = text_to_textnodes("""This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)""")
        self.assertEqual(output, [
    TextNode("This is ", text_type_text),
    TextNode("text", text_type_bold),
    TextNode(" with an ", text_type_text),
    TextNode("italic", text_type_italic),
    TextNode(" word and a ", text_type_text),
    TextNode("code block", text_type_code),
    TextNode(" and an ", text_type_text),
    TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", text_type_text),
    TextNode("link", text_type_link, "https://boot.dev"),
])
