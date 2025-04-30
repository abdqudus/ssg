import unittest
from htmlnode import HTMLNode, LeafNode,ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )



class TestLeafNode(unittest.TestCase):
    def test_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
    def test_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_no_label(self):
        node = LeafNode(None, "Hello world")
        self.assertEqual(node.to_html(), "Hello world")

    def test_no_value(self):
        node = LeafNode("p", None)  

        with self.assertRaises(ValueError) as context:
            node.to_html() 
        # Optionally, check the error message
        self.assertEqual(str(context.exception), "All leaf nodes must have a value.")


class TextParentNode(unittest.TestCase):
    def test_parent_with_children_with_attr(self):
        node = ParentNode("div", [LeafNode("a", "Link", {"href": "http://example.com"}),LeafNode("img", "", {"src": "image.jpg"}) ])
        self.assertEqual(node.to_html(),'<div><a href="http://example.com">Link</a><img src="image.jpg"></img></div>')
    
    def test_parent_with_no_leaf_node(self):
        node = ParentNode("div", [ParentNode("section", [ParentNode("article", []) ])])
        with self.assertRaises(ValueError) as context:
            node.to_html() 
        # Optionally, check the error message
        self.assertEqual(str(context.exception), "All Parent node must have a child")

    def test_recursive_depth(self):
        node = ParentNode("div", [ParentNode("section", [ParentNode("article", [LeafNode("p", "Nested text")])])])
        self.assertEqual(node.to_html(),'<div><section><article><p>Nested text</p></article></section></div>')
    
    def test_mixed_children(self):
        node = ParentNode("div", [LeafNode("b", "Bold"),ParentNode("span", [LeafNode("i", "Italic")])])
        self.assertEqual(node.to_html(),"<div><b>Bold</b><span><i>Italic</i></span></div>")


        