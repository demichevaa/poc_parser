from dataclasses import dataclass
from enum import auto
from typing import Union, List

from cursor import Cursor
import logging

from utils import BaseEnum

LOGGER = logging.getLogger(__name__)


class TerminalCharacter(BaseEnum):
    SPACE = ' ',
    DOUBLE_QUOTE = '"'
    PERCENT = '%'
    AMPERSAND = '&'
    QUOTE = "'"
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    ASTERISK = '*'
    PLUS = '+'
    COMMA = ','
    MINUS = '-'
    PERIOD = '.'
    SOLIDUS = '/'
    REVERSE_SOLIDUS = '\\'
    COLON = ':'
    SEMICOLON = ';'
    LESS_THAN = '<'
    EQUALS = '='
    GREATER_THAN = '>'
    QUESTION_MARK = '?'
    LEFT_BRACKET = '['
    RIGHT_BRACKET = ']'
    CIRCUMFLEX = '^'
    UNDERSCORE = '_'
    VERTICAL_BAR = '|'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'


class Operators(BaseEnum):
    PLUS = "+"
    MINUS = "-"
    GREATER = ">"
    GREATER_OR_EQUAL = ">="
    LESS = "<"
    LESS_OR_EQUAL = "<="
    DIVIDE = "/"
    MULTIPLY = "*"
    NOT = "NOT"
    NOT_EQUAL = "!="
    EQUAL = "=="
    ASSIGN = "="

    def __repr__(self):
        return self.value
        return f"{self.name}({self.value})"


class Keywords(BaseEnum):
    SELECT = auto()


class TokenType(BaseEnum):
    LITERAL = auto()
    OPERATOR = auto()
    KEYWORD = auto()


@dataclass
class Token:
    type: TokenType
    value: Union[Operators, Keywords, int, float]

    @staticmethod
    def from_operator(value):
        return Token(TokenType.OPERATOR, value)

    @staticmethod
    def from_literal(value):
        return Token(TokenType.LITERAL, value)

    @staticmethod
    def create(value) -> 'Token':
        if isinstance(value, Operators):
            return Token.from_operator(value)

        if (
                isinstance(value, int)
                or isinstance(value, float)
                or isinstance(value, bool)
        ):
            return Token.from_literal(value)

    def __repr__(self):
        return f"`{self.value.__repr__()}` : {self.type.__repr__()}"


def get_token(cur: Cursor[str]) -> Token:
    match cur.peek():
        case TerminalCharacter.PLUS:
            cur.next()
            return Token.create(Operators.PLUS)
        case TerminalCharacter.MINUS:
            cur.next()
            return Token.create(Operators.MINUS)
        case TerminalCharacter.LESS_THAN:
            cur.next()
            op = Operators.LESS_OR_EQUAL if cur.advance_if(TerminalCharacter.EQUALS.value) else Operators.LESS
            return Token.create(op)
        case TerminalCharacter.GREATER_THAN:
            cur.next()
            op = Operators.GREATER_OR_EQUAL if cur.advance_if(TerminalCharacter.EQUALS.value) else Operators.LESS
            return Token.create(op)
        case TerminalCharacter.EQUALS:
            cur.next()
            op = Operators.EQUAL if cur.advance_if(TerminalCharacter.EQUALS.value) else Operators.ASSIGN
            return Token.create(op)
        case c if c.isdigit():
            return Token.create(scan_number(cur))
        case c if c.isalpha():
            text = scan_alpha_numeric(cur)

            if text.upper() in Keywords:
                return Token.create(Keywords(text.upper()))
            return Token.create(bool(text))
        case c:
            raise ValueError(f"Unknown token: `{c}`")


def scan_number(cur: Cursor[str]) -> Union[int, float]:
    num = ''
    is_digit = lambda: cur.peek().isdigit()
    is_point = lambda: cur.peek() == TerminalCharacter.PERIOD

    is_float = False
    while has_point := is_point() or is_digit():
        is_float |= has_point
        num += cur.advance()

    return float(num) if is_float else int(num)


def scan_alpha_numeric(cur: Cursor[str]) -> str:
    text = ''
    while (c := cur.peek()) and c != TerminalCharacter.SPACE:
        text += cur.advance()

    return text


def scan(text: str) -> List[Token]:
    LOGGER.debug("Input: `{}`".format(text))

    cur = Cursor(text)
    tokens = []

    while cur.has_any:
        if t := get_token(cur):
            tokens.append(t)
        cur.next()

    LOGGER.debug("Tokens: {}".format(tokens))

    return tokens
