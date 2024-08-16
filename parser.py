from enum import Enum, auto
from typing import Sequence

from cursor import Cursor
from scaner import Token, Operators
from tree import TreeNode

# TARGET RULES:

# expression→ equality ;
# equality→ comparison ( ( "!=" | "==" ) comparison )* ;
# comparison→ term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
# term→ factor ( ( "-" | "+" ) factor )* ;
# factor→ unary ( ( "/" | "*" ) unary )* ;
# unary
# → ( "!" | "-" ) unary
# | primary ;
# primary
# → NUMBER | STRING | "true" | "false" | "nil"
# | "(" expression ")" ;


class ExpressionType(Enum):
    BINARY = auto()
    GROUPING = auto()
    LITERAL = auto()
    UNARY = auto()


def match_any(cur: Cursor[Token], *operators: Operators) -> bool:
    if not cur.peek():
        return False
    for operator in operators:
        if cur.peek().value == operator:
            return True
    return False


def parse_equality(cur: Cursor[Token]) -> TreeNode[Token]:
    left = parse_comparison(cur)

    while match_any(cur, Operators.EQUAL, Operators.NOT_EQUAL):
        equality = TreeNode(cur.advance())

        right = parse_comparison(cur)
        equality.add(left)
        equality.add(right)

        return equality

    return left


def parse_comparison(cur: Cursor[Token]) -> TreeNode[Token]:
    # Stub
    return TreeNode(cur.advance())


def parse(tokens: Sequence[Token]) -> TreeNode[Token]:
    cur = Cursor(tokens)
    return parse_equality(cur)
