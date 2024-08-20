from typing import Self, List, TypeVar

T = TypeVar('T')


class TreeNode[T]:
    def __init__(self, data: T):
        self.data = data
        self.descendants: List[Self] = []

    def add(self, node: Self):
        self.descendants.append(node)

    @property
    def has_any(self) -> bool:
        return bool(self.descendants)

    @property
    def size(self) -> int:
        return len(self.descendants)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.data.__repr__()


# expected
# *
# ├── +
# │   ├── a
# │   └── b
# └── c
def display(node: TreeNode, indent="", is_last=True):
    if node is None:
        return

    line_start = "└── " if is_last else "├── "

    print(indent + line_start + str(node))

    indent += "    " if is_last else "│   "

    for i, descendant in enumerate(node.descendants, 1):
        is_last = i == node.size
        display(descendant, indent, is_last=is_last)


if __name__ == "__main__":
    # (a + b) * c

    root = TreeNode('*')
    plus_node = TreeNode('+')
    a_node = TreeNode('a')
    b_node = TreeNode('b')
    c_node = TreeNode('c')
    d_node = TreeNode('d')

    plus_node.add(a_node)
    plus_node.add(b_node)

    root.add(plus_node)
    root.add(c_node)

    display(root)
