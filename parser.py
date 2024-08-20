from enum import Enum, auto
from typing import Sequence, List

from cursor import Cursor
from scaner import Token, Operators, TokenType
from tree import TreeNode

# TARGET RULES:

# expression→ equality ;
# equality→ comparison ( ( "!=" | "==" ) comparison )* ;
# comparison→ term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
# term→ factor ( ( "-" | "+" ) factor )* ;
# factor→ unary ( ( "/" | "*" ) unary )* ;
# unary→ ( "!" | "-" ) unary | primary ;
# primary → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;


class ExpressionType(Enum):
    BINARY = auto()
    GROUPING = auto()
    LITERAL = auto()
    UNARY = auto()


def match_any(cur: Cursor[Token], operators: List[Operators]) -> bool:
    if not cur.peek():
        return False
    for operator in operators:
        if (t := cur.peek()) and t.value == operator:
            cur.next()
            return True
    return False


def parse_expression(cur: Cursor[Token]) -> TreeNode[Token]:
    return parse_equality(cur)


def parse_equality(cur: Cursor[Token]) -> TreeNode[Token]:
    """
    == !+
    """

    left = parse_comparison(cur)

    while match_any(cur, operators=[Operators.EQUAL, Operators.NOT_EQUAL]):
        equality = TreeNode(cur.previous())

        right = parse_comparison(cur)
        equality.add(left)
        equality.add(right)

        return equality

    return left


def parse_comparison(cur: Cursor[Token]) -> TreeNode[Token]:
    """
    < <= > >=
    """

    left = parse_term(cur)

    while match_any(cur, operators=[
        Operators.LESS,
        Operators.LESS_OR_EQUAL,
        Operators.GREATER,
        Operators.LESS_OR_EQUAL
    ]):
        comparison = TreeNode(cur.previous())

        right = parse_term(cur)
        comparison.add(left)
        comparison.add(right)

        return comparison

    return left


def parse_term(cur: Cursor[Token]) -> TreeNode[Token]:
    """
    + -
    """
    left = parse_factor(cur)

    while match_any(cur, operators=[
        Operators.PLUS,
        Operators.MINUS]
    ):
        term = TreeNode(cur.previous())

        right = parse_factor(cur)
        term.add(left)
        term.add(right)

        return term
    return left


def parse_factor(cur: Cursor[Token]) -> TreeNode[Token]:
    """
    / *
    """
    left = parse_unary(cur)

    while match_any(cur, operators=[
        Operators.DIVIDE,
        Operators.MULTIPLY
    ]):
        factor = TreeNode(cur.previous())

        right = parse_unary(cur)
        factor.add(left)
        factor.add(right)

        return factor
    return left


def parse_unary(cur: Cursor[Token]) -> TreeNode[Token]:
    if match_any(cur, operators=[
        Operators.NOT,
        Operators.MINUS
    ]):
        unary = TreeNode(cur.previous())

        right = parse_unary(cur)
        unary.add(right)

        return unary
    return parse_primary(cur)


def parse_primary(cur: Cursor[Token]) -> TreeNode[Token]:
    t = cur.peek()

    if t.type == TokenType.LITERAL:
        cur.next()
        return TreeNode(cur.previous())

    is_paren = t.type == TokenType.OPERATOR and t.value.value == Operators.LEFT_PAREN
    if is_paren:
        cur.next()

        group = TreeNode(cur.previous())
        expression = parse_expression(cur)
        group.add(expression)
        cur.consume(Token.create(Operators.RIGHT_PAREN))

        return group


def parse(tokens: Sequence[Token]) -> TreeNode[Token]:
    cur = Cursor(tokens)
    return parse_expression(cur)


if __name__ == "__main__":
    print(str(Operators.RIGHT_PAREN))