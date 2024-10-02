import unittest

from markdown_blocks import (
    block_to_block_type,
    code_type,
    extarct_title,
    heading_type,
    markdown_to_blocks,
    markdown_to_html_node,
    ordered_list_type,
    paragraph_type,
    quote_type,
    unordered_list_type,
)

markdown = """ 
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.


              


* This is the first list item in a list block
* This is a list item
* This is another list item





This is another paragrapgh



"""


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        result = markdown_to_blocks(markdown)
        expected = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            """* This is the first list item in a list block\n* This is a list item\n* This is another list item""",
            'This is another paragrapgh',
        ]
        self.assertEqual(result, expected)

    def test_block_to_block_type_heading(self):
        block = '#### Heading Example'
        result = block_to_block_type(block)
        expected = heading_type
        self.assertEqual(result, expected)

    def test_block_to_block_type_code(self):
        block = '``` Code Example\n```'
        result = block_to_block_type(block)
        expected = code_type
        self.assertEqual(result, expected)

    def test_block_to_block_type_quote(self):
        block = '> Quote Example\n> Second Line\n> Third Line'
        result = block_to_block_type(block)
        expected = quote_type
        self.assertEqual(result, expected)

    def test_block_to_block_type_unordered_list(self):
        block = '* Unordered Example\n* Second Line\n* Third Line'
        result = block_to_block_type(block)
        expected = unordered_list_type
        self.assertEqual(result, expected)

    def test_block_to_block_type_ordered_list(self):
        block = '1. Ordered Example\n2. Second Line\n3. Third Line'
        result = block_to_block_type(block)
        expected = ordered_list_type
        self.assertEqual(result, expected)

    def test_block_to_block_type_ordered_list_bad(self):
        block = '1. Ordered Example\n2. Second Line\n3.Third Line'
        result = block_to_block_type(block)
        expected = paragraph_type
        self.assertEqual(result, expected)

    def test_markdown_to_html_node(self):
        result = markdown_to_html_node(markdown)
        html_expected = '<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul><p>This is another paragrapgh</p></div>'
        self.assertEqual(result.to_html(), html_expected)

    def test_markdown_to_html_node_paragrapgh(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""
        result = markdown_to_html_node(md)
        expected = '<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>'
        self.assertEqual(result.to_html(), expected)

    def test_extract_title(self):
        result = extarct_title(markdown)
        assert result == 'This is a heading'
        md = """
### This is an h3
"""
        with self.assertRaises(Exception):
            extarct_title(md)
        md = """
### H3

# H1   
"""
        self.assertEqual(extarct_title(md), 'H1')
