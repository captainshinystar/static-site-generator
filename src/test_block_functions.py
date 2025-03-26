import unittest
from block_functions import *

class Test_markdown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""        
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ]
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is _italic_ text




This is a paragraph with `code` text
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is _italic_ text",
                "This is a paragraph with `code` text\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"
            ]
        )

class Test_block_to_blocktype(unittest.TestCase):
    def test_heading(self):
        block = "###### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = "> quote\n> quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "- one\n- two\n- three"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)

        block = "1. one\n2. two"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)

        block = "this is a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class Test_markdown_to_html_node(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is a paragraph

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is a paragraph</p><h2>this is an h2</h2></div>"
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is a paragraph
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is a paragraph</p></div>"
        )
    
    def test_code(self):
        md = """
```
this is **text** that should
remain _the_ same even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>this is **text** that should\nremain _the_ same even with inline stuff\n</code></pre></div>"
        )

if __name__ == "__main__":
    unittest.main()