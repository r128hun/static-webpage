import re
from enum import Enum

class TextType(Enum):
    TEXT="Text"
    BOLD="Bold"
    ITALIC="Italic"
    CODE="Code"
    LINK="Link"
    IMAGE="Image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        return (self.text == other.text and self.text_type == other.text_type and self.url == other.url)
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    newnodes = []
    for oldnode in old_nodes:
        if oldnode.text_type == TextType.TEXT:
            valuetext = oldnode.text
            splitted = valuetext.split(delimiter)
            in_format = False
            if len(splitted) % 2 == 0:
                raise Exception("invalid markdown format")
            for text in splitted:
                if text != "":
                    if in_format:
                        newnodes.append(TextNode(text, text_type))
                    else:
                        newnodes.append(TextNode(text, TextType.TEXT))
                in_format = (not in_format)
        else:
            newnodes.append(oldnode)
    return newnodes

def extract_markdown_images(text: str):
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches

def extract_markdown_links(text: str):
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    nodeslist = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            remainingtext = originaltext = node.text
            matches = extract_markdown_images(originaltext)
            for match in matches:
                image_alt = match[0]
                image_link = match[1]
                convert = f"![{image_alt}]({image_link})"
                splitted = remainingtext.split(convert, 1)
                nodeslist.append(TextNode(splitted[0], TextType.TEXT))
                nodeslist.append(TextNode(image_alt, TextType.IMAGE, image_link))
                remainingtext = splitted[1]
            if remainingtext != "":
                nodeslist.append(TextNode(remainingtext, TextType.TEXT))
        else:
            nodeslist.append(node)
    return nodeslist

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    nodeslist = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            remainingtext = originaltext = node.text
            matches = extract_markdown_links(originaltext)
            for match in matches:
                link_text = match[0]
                link_url = match[1]
                convert = f"[{link_text}]({link_url})"
                splitted = remainingtext.split(convert, 1)
                nodeslist.append(TextNode(splitted[0], TextType.TEXT))
                nodeslist.append(TextNode(link_text, TextType.LINK, link_url))
                remainingtext = splitted[1]
            if remainingtext != "":
                nodeslist.append(TextNode(remainingtext, TextType.TEXT))
        else:
            nodeslist.append(node)
    return nodeslist

def text_to_textnodes(text) -> list[TextNode]:
    nodeslist = [
        TextNode(text, TextType.TEXT)
    ]
    text_formats = [
        ('**', TextType.BOLD),
        ('_', TextType.ITALIC),
        ('`', TextType.CODE)
    ]
    for text_format in text_formats:
        nodeslist = split_nodes_delimiter(nodeslist, text_format[0], text_format[1])
    nodeslist = split_nodes_image(nodeslist)
    nodeslist = split_nodes_link(nodeslist)
    return nodeslist
