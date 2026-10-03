import unittest
from markdown_block import BlockType, markdown_to_blocks, block_to_block_type


class TestTextNode(unittest.TestCase):
    def test_block_to_blocktype(self):
        md = """
### This is **bolded** heading

1. this is an ordered list
2. second list element

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

```
this is a code segment```

- This is a list
- with items
"""
        
        blocks = markdown_to_blocks(md)
        print(f"{blocks}")
        blocktype_order = [
            BlockType.HEADING,
            BlockType.ORDERED_LIST,
            BlockType.QUOTE,
            BlockType.CODE,
            BlockType.UNORDERED_LIST
        ]
        blocktypes = []
        for block in blocks:
            blocktypes.append(block_to_block_type(block))
        self.assertEqual(blocktype_order, blocktypes)
        pass



if __name__ == "__main__":
    unittest.main()