class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value,None, props)

    def to_html(self):
        value, tag, props = self.value, self.tag, self.props_to_html()
        if value is None:
            raise ValueError("All leaf nodes must have a value.")
        if tag is None:
            return value
        return f'<{tag}{props if props else ""}>{value}</{tag}>'
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Every parent must have a tag")
        if self.children is None :
            raise ValueError("All Parent node must have a child")
        
        children, tag, props = self.children, self.tag, self.props_to_html()

        def create_children(children):
            if len(children) == 0:
                raise ValueError('All Parent node must have a child')
            else:
                if len(children) == 1: 
                    if hasattr(children[0], 'create_children'): #this means the child is a parent
                        return create_children(children[0])
                    return children[0].to_html()
                else:
                    return f'{children[0].to_html()}{create_children(children[1:])}'
                
        return f'<{tag}{props if props else ""}>{create_children(children)}</{tag}>'
    
             
        
children =[]	
ParentNode('div',children)