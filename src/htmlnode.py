from textnode import TextNode, text_to_textnodes, TextType, split_nodes_delimiter
from markdown_block import markdown_to_blocks, block_to_block_type, BlockType

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        pass
    
    def to_html(self):
        raise NotImplementedError()
    
    def propr_to_html(self):
        txt = ""
        if self.props != None:
            for key in self.props.keys():
                prop = self.props[key]
                txt = txt + " " f"{key}=\"{prop}\""
        return txt

    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag,value,None,props)
        pass
    def to_html(self):
        if self.value == None:
            raise ValueError(f"no value for tag: {self.tag}")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.propr_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Props: {self.props}"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
        pass
    def to_html(self):
        if self.tag == None:
            raise ValueError("no tag")
        if self.children == None:
            raise ValueError("no children")
        txt = f"<{self.tag}{self.propr_to_html()}>"
        for child in self.children:
            txt += child.to_html()
        txt += f"</{self.tag}{self.propr_to_html()}>"
        return txt

def block_to_htmlnode(blocktype, block):
    htmlnode = None

    tag = "p"
    children = text_to_children(blocktype, block)
    props = None
    nodetype = "leaf"

    if blocktype == BlockType.HEADING:
        hnum = 1
        curstr = ""
        for i in range(1, 6):
            curstr += "#"
            if block.startswith(curstr):
                hnum = i
        tag = "h" + str(hnum)
    elif blocktype == BlockType.CODE:
        tag = "pre"
    elif blocktype == BlockType.QUOTE:
        tag = "blockquote"
    elif blocktype == BlockType.ORDERED_LIST:
        tag = "ol"
    elif blocktype == BlockType.UNORDERED_LIST:
        tag = "ul"
    return ParentNode(tag, children, props)

def text_to_children(blocktype, text):
    children = []
    if blocktype == BlockType.CODE:
        finaltext = text.replace("```\n", "")
        finaltext = finaltext.replace("```", "")
        children.append(LeafNode("code", finaltext))
    else:
        rows = text.split("\n")
        currow = 0
        for row in rows:
            currow += 1
            if blocktype == BlockType.ORDERED_LIST or blocktype == BlockType.UNORDERED_LIST:
                if blocktype == BlockType.ORDERED_LIST:
                    row = row.replace(f"{currow}. ", "")
                else:
                    row = row.replace(f"- ", "")
                textnodes = text_to_textnodes(row)
                if len(children) > 0:
                    children.append(LeafNode(None, " "))
                subchildren = []
                for tn in textnodes:
                    subchildren.append(text_node_to_html_node(tn))
                listelement_node = ParentNode("li", subchildren)
                children.append(listelement_node)
            else:
                if blocktype == BlockType.HEADING:
                    hnum = 1
                    found = ""
                    check = ""
                    for i in range(1, 6):
                        check += "#"
                        if row.startswith(check):
                            found = check
                    row = row.replace(f"{found} ", "")
                elif blocktype == BlockType.QUOTE:
                    row = row.replace(f"> ", "")
                if len(children) > 0:
                    children.append(LeafNode(None, " "))
                textnodes = text_to_textnodes(row)
                for tn in textnodes:
                    children.append(text_node_to_html_node(tn))
    return children

def markdown_to_html_node(md) -> ParentNode:
    blocks = markdown_to_blocks(md)
    children_nodes = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        htmlnode = block_to_htmlnode(blocktype, block)
        children_nodes.append(htmlnode)
    return ParentNode("div", children_nodes)

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    node = None

    tag = None
    value = None
    props = None

    if text_node.text_type == TextType.TEXT:
        value = text_node.text
    elif text_node.text_type == TextType.BOLD:
        tag = "b"
        value = text_node.text
    elif text_node.text_type == TextType.ITALIC:
        tag = "i"
        value = text_node.text
    elif text_node.text_type == TextType.CODE:
        tag = "code"
        value = text_node.text
    elif text_node.text_type == TextType.LINK:
        tag = "a"
        value = text_node.text
        props = {"href": text_node.url}
    elif text_node.text_type == TextType.IMAGE:
        tag = "img"
        value = ""
        props = {"src": text_node.url, "alt": text_node.text}
    if tag == None and value == None:
        raise Exception("Invalid text type")
    else:
        return LeafNode(tag, value, props)