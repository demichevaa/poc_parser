from dataclasses import dataclass
from typing import Any

from scaner import Token


@dataclass
class Expression:
    pass
    # left: 'Expression'
    # operator: Token
    # right: 'Expression'


@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: Token
    right: Expression


@dataclass
class LiteralExpression(Expression):
    value: Any


@dataclass
class LogicalExpression(Expression):
    left: Expression
    operator: Token
    right: Expression


@dataclass
class GroupingExpression(Expression):
    expression: Expression


@dataclass
class TermExpression(Expression):
    pass


@dataclass
class FactorExpression(Expression):
    pass


@dataclass
class UnaryExpression(Expression):
    operator: Token
    right: Expression
