import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, markdown_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        pass
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        test = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        print("---")
        print(test)
        html = node.to_html()
        print(html)
        print("---")
        self.assertEqual(
            html,
            test,
        )
        pass

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        test = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        print("TESTING CODE BLOCK")
        print("---")
        print("TEST")
        print(test)
        html = node.to_html()
        print("=")
        print("ACTUAL")
        print(html)
        print("---")
        self.assertEqual(
            html,
            test,
        )
        pass

if __name__ == "__main__":
    unittest.main()