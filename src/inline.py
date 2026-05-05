import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("Invalid markdown, expected opening delimiter")

        for i, part in enumerate(split_text):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        for i, image in enumerate(matches, 1):
            parts = text.split(f"![{image[0]}]({image[1]})")
            if parts[0] == "":
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            elif parts[1] == "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            else:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            if i == len(matches) and parts[1] != "":
                new_nodes.append(TextNode(parts[1], TextType.TEXT))
            else:
                text = parts[1]
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        for i, link in enumerate(links, 1):
            parts = text.split(f"[{link[0]}]({link[1]})")
            if parts[0] == "":
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            elif parts[1] == "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            else:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            if i == len(links) and parts[1] != "":
                new_nodes.append(TextNode(parts[1], TextType.TEXT))
            else:
                text = parts[1]
    return new_nodes


def text_to_text_nodes(text):
    nodes = split_nodes_delimiter(
        old_nodes=[TextNode(text, TextType.TEXT)],
        delimiter="**",
        text_type=TextType.BOLD,
    )

    nodes = split_nodes_delimiter(
        old_nodes=nodes, delimiter="_", text_type=TextType.ITALIC
    )
    nodes = split_nodes_delimiter(
        old_nodes=nodes, delimiter="`", text_type=TextType.CODE
    )

    nodes = split_nodes_image(old_nodes=nodes)
    nodes = split_nodes_link(old_nodes=nodes)
    return nodes
