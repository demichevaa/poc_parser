import logging
import unittest

from parser import parse
from scaner import Operators, TokenType, Token, scan

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] -> %(message)s'
)


class MyTestCase(unittest.TestCase):
    def test_scan_scalar_tokens(self):
        tokens = scan("1 + 2 - 5")

        self.assertListEqual(tokens, [
            Token(TokenType.LITERAL, 1),
            Token(TokenType.OPERATOR, Operators.PLUS),
            Token(TokenType.LITERAL, 2),
            Token(TokenType.OPERATOR, Operators.MINUS),
            Token(TokenType.LITERAL, 5),
        ])

    def test_scan_long_numbers(self):
        tokens = scan("1231 + 1323.4")
        self.assertListEqual(tokens, [
            Token(TokenType.LITERAL, 1231),
            Token(TokenType.OPERATOR, Operators.PLUS),
            Token(TokenType.LITERAL, 1323.4),
        ])

    def test_parse(self):
        tokens = scan("6 <= 7 == False")

        ast = parse(tokens)
        print(ast)
        pass

    def test_ast_print(self):
        pass


if __name__ == '__main__':
    unittest.main()

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