import unittest
from textnode import TextType, TextNode
from markdown_helper_functions import BlockType, split_nodes_delimiter, extract_markdown_images, extract_markdown_links,split_nodes_image, split_nodes_link, markdown_to_blocks,text_to_textnodes,block_to_block_type,markdown_to_html_node
class TestMarkdownFunctions(unittest.TestCase):

    def test_split_nodes_delimiter(self):
        # Test case 1: Basic delimiter splitting
        old_nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

        # Test case 2: Unpaired delimiter (should raise an exception)
        old_nodes = [TextNode("This is **bold text", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        # Test case 1: Extract images from text
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_output = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected_output)

        # Test case 2: No images in text
        text = "This is text without any images."
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_markdown_links(self):
        # Test case 1: Extract links from text
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_output = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(extract_markdown_links(text), expected_output)

        # Test case 2: No links in text
        text = "This is text without any links."
        self.assertEqual(extract_markdown_links(text), [])

        # Test case 3: Ensure images are not extracted as links
        text = "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to boot dev](https://www.boot.dev)"
        expected_output = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(extract_markdown_links(text), expected_output)
    def test_split_nodes_links(self):
         text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
         nodes = split_nodes_link([TextNode(text, TextType.TEXT)])
         expected_output =  [TextNode("This is text with a link ", TextType.TEXT),
                             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                             TextNode(" and ", TextType.TEXT),
                             TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")]
         self.assertEqual(nodes, expected_output)
    
    def test_split_nodes_images(self):
         text = "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
         nodes = split_nodes_image([TextNode(text, TextType.TEXT)])
         expected_output =  [TextNode("This is text with a link ", TextType.TEXT),
                             TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                             TextNode(" and ", TextType.TEXT),
                             TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev")]
         self.assertEqual(nodes, expected_output)
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        t="""
This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.


- This is the first list item in a list block
- This is a list item
- This is another list item

"""
        blocks = markdown_to_blocks(md)
        block = markdown_to_blocks(t)
        self.assertEqual(blocks,[
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ])
        self.assertEqual(block,[
            'This is a heading',
            'This is a paragraph of text. It has some **bold** and _italic_ words inside of it.',
            '- This is the first list item in a list block\n- This is a list item\n- This is another list item'
        ])
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()