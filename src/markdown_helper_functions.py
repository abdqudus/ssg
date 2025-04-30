import re
from enum import Enum
from textnode import TextType,TextNode,text_node_to_html_node
from htmlnode import LeafNode,ParentNode

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    ULIST = 'unordered_list'
    OLIST = 'ordered_list'


    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if len(old_nodes) == 0:
        return old_nodes
    new_node = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node.append(node)
        else:
            pattern = r'(?<!\*)\*(?!\*)'
            # Use pattern that has look behind and look forward if delimiter is *, else just split with the delimiter itself.
            # Did this because splitting with * is mixing up with **
            # When confused about this code, just split with delimiter and test the function with *, then you'd understand why you had to do this
            nodes_array = list(filter(lambda x:x != '',re.split(f'({pattern if delimiter == "*" else re.escape(delimiter)})',node.text)))
            # check if delimiter is properly applied
            delimiter_count = nodes_array.count(delimiter)
            if delimiter_count % 2 != 0:
                raise Exception("Every delimiter must be paired")
            # Create the text nodes
            n = 0
            while n < len(nodes_array):
                if nodes_array[n] != delimiter:
                    new_node.append(TextNode(nodes_array[n], TextType.TEXT))
                    n += 1
                else:
                    new_node.append(TextNode(nodes_array[n+1], text_type))
                    n += 3
    return new_node

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)
def extract_markdown_links(text):
    pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections = original_text.split(f'![{image[0]}]({image[1]})')
            if len(sections) != 2:
                raise Exception("Invalid markdown")
            if sections[0] != '':
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
            new_nodes.append(TextNode(image[0],TextType.IMAGE,image[1]))
            original_text = sections[1]
        if original_text != '':
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        # Extract the links
        links = extract_markdown_links(node.text)
        # If there's no link, just append the node
        if len(links) == 0:
            new_nodes.append(node)
            continue
        # When there's a link
        for link in links:
            # Split would split the string into 2 parts, part before, and part after
            sections = original_text.split(f'[{link[0]}]({link[1]})')
            if len(sections) != 2:
                raise Exception("Invalid markdown")
            if sections[0] != '':
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
            new_nodes.append(TextNode(link[0],TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != '':
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text,TextType.TEXT)],"**",TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,"*",TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,"`",TextType.CODE)
    nodes = split_nodes_image(split_nodes_link(nodes))
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks=[item.strip() for item in blocks]
    return list(filter(lambda x: x!= '',stripped_blocks))

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    def text_to_children(text):
            children_list = text_to_textnodes(text)
            children_list = [text_node_to_html_node(item) for item in children_list]
            return children_list
            

        
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            level = block.count("#")
            if(level > 6):
                raise ValueError(f"invalid heading level: {level}")
            children = text_to_children(block[level+1:])
            nodes.append(ParentNode(f'h{level}',children))


        elif block_type == BlockType.ULIST:
            list_items = block.split('\n')
            list_items = [word[2:].strip() for word in list_items]
            #  Here I converted the text(excluding - and space hence [2:]) to list (li) items
            list_items = [text_to_children(item) for item in list_items]
            list_items = [ParentNode('li',item) for item in list_items]
            # Here I made each list in list item a child to a li tag
            nodes.append(ParentNode('ul',list_items))

        elif block_type == BlockType.OLIST:
            list_items = block.split('\n')
            list_items = [word[2:].strip() for word in list_items]
            list_items = [text_to_children(item) for item in list_items]
            list_items = [ParentNode('li',item) for item in list_items]
            nodes.append(ParentNode('ol',list_items))
            
        elif block_type == BlockType.PARAGRAPH:
            children = text_to_children(block.replace('\n',''))
            nodes.append(ParentNode('p',children))

        elif block_type == BlockType.CODE:
            node = [text_node_to_html_node(TextNode(block[3:-3].strip(),TextType.TEXT))]
            node = [ParentNode('code',node)]
            nodes.append(ParentNode('pre',node))
        
        elif block_type == BlockType.QUOTE:
            blocks_arr = block.split('\n')
            blocks_arr = [block[2:] for block in blocks_arr]
            block = ('\n'.join(blocks_arr))
            children = text_to_children(block)
            nodes.append(ParentNode("blockquote", children))
            

    return ParentNode('div',nodes)

