import unittest
from node_functions import *
from textnode import *

class TestTexttoHTML(unittest.TestCase):
    def test_bold(self):
        node = TextNode("heyo", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "heyo")

    def test_Italic(self):
        node = TextNode("I am italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "I am italic")

    def test_normal(self):
        node = TextNode("I'm normal", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "I'm normal")

    def test_code(self):
        node = TextNode("secret code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "secret code")

    def test_link(self):
        node = TextNode("send link", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "send link")
        self.assertEqual(html_node.props, {"href": "www.google.com"})

    def test_image(self):
        node = TextNode("silly cat", TextType.IMAGE, "www.sillycats.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "www.sillycats.com", "alt": "silly cat"})

    def test_invalid(self):
        node = TextNode("haha", None)        
        with self.assertRaises(Exception) as context:
            html_node = text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Invalid text type")

class Test_split_nodes_delimiter(unittest.TestCase):
    def test_split_nodes_two_types(self):
        nodes = [
            TextNode("Hi everybody, **what's up?**", TextType.TEXT),
            TextNode("This is italic", TextType.ITALIC),
    ]
        self.assertListEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), [
            TextNode("Hi everybody, ", TextType.TEXT),
            TextNode("what's up?", TextType.BOLD),
            TextNode("This is italic", TextType.ITALIC)
        ])

    def test_split_nodes_not_normal(self):
        nodes = [
            TextNode("This is italic", TextType.ITALIC),
            TextNode("I'm a link", TextType.LINK, "www.google.com")
    ]
        self.assertListEqual(split_nodes_delimiter(nodes, "_", TextType.ITALIC), [
            TextNode("This is italic", TextType.ITALIC),
            TextNode("I'm a link", TextType.LINK, "www.google.com")
        ])

    def test_split_nodes_normal(self):
        nodes = [
            TextNode("Hi everybody, **what's up?**", TextType.TEXT),
    ]
        self.assertListEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), [
            TextNode("Hi everybody, ", TextType.TEXT),
            TextNode("what's up?", TextType.BOLD),
        ])

    def test_no_delimiter(self):
        nodes = [
            TextNode("Hi everybody, what's up?", TextType.TEXT),
    ]
        self.assertListEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), [
            TextNode("Hi everybody, what's up?", TextType.TEXT)
        ])

    def test_unmatched_delimiter(self):
        nodes = [
            TextNode("Hi everybody, **what's up?", TextType.TEXT),
    ]
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(str(context.exception), f"Invalid markdown syntax: Unmatched delimiter **")

    def test_two_delimeter_pairs(self):
        nodes = [
            TextNode("Hi **everybody,** what's **up?**", TextType.TEXT),
    ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), [
            TextNode("Hi ", TextType.TEXT),
            TextNode("everybody,", TextType.BOLD),
            TextNode(" what's ", TextType.TEXT),
            TextNode("up?", TextType.BOLD)
        ])

    def test_two_different_delimiters(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes
        )

class Text_extract_markdown(unittest.TestCase):
    def test_extract_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_nodes_image(self):
        node = TextNode("This is a silly ![cat](https://imgur.com/gallery/girlfriends-doggo-spent-night-last-night-lR9KN)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a silly ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://imgur.com/gallery/girlfriends-doggo-spent-night-last-night-lR9KN")
            ], new_nodes
        )

    def test_split_image_single(self):
        node = TextNode("![image](https://imgur.com/gallery/3-huskies-become-friends-with-cat-after-saving-from-dying-VjaYg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://imgur.com/gallery/3-huskies-become-friends-with-cat-after-saving-from-dying-VjaYg")], new_nodes)

    def test_split_images(self):
        node = TextNode("this is ![image1](https://imgur.com/gallery/sad-pepe-oc-8nLFCVP) and this is ![image2](https://imgur.com/gallery/friend-cut-into-his-cake-said-oh-god-this-cake-is-meme-6amXGTM)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://imgur.com/gallery/sad-pepe-oc-8nLFCVP"),
                TextNode(" and this is ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "https://imgur.com/gallery/friend-cut-into-his-cake-said-oh-god-this-cake-is-meme-6amXGTM"),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode("this is my [link](www.google.com) and this is my [other link](www.youtube.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("this is my ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.google.com"),
                TextNode(" and this is my ", TextType.TEXT),
                TextNode("other link", TextType.LINK, "www.youtube.com")
            ],
            new_nodes
        )
    def test_text_to_textnode(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
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
            ],
            nodes
        )

if __name__ == "__main__":
    unittest.main()