import unittest
from generate_html_from_md import *

class TestGenerateHTMLFromMD(unittest.TestCase):
    def test_determine_type_header_tag(self):
        text1 = "# test"
        text2 = "## test"
        text3 = "### test"
        text4 = "#### test"
        text5 = "##### test"
        text6 = "###### test"
        self.assertEqual(determine_type_of_header_tag(text1), "h1")
        self.assertEqual(determine_type_of_header_tag(text2), "h2")
        self.assertEqual(determine_type_of_header_tag(text3), "h3")
        self.assertEqual(determine_type_of_header_tag(text4), "h4")
        self.assertEqual(determine_type_of_header_tag(text5), "h5")
        self.assertEqual(determine_type_of_header_tag(text6), "h6")
    
    def test_strip_tag_from_md_header(self):
        text = "#### test test"
        output = strip_md_block_id_from_text(text, block_type_heading)
        self.assertEqual(output, "test test")

    def test_generation_w_heading(self):
        text = "### test test"
        output = markdown_to_html_node(text)

        self.assertEqual(output.to_html(), """<div><h3>test test</h3></div>""")

    def test_generation_w_paragraph(self):
        text = "Test test test"
        output = markdown_to_html_node(text)
        self.assertEqual(output.to_html(), """<div><p>Test test test</p></div>""")

    def test_generation_w_code(self):
        text = "```test test test```"
        output = markdown_to_html_node(text)
        self.assertEqual(output.to_html(), """<div><code>test test test</code></div>""")

    def test_generation_w_quote(self):
        text = ">test test"
        output = markdown_to_html_node(text)
        self.assertEqual(output.to_html(), """<div><blockquote>test test</blockquote></div>""")

    def test_generation_unordered_list(self):
        text = "- test\n- test2\n- test3"
        text2 = "* test\n* test2\n* test3"
        output = markdown_to_html_node(text)
        self.assertEqual(output.to_html(), """<div><ul><li>test</li><li>test2</li><li>test3</li></ul></div>""")
        output = markdown_to_html_node(text2)
        self.assertEqual(output.to_html(), """<div><ul><li>test</li><li>test2</li><li>test3</li></ul></div>""")
        
    def test_generation_ordered_list(self):
        text = "1. test\n2. test2\n3. test3"
        output = markdown_to_html_node(text)
        self.assertEqual(output.to_html(), """<div><ol><li>test</li><li>test2</li><li>test3</li></ol></div>""")

