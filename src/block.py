from inline import text_to_text_nodes
from htmlnode import ParentNode, text_to_html_node
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "ul"
    OL = "ol"


def markdown_to_blocks(markdown):
    markdown_blocks = markdown.split("\n\n")
    filtered_blocks = [block.strip() for block in markdown_blocks if block.strip()]
    return filtered_blocks


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_html_node(block, block_type)
        children.append(node)

    return ParentNode(tag="div", children=children)


def block_to_html_node(text, type):
    match type:
        case BlockType.QUOTE:
            return _quote_to_html_node(text)
        case BlockType.UL:
            return _ul_to_html_node(text)
        case BlockType.OL:
            return _ol_to_html_node(text)
        case BlockType.CODE:
            return _code_to_html_node(text)
        case BlockType.PARAGRAPH:
            return _paragraph_to_html_node(text)
        case BlockType.HEADING:
            return _heading_to_html_node(text)
        case _:
            raise ValueError("Invalid block type")


def block_to_block_type(block):
    if _is_heading(block):
        return BlockType.HEADING
    elif _is_code(block):
        return BlockType.CODE
    elif _is_quote(block):
        return BlockType.QUOTE
    elif _is_ul(block):
        return BlockType.UL
    elif _is_ol(block):
        return BlockType.OL
    else:
        return BlockType.PARAGRAPH


def _is_heading(block):
    if block.startswith("#") and block.strip("#")[0] == " ":
        parts = block.split()
        return 1 <= len(parts[0]) < 7
    return False


def _is_code(block):
    return block.startswith("```") and block.endswith("```")


def _is_quote(block):
    parts = block.split("\n")
    return all(part.startswith(">") for part in parts)


def _is_ul(block):
    parts = block.split("\n")
    return all(part.startswith("-") for part in parts)


def _is_ol(block):
    parts = block.split("\n")
    for i, part in enumerate(parts):
        if not part.startswith(f"{i+1}."):
            return False
    return True


def text_to_leaf_node(text):
    text_nodes = text_to_text_nodes(text)

    children = [text_to_html_node(node) for node in text_nodes]
    return children


def _paragraph_to_html_node(markdown):
    text = ""
    for line in markdown.split("\n"):
        text += " " + line
    children = text_to_leaf_node(text.strip())
    return ParentNode(tag="p", children=children)


def _heading_to_html_node(markdown):
    heading_parts = markdown.split()
    heading, heading_text = heading_parts[0], " ".join(heading_parts[1:])
    heading_num = len(heading)
    children = text_to_leaf_node(heading_text)
    return ParentNode(tag=f"h{heading_num}", children=children)


def _quote_to_html_node(markdown):
    text = ""
    for line in markdown.split("\n"):
        text += line.strip().strip(">")
    children = text_to_leaf_node(text.strip())
    return ParentNode(tag="blockquote", children=children)


def _ul_to_html_node(markdown):
    list_elements = []
    for line in markdown.split("\n"):
        children = text_to_leaf_node(line[2:])
        list_elements.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ul", children=list_elements)


def _ol_to_html_node(markdown):
    list_elements = []
    for line in markdown.split("\n"):
        children = text_to_leaf_node(line[3:])
        list_elements.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ol", children=list_elements)


def _code_to_html_node(markdown):
    list_elements = []
    text = markdown.strip("```")
    children = text_to_leaf_node(text)
    list_elements.append(ParentNode(tag="pre", children=children))
    return ParentNode(tag="code", children=list_elements)
