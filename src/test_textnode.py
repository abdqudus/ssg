import unittest

from textnode import TextNode, TextType,text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_node_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_node_link(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK,'fb.com')
        self.assertNotEqual(node, node2)
    def test_eq_url_is_none(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)  # url is None
        node2 = TextNode("This is a text node", TextType.BOLD, url=None)  # Same content, url is None
        self.assertEqual(node, node2)



class TestTextToHTMLNode(unittest.TestCase):
    def test_img_with_src(self):
        node = TextNode("",TextType.IMAGE, 'x.com')
        node_two = TextNode("x logo",TextType.IMAGE, 'x.com')
        self.assertEqual(text_node_to_html_node(node).to_html(),'<img src="x.com" alt=""></img>')
        self.assertEqual(text_node_to_html_node(node_two).to_html(),'<img src="x.com" alt="x logo"></img>')
    
    def test_img_without_src(self):
        node = TextNode("boy",TextType.IMAGE)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node).to_html()
        self.assertEqual(str(context.exception), "TextType.IMAGE requires a URL.")
    
    def test_link_with_src(self):
        node = TextNode("boy",TextType.LINK, 'x.com')
        self.assertEqual(text_node_to_html_node(node).to_html(),'<a href="x.com">boy</a>')
    

    def test_link_without_src(self):
        node = TextNode("boy",TextType.LINK)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node).to_html()
        self.assertEqual(str(context.exception), "TextType.LINK requires a URL.")




if __name__ == "__main__":
    unittest.main()