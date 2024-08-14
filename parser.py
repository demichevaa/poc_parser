from enum import Enum, auto
from typing import Sequence

from cursor import Cursor
from expression import Expression, BinaryExpression, LiteralExpression, UnaryExpression
from scaner import Token, Operators


class ExpressionType(Enum):
    BINARY = auto()
    GROUPING = auto()
    LITERAL = auto()
    UNARY = auto()


def equality(cur: Cursor[Token]) -> Expression:
    """
    equality → comparison ( ( "!=" | "==" ) comparison )* ;
    """
    expression = comparison(cur)

    while match_any(cur, Operators.EQUAL, Operators.NOT_EQUAL):
        operator = cur.previous()
        right = comparison(cur)
        expression = BinaryExpression(expression, operator, right)

    return expression


def comparison(cur: Cursor[Token]) -> Expression:
    """
    comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    :return:
    """
    expression = term(cur)

    while match_any(
            cur,
            Operators.GREATER,
            Operators.GREATER_OR_EQUAL,
            Operators.LESS,
            Operators.LESS_OR_EQUAL
    ):
        operator = cur.previous()
        right = term(cur)
        expression = BinaryExpression(expression, operator, right)

    return expression


def term(cur: Cursor[Token]) -> Expression:
    expression = factor(cur)

    while match_any(cur, Operators.PLUS, Operators.MINUS):
        operator = cur.previous()
        right = factor(cur)
        expression = BinaryExpression(expression, operator, right)

    return expression


def factor(cur: Cursor[Token]) -> Expression:
    expression = unary(cur)

    while match_any(cur, Operators.DIVIDE, Operators.MULTIPLY):
        operator = cur.previous()
        right = unary(cur)
        expression = BinaryExpression(expression, operator, right)

    return expression


def unary(cur: Cursor[Token]) -> Expression:
    if not match_any(cur, Operators.MINUS, Operators.NOT):
        return primary(cur)

    operator = cur.previous()
    right = unary(cur)
    return UnaryExpression(operator, right)


def primary(cur: Cursor[Token]) -> Expression:
    t = cur.advance()

    if isinstance(t.value, bool):
        return LiteralExpression(t.value)

    is_num = isinstance(t.value, int) or isinstance(t.value, float)
    is_str = isinstance(t.value, str)

    if is_num or is_str:
        return LiteralExpression(t.value)

    return None


def match_any(cur: Cursor[Token], *operators: Operators) -> bool:
    for operator in operators:
        if cur.peek().value == operator:
            return True
    return False


def parse(tokens: Sequence[Token]) -> Expression:
    cur = Cursor(tokens)
    return equality(cur)
