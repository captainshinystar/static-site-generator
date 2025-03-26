class HTMLNode: # represents a node in an HTML doc tree (like a <p> tag and its contents)
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        props_html = ""
        for item in self.props:
            props_html += f' {item}="{self.props[item]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode): #must have a value, cannot have children, tag can be None
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode requires a value, but none was provided")
        super().__init__(tag, value, None, props)
        self.children = []
        
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a value, but none was provided")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode): # cannot have value, must have tag and children
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must contain a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"