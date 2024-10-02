import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node, text_to_textnodes

paragraph_type = 'paragraph'
heading_type = 'heading'
code_type = 'code'
quote_type = 'quote'
ordered_list_type = 'ordered_list'
unordered_list_type = 'unordered_list'


def text_to_children(text) -> list[HTMLNode]:
    children = text_to_textnodes(text)
    children_list = []
    for c in children:
        children_list.append(text_node_to_html_node(c))
    return children_list


def text_to_html(block, block_type):
    if block_type == paragraph_type:
        text = ' '.join(block.split('\n'))
        children_list = text_to_children(text)
        return ParentNode('p', children_list)
    if block_type == heading_type:
        count = 0
        while block[count] == '#':
            count += 1
        children_list = text_to_children(block[count + 1 :])
        if len(children_list) > 1:
            return ParentNode(f'h{count}', children_list)
        return LeafNode(f'h{count}', block[count + 1 :])
    if block_type == quote_type:
        children_list = text_to_children(block[2:])
        if len(children_list) > 1:
            return ParentNode('blockquote', children_list)
        return LeafNode('blockquote', block[2:])
    if block_type == code_type:
        children_list = text_to_children(block.strip('```'))
        if len(children_list) > 1:
            return ParentNode('pre', [ParentNode('code', children_list)])
        return ParentNode('pre', [LeafNode('code', block.strip('```'))])
    if block_type == unordered_list_type:
        items = block.split('\n')
        nodes = []
        for item in items:
            children_list = text_to_children(item[2:])
            if len(children_list) > 1:
                nodes.append(ParentNode('li', children_list))
            else:
                nodes.append(LeafNode('li', item[2:]))
        return ParentNode('ul', nodes)
    if block_type == ordered_list_type:
        items = block.split('\n')
        nodes = []
        for item in items:
            children_list = text_to_children(item[3:])
            if len(children_list) > 1:
                nodes.append(ParentNode('li', children_list))
            else:
                nodes.append(LeafNode('li', item[3:]))
        return ParentNode('ol', nodes)
    raise Exception('Invalid block type')


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_nodes.append(text_to_html(block, block_type))
    return ParentNode('div', html_nodes)


def markdown_to_blocks(markdown: str):
    blocks = markdown.split('\n\n')

    stripped = map(lambda x: x.strip(' ').strip('\n'), blocks)
    return list(filter(lambda x: x, stripped))


def block_to_block_type(block: str):
    if re.fullmatch(r'^[#]{1,6}', block.split()[0]):
        return heading_type
    if block.startswith('```') and block.endswith('```'):
        return code_type
    lines = block.split('\n')
    if lines[0].startswith('>'):
        for i in range(1, len(lines)):
            if not lines[i].startswith('>'):
                return paragraph_type
        return quote_type
    if lines[0].startswith('* ') or lines[0].startswith('- '):
        for i in range(1, len(lines)):
            if not lines[i].startswith('* ') and not lines[i].startswith('- '):
                return paragraph_type
        return unordered_list_type
    if lines[0].startswith('1. '):
        for i in range(1, len(lines)):
            if not lines[i].startswith(f'{i+1}. '):
                return paragraph_type
        return ordered_list_type
    return paragraph_type


def extarct_title(markdown: str):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == heading_type and block.startswith('# '):
            return block.strip('#').strip()
    raise Exception('No header in markdown')
