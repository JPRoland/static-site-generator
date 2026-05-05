import unittest

from textnode import TextNode, TextType
from inline import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_ne_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.bing.com")
        self.assertNotEqual(node, node2)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertListEqual(result, expected)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(result, expected)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a *italic* word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        result = split_nodes_delimiter([node], "*", TextType.ITALIC)

        self.assertListEqual(result, expected)

    def test_mixed_delimiter_error(self):
        node = TextNode("This is text with a **bold` word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


if __name__ == "__main__":
    unittest.main()
