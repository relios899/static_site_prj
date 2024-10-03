from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children):
        super().__init__(tag, None, children, None)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag cannot be none")
        if self.children is None:
            raise ValueError("children variable cannot be none")
        res = f"<{self.tag}>"
        for child in self.children:
            res += child.to_html()
        return f"{res}</{self.tag}>"
        
