from htmlnode import LeafNode
from inline_markdown import extract_markdown_images, extract_markdown_links


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, __value: object) -> bool:
        if (
            self.text == __value.text
            and self.text_type == __value.text_type
            and self.url == __value.url
        ):
            return True

        return False

    def __repr__(self) -> str:
        t = self.text
        ty = self.text_type
        u = self.url
        return f"TextNode({t}, {ty}, {u})"


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == text_type_text:
        return LeafNode(value=text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode(tag="b", value=text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode(tag="i", value=text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode(tag="code", value=text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode(
            tag="img", value="", props={"alt": text_node.text, "src": text_node.url}
        )
    raise Exception("Invalid text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new.append(node)
            continue

        texts = node.text.split(delimiter)
        if len(texts) % 2 == 0:
            raise Exception("Invalid markdown.")

        splitted_nodes = []
        for i in range(len(texts)):
            if not texts[i]:
                continue
            if i % 2 == 0:
                splitted_nodes.append(TextNode(texts[i], text_type_text))
            else:
                splitted_nodes.append(TextNode(texts[i], text_type))
        new.extend(splitted_nodes)

    return new


def split_nodes_image(old_nodes):
    new = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not len(images):
            new.append(node)
            continue
        to_split = node.text
        splitted_nodes = []
        for i in images:
            splitted = to_split.split(f"![{i[0]}]({i[1]})", 1)
            if splitted[0]:
                splitted_nodes.append(TextNode(splitted[0], text_type_text))
            splitted_nodes.append(TextNode(i[0], text_type_image, i[1]))

            to_split = splitted[1]

        if to_split:
            splitted_nodes.append(TextNode(to_split, text_type_text))
        new.extend(splitted_nodes)

    return new


def split_nodes_link(old_nodes):
    new = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not len(links):
            new.append(node)
            continue
        to_split = node.text
        splitted_nodes = []
        for i in links:
            splitted = to_split.split(f"[{i[0]}]({i[1]})", 1)
            if splitted[0]:
                splitted_nodes.append(TextNode(splitted[0], text_type_text))
            splitted_nodes.append(TextNode(i[0], text_type_link, i[1]))

            to_split = splitted[1]

        if to_split:
            splitted_nodes.append(TextNode(to_split, text_type_text))
        new.extend(splitted_nodes)
    return new


def text_to_textnodes(text):
    bold = split_nodes_delimiter([TextNode(text, text_type_text)], "**", text_type_bold)
    italic = split_nodes_delimiter(bold, "*", text_type_italic)
    code = split_nodes_delimiter(italic, "`", text_type_code)
    image = split_nodes_image(code)
    result = split_nodes_link(image)
    return result
