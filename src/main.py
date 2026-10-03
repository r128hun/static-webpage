from textnode import TextNode
from static_to_public import copy_from_static_to_public, generate_pages_recursive
import sys

def main():
    targetdir = "docs"
    
    copy_from_static_to_public(targetdir)
    template_file = "template.html"
    first_argument = sys.argv[1]
    basepath = "/"
    if first_argument is not None:
        basepath = first_argument

    generate_pages_recursive("content", template_file, "docs", basepath)
    pass

main()