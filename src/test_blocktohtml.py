import unittest
from blocktohtml import *


class TestBlockToHTML(unittest.TestCase):
    # test basic use case
    def test_single_line(self):
        text = "# test test"
        output = markdown_to_blocks(text)
        self.assertEqual(output, ["# test test"])

    def test_two_blocks(self):
        text="""# test test

paragraph 2"""
        output = markdown_to_blocks(text)
        self.assertEqual(output, ["# test test", "paragraph 2"])
    
    def test_multi_line_block(self):
        text = """* test1\n* test2\n* test3"""
        output = markdown_to_blocks(text)
        self.assertEqual(output, ["* test1\n* test2\n* test3"])


    def test_multi_block_w_multi_line(self):
        text = "* test1\n* test2\n* test3\n\nThis is a paragraph"
        output = markdown_to_blocks(text)
        self.assertEqual(output, ["* test1\n* test2\n* test3", "This is a paragraph"])

    def test_base_case(self):
        text = "# This is a heading\n\nThis is a paragraph. Has some **bold** and *italic*\n\n* test1\n* test2\n* test3"
        output = markdown_to_blocks(text)
        self.assertEqual(output, ["# This is a heading", "This is a paragraph. Has some **bold** and *italic*", "* test1\n* test2\n* test3"])

    def test_block_is_quote(self):
        block = "> test test"
        self.assertEqual(block_to_block_type(block), block_type_quote)

    def test_quote_symbol_not_at_start(self):
        block = "test test >"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_empty_block_raises_error(self):
        block = ""
        with self.assertRaises(Exception):
            block_to_block_type(block)

    def test_code_block(self):
        block = "``` test test test ```"
        self.assertEqual(block_to_block_type(block), block_type_code)

    def test_code_block_missing_end(self):
        block = "``` test test test"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_code_block_missing_start(self):
        block = "test test test ```"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_unordered_list_type(self):
        block1 = "* test test"
        block2 = "- test test"
        self.assertEqual(block_to_block_type(block1), block_type_unordered_list)
        self.assertEqual(block_to_block_type(block2), block_type_unordered_list)

    def test_unordered_list_missing_space(self):
        block1 = "*test test"
        block2 = "-test test"
        self.assertEqual(block_to_block_type(block1), block_type_paragraph)
        self.assertEqual(block_to_block_type(block2), block_type_paragraph)

    def test_unordered_list_symbols_not_in_order(self):
        block1 = "test *test"
        block2 = "test -test"
        self.assertEqual(block_to_block_type(block1), block_type_paragraph)
        self.assertEqual(block_to_block_type(block2), block_type_paragraph)

    def test_heading(self):
        block_h1 = "# test"
        block_h2 = "## test"
        block_h3 = "### test"
        block_h4 = "#### test"
        block_h5 = "##### test"
        block_h6 = "###### test"
        self.assertEqual(block_to_block_type(block_h1), block_type_heading)
        self.assertEqual(block_to_block_type(block_h2), block_type_heading)
        self.assertEqual(block_to_block_type(block_h3), block_type_heading)
        self.assertEqual(block_to_block_type(block_h4), block_type_heading)
        self.assertEqual(block_to_block_type(block_h5), block_type_heading)
        self.assertEqual(block_to_block_type(block_h6), block_type_heading)

    def test_bad_heading(self):
        block = "?### test"
        block2 = "###test"
        block3 = "test"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)
        self.assertEqual(block_to_block_type(block2), block_type_paragraph)
        self.assertEqual(block_to_block_type(block3), block_type_paragraph)

    def test_ordered_list(self):
        block = "1. test"
        block1 = "1. test\n2. test2"

        self.assertEqual(block_to_block_type(block), block_type_ordered_list)
        self.assertEqual(block_to_block_type(block1), block_type_ordered_list)

    def test_bad_ordered_list(self):
        block1 = "1.test"
        block2 = ".test"
        block3 = "test 1.test"
        block4 = "1. test\n2.test"
        block5 = "test 1. test"
        self.assertEqual(block_to_block_type(block1), block_type_paragraph)
        self.assertEqual(block_to_block_type(block2), block_type_paragraph)
        self.assertEqual(block_to_block_type(block3), block_type_paragraph)
        self.assertEqual(block_to_block_type(block4), block_type_paragraph)
        self.assertEqual(block_to_block_type(block5), block_type_paragraph)

