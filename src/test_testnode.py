import unittest
from textnode import TextNode, TextType, split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes
from htmlnode import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        pass
    def split_nodes_link(self):
        node = TextNode(
            "This is text with an [first image link](https://i.imgur.com/zjjcJKZ.png) and another ![second LINK](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        print(f"LINK convert nodes {new_nodes}")
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("first image link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second LINK", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
        pass
    def test_full_textnode_format(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        checknodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(new_nodes, checknodes)
        pass

    def test_check_textnode_format(self):
        text = "_italic word_"
        checknodes = [
            TextNode("italic word", TextType.ITALIC),
        ]
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(new_nodes, checknodes)
        pass


if __name__ == "__main__":
    unittest.main()