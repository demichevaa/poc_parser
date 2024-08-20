import logging
import unittest

from parser import parse
from scaner import Operators, TokenType, Token, scan
from tree import display, TreeNode

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] -> %(message)s'
)

TRUE_TOKEN = Token.create(True)
FALSE_TOKEN = Token.create(False)
EQUAL_TOKEN = Token.create(Operators.EQUAL)


class ScannerTestCase(unittest.TestCase):
    def test_scan_scalar_tokens(self):
        tokens = scan("1 + 2 - 5")

        self.assertListEqual(tokens, [
            Token(TokenType.LITERAL, 1),
            Token(TokenType.OPERATOR, Operators.PLUS),
            Token(TokenType.LITERAL, 2),
            Token(TokenType.OPERATOR, Operators.MINUS),
            Token(TokenType.LITERAL, 5),
        ])

        self.assertTrue(isinstance(tokens[0].value, int))
        self.assertTrue(isinstance(tokens[2].value, int))
        self.assertTrue(isinstance(tokens[4].value, int))

    def test_scan_long_numbers(self):
        tokens = scan("1231 + 1323.4")
        self.assertListEqual(tokens, [
            Token(TokenType.LITERAL, 1231),
            Token(TokenType.OPERATOR, Operators.PLUS),
            Token(TokenType.LITERAL, 1323.4),
        ])

        self.assertTrue(isinstance(tokens[0].value, int))
        self.assertTrue(isinstance(tokens[2].value, float))

    def test_scan_number_no_space_terminal(self):
        tokens = scan("(1)")
        self.assertListEqual(tokens, [
            Token(TokenType.OPERATOR, Operators.LEFT_PAREN),
            Token(TokenType.LITERAL, 1),
            Token(TokenType.OPERATOR, Operators.RIGHT_PAREN),
        ])
        self.assertTrue(isinstance(tokens[1].value, int))

    def test_scan_boolean_literal(self):
        for input_with_bool_literal, expected_value in [
            ("True", True),
            ("true", True),
            ("TRUE", True),
            ("False", False),
            ("false", False),
            ("FALSE", False)
        ]:
            tokens = scan(input_with_bool_literal)

            self.assertListEqual(tokens, [
                Token(TokenType.LITERAL, expected_value),
            ])
            self.assertTrue(isinstance(tokens[0].value, bool))

    def test_scan_complex_var_separators(self):
        tokens = scan("   )(1+ 2)*     3.14  ")
        self.assertListEqual(tokens, [
            Token(TokenType.OPERATOR, Operators.RIGHT_PAREN),
            Token(TokenType.OPERATOR, Operators.LEFT_PAREN),
            Token(TokenType.LITERAL, 1),
            Token(TokenType.OPERATOR, Operators.PLUS),
            Token(TokenType.LITERAL, 2),
            Token(TokenType.OPERATOR, Operators.RIGHT_PAREN),
            Token(TokenType.OPERATOR, Operators.MULTIPLY),
            Token(TokenType.LITERAL, 3.14),
        ])
        self.assertTrue(isinstance(tokens[2].value, int))
        self.assertTrue(isinstance(tokens[4].value, int))
        self.assertTrue(isinstance(tokens[7].value, float))

    def test_scan_unknown_char(self):
        with self.assertRaises(ValueError):
            scan("@")

    def test_scan_all_supported_tokens(self):
        tokens = scan("+ - * / ( ) True False < > <= >= == = 1 1.2")
        self.assertTrue(len(tokens) > 0)
        self.assertTrue(isinstance(tokens, list))

    def test_scan_not_separated_literals(self):
        with self.assertRaises(ValueError):
            scan("TrueFalse")


class ParserTestCase(unittest.TestCase):
    def test_parse_simple_comparison(self):
        tokens = scan("True == False")

        ast_head = parse(tokens)
        display(ast_head)

        self.assertIsInstance(ast_head, TreeNode)
        self.assertIsInstance(ast_head.data, Token)
        self.assertIsInstance(ast_head.descendants, list)
        self.assertEqual(len(ast_head.descendants), 2)
        self.assertIsInstance(ast_head.descendants[0], TreeNode)
        self.assertIsInstance(ast_head.descendants[0].data, Token)

        parent_token = ast_head.data
        left_token = ast_head.descendants[0].data
        right_token = ast_head.descendants[1].data

        self.assertEqual(parent_token, EQUAL_TOKEN)
        self.assertEqual(left_token, TRUE_TOKEN)
        self.assertEqual(right_token, FALSE_TOKEN)

    def test_parse_simple_paren_comparison(self):
        tokens = scan("(True) == False")

        ast_head = parse(tokens)
        display(ast_head)

    def test_parse_no_closing_paren(self):
        tokens = scan("(True == False")

        with self.assertRaises(ValueError):
            parse(tokens)

    def test_parse_comparison_with_paren(self):
        tokens = scan("((True) == (False))")

        ast_head = parse(tokens)
        display(ast_head)


if __name__ == '__main__':
    unittest.main()
