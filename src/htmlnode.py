from types import NotImplementedType


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        output = ""
        for k, v in props:
            output += f" {k} {v}"

    def __repr__(self):
        return f"HTMLNode("


