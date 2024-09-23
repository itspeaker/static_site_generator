class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""
        if self.props is not None:
            for key, value in self.props.items():
                result += f' {key}="{value}"'
        return result

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}/{self.value}/{self.children}/{self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Not value provided to LeafNode")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag provided")
        if not self.children:
            raise ValueError("No children provided")
        children_string = ""
        for c in self.children:
            children_string += c.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
