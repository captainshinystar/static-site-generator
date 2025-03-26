import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Hallooo", TextType.TEXT, "www.google.com")
        node2 = TextNode("I'm a little text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_text_neq(self):
        node = TextNode("Hi, what's up?", TextType.CODE)
        node2 = TextNode("How's it going?", TextType.CODE)
        self.assertIs(node, node)

    def test_type_neq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()