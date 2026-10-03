from enum import Enum
 
def markdown_to_blocks(text):
    blocklist = []
    splitted = text.split("\n\n")
    for block in splitted:
        clean = block.strip()
        if clean != "":
            blocklist.append(clean)
    return blocklist

def block_to_block_type(text):
    blocktype = BlockType.PARAGRAPH
    for i in range(1, 5):
        start = ""
        for j in range(0,i):
            start += "#"
        start += " "
        if text.startswith(start):
            blocktype = BlockType.HEADING
    if blocktype == BlockType.PARAGRAPH:
        if text.startswith("```\n") and text.endswith("```"):
            blocktype = BlockType.CODE
    if blocktype == BlockType.PARAGRAPH:
        splitted = text.split("\n")
        rowcount = len(splitted)
        linecount = {
            "Q":0,
            "UOL":0,
            "OL":0
        }
        curline = 0
        for line in splitted:
            curline += 1
            if line.startswith("> ") or line == ">":
                linecount["Q"] += 1
            if line.startswith("- "):
                linecount["UOL"] += 1
            if line.startswith(str(curline) + ". "):
                linecount["OL"] += 1
        if linecount["Q"] == rowcount:
            blocktype = BlockType.QUOTE
        if linecount["UOL"] == rowcount:
            blocktype = BlockType.UNORDERED_LIST
        if linecount["OL"] == rowcount:
            blocktype = BlockType.ORDERED_LIST
    return blocktype

class BlockType(Enum):
    PARAGRAPH="paragraph"
    HEADING="heading"
    CODE="code"
    QUOTE="quote"
    UNORDERED_LIST="unordered_list"
    ORDERED_LIST="ordered_list"
    pass
