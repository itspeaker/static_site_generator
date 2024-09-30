import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        propis = {'href': 'https://www.google.com', 'target': '_blank'}
        node = HTMLNode(tag='a', value='a text', props=propis)
        propis_text = node.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(propis_text, expected)

    def test_empty_props_to_html(self):
        node = HTMLNode(tag='a', value='a text')
        result = node.props_to_html()
        self.assertEqual(result, '')


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        leaf = LeafNode(tag='a', value='Click me!', props={'href': 'https://www.google.com'})
        self.assertEqual(leaf.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        leaf = LeafNode(value='Click me!', props={'href': 'https://www.google.com'})
        self.assertEqual(leaf.to_html(), 'Click me!')

    def test_leaf_to_html_no_value(self):
        leaf = LeafNode(props={'href': 'https://www.google.com'})
        with self.assertRaises(ValueError):
            leaf.to_html()

    def test_text_node_to_leaf_node_type_text(self):
        text_node = TextNode('Some text', 'text')
        leaf = LeafNode(value='Some text')
        self.assertEqual(text_node_to_html_node(text_node).to_html(), leaf.to_html())

    def test_text_node_to_leaf_node_type_bold(self):
        text_node = TextNode('Some text', 'bold')
        leaf = LeafNode('b', 'Some text')
        self.assertEqual(text_node_to_html_node(text_node).to_html(), leaf.to_html())

    def test_text_node_to_leaf_node_type_italic(self):
        text_node = TextNode('Some text', 'italic')
        leaf = LeafNode('i', 'Some text')
        self.assertEqual(text_node_to_html_node(text_node).to_html(), leaf.to_html())

    def test_text_node_to_leaf_node_type_code(self):
        text_node = TextNode('Some code', 'code')
        leaf = LeafNode('code', 'Some code')
        self.assertEqual(text_node_to_html_node(text_node).to_html(), leaf.to_html())

    def test_text_node_to_leaf_node_type_link(self):
        text_node = TextNode('Some text', 'link', 'www.url.com')
        leaf = LeafNode('a', 'Some text', {'href': 'www.url.com'})
        self.assertEqual(text_node_to_html_node(text_node).to_html(), leaf.to_html())

    def test_text_node_to_leaf_node_type_image(self):
        text_node = TextNode('Some text', 'image', 'www.url.com')
        leaf = LeafNode('img', '', {'alt': 'Some text', 'src': 'www.url.com'})
        self.assertEqual(text_node_to_html_node(text_node).to_html(), leaf.to_html())


class TestParentNode(unittest.TestCase):
    def test_parent_node_leaf_children(self):
        node = ParentNode(
            tag='p',
            children=[
                LeafNode(tag='b', value='Bold text'),
                LeafNode(value='Normal text'),
                LeafNode(tag='i', value='italic text'),
                LeafNode(value='Normal text'),
            ],
        )

        self.assertEqual(
            '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>',
            node.to_html(),
        )

    def test_parent_node_with_parent_children(self):
        node = ParentNode(
            tag='p',
            children=[
                ParentNode(
                    tag='p',
                    children=[
                        LeafNode(tag='b', value='Bold text'),
                        LeafNode(value='Normal text'),
                    ],
                ),
                LeafNode(tag='b', value='Bold text'),
                LeafNode(value='Normal text'),
            ],
        )

        self.assertEqual(
            '<p><p><b>Bold text</b>Normal text</p><b>Bold text</b>Normal text</p>',
            node.to_html(),
        )

    def test_parent_node_with_parent_children_no_tag(self):
        node = ParentNode(
            tag='p',
            children=[
                ParentNode(
                    children=[
                        LeafNode(tag='b', value='Bold text'),
                        LeafNode(value='Normal text'),
                    ],
                ),
                LeafNode(tag='b', value='Bold text'),
                LeafNode(value='Normal text'),
            ],
        )

        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_with_parent_children_no_children(self):
        node = ParentNode(
            tag='p',
        )

        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == '__main__':
    unittest.main()
