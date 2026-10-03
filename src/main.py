from textnode import TextNode
from static_to_public import copy_from_static_to_public, generate_pages_recursive

def main():
    copy_from_static_to_public()
    template_file = "template.html"
    generate_pages_recursive("content", template_file, "public")
    pass

main()