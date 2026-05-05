import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"class": "test", "id": "test"})
        self.assertEqual(node.props_to_html(), ' class="test" id="test"')

    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one(self):
        node = HTMLNode(props={"class": "test"})
        self.assertEqual(node.props_to_html(), ' class="test"')


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Hello, world!</a>'
        )

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag_no_value(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode("p", [LeafNode("b", "Hello"), LeafNode("i", "world")])
        self.assertEqual(node.to_html(), "<p><b>Hello</b><i>world</i></p>")

    def test_to_html_with_props(self):
        node = ParentNode(
            "div", [LeafNode("b", "Hello"), LeafNode("i", "world")], {"class": "test"}
        )
        self.assertEqual(
            node.to_html(),
            '<div class="test"><b>Hello</b><i>world</i></div>',
        )

    def test_to_html_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag_no_children(self):
        node = ParentNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()


class TestTextToHtmlNode(unittest.TestCase):
    def test_text_to_html_node(self):
        node = TextNode("Hello", TextType.TEXT)
        self.assertEqual(text_to_html_node(node), LeafNode(None, "Hello"))

    def test_text_to_html_node_bold(self):
        node = TextNode("Hello", TextType.BOLD)
        self.assertEqual(text_to_html_node(node), LeafNode("b", "Hello"))

    def test_text_to_html_node_italic(self):
        node = TextNode("Hello", TextType.ITALIC)
        self.assertEqual(text_to_html_node(node), LeafNode("i", "Hello"))

    def test_text_to_html_node_code(self):
        node = TextNode("Hello", TextType.CODE)
        self.assertEqual(text_to_html_node(node), LeafNode("code", "Hello"))

    def test_text_to_html_node_link(self):
        node = TextNode("Hello", TextType.LINK, "https://www.google.com")
        self.assertEqual(
            text_to_html_node(node),
            LeafNode("a", "Hello", {"href": "https://www.google.com"}),
        )

    def test_text_to_html_node_image(self):
        node = TextNode("Hello", TextType.IMAGE, "https://www.google.com")
        self.assertEqual(
            text_to_html_node(node),
            LeafNode("img", "Hello", {"src": "https://www.google.com"}),
        )

    def test_text_to_html_node_unknown(self):
        node = TextNode("Hello", "unknown")
        with self.assertRaises(ValueError):
            text_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
