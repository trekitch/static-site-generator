class HTMLNode:
    def __init__(self,tag = None,value = None,children= None,props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented.")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        ouput = ""
        for k, v in self.props.items():
            ouput += f' {k}: "{v}"'
        return ouput
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self,tag=None, value=None):
        super().__init__()
        self.tag = tag
        self.value = value
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}>{self.value}</{self.tag}>"

