from block import block_to_html_node
import unittest
from block import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n   \n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_trailing_whitespace(self):
        md = "This is **bolded** paragraph\n\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n\n- This is a list\n- with items\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockType(unittest.TestCase):
    def test_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_block_type_heading_invalid(self):
        self.assertEqual(block_to_block_type("####### Heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_block_type_code(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```code\ncode```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```code\ncode\ncode```"), BlockType.CODE)

    def test_block_type_quote(self):
        self.assertEqual(block_to_block_type("> quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> quote\n> quote"), BlockType.QUOTE)

    def test_block_type_ul(self):
        self.assertEqual(block_to_block_type("- ul"), BlockType.UL)
        self.assertEqual(block_to_block_type("- ul\n- ul"), BlockType.UL)

    def test_block_type_ul_invalid(self):
        self.assertEqual(block_to_block_type("* ul"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. ul"), BlockType.OL)

    def test_block_type_ol(self):
        self.assertEqual(block_to_block_type("1. ol"), BlockType.OL)
        self.assertEqual(block_to_block_type("1. ol\n2. ol"), BlockType.OL)
        self.assertEqual(block_to_block_type("1. ol\n2. ol\n3. ol"), BlockType.OL)

    def test_block_type_ol_invalid(self):
        self.assertEqual(block_to_block_type("- ol"), BlockType.UL)
        self.assertEqual(
            block_to_block_type("1. ol\n3. ol\n2. ol"), BlockType.PARAGRAPH
        )

    def test_block_type_paragraph(self):
        self.assertEqual(block_to_block_type("paragraph"), BlockType.PARAGRAPH)


class TestBlockToHTMLNode(unittest.TestCase):
    def test_block_to_html_node_heading(self):
        markdown = "# H1 Heading"
        result = block_to_html_node(markdown, BlockType.HEADING).to_html()
        expected = "<h1>H1 Heading</h1>"
        self.assertEqual(result, expected)

        markdown = "###### H6 Heading"
        result = block_to_html_node(markdown, BlockType.HEADING).to_html()
        expected = "<h6>H6 Heading</h6>"
        self.assertEqual(result, expected)

    def test_block_to_html_node_paragraph(self):
        markdown = "paragraph"
        result = block_to_html_node(markdown, BlockType.PARAGRAPH).to_html()
        expected = "<p>paragraph</p>"
        self.assertEqual(result, expected)

    def test_block_to_html_node_quote(self):
        markdown = "> quote"
        result = block_to_html_node(markdown, BlockType.QUOTE).to_html()
        expected = "<blockQuote>quote</blockQuote>"
        self.assertEqual(result, expected)

    def test_block_to_html_node_ul(self):
        markdown = "* unordered\n* list\n* items"
        result = block_to_html_node(markdown, BlockType.UL).to_html()
        expected = "<ul><li>unordered</li><li>list</li><li>items</li></ul>"
        self.assertEqual(result, expected)

    def test_block_to_html_node_ol(self):
        markdown = "1. ordered\n2. list\n3. items"
        result = block_to_html_node(markdown, BlockType.OL).to_html()
        expected = "<ol><li>ordered</li><li>list</li><li>items</li></ol>"
        self.assertEqual(result, expected)

    def test_block_to_html_node_code(self):
        markdown = "```code```"
        result = block_to_html_node(markdown, BlockType.CODE).to_html()
        expected = "<code><pre>code</pre></code>"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
