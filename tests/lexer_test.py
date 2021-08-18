from unittest import TestCase
from typing import List
from sigmaF.token import Token, TokenType
from sigmaF.lexer import Lexer


class LexerTest(TestCase):
    def test_illegal(self) -> None:
        source: str = "¡¿@"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for _ in range(len(source)):
            tokens.append(lexer.next_token())

        expected_token: List[Token] = [
            Token(TokenType.ILLEGAL, "¡"),
            Token(TokenType.ILLEGAL, "¿"),
            Token(TokenType.ILLEGAL, "@"),
        ]

        self.assertEqual(tokens, expected_token)

    def test_one_character_operator(self) -> None:
        source: str = "=+-/*<>%."
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for _ in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DIVISION, "/"),
            Token(TokenType.MULTIPLICATION, "*"),
            Token(TokenType.LT, "<"),
            Token(TokenType.GT, ">"),
            Token(TokenType.MODULUS, "%"),
            Token(TokenType.COMPOSITION, "."),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_eof(self) -> None:
        source: str = "+"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for _ in range(len(source) + 1):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.PLUS, "+"),
            Token(TokenType.EOF, ""),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_delimiters(self) -> None:
        source: str = "(){}[],;"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for _ in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.LBRAKET, "["),
            Token(TokenType.RBRAKET, "]"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.SEMICOLON, ";"),
        ]
        self.assertEquals(tokens, expected_tokens)

    def test_assignment(self) -> None:
        source: str = """
            let x = 5;
            let y = "cinco";
            let foo = 5.0;
        """
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for _ in range(15):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.INT, "5"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "y"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.STRING, '"cinco"'),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "foo"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.FLOAT, "5.0"),
            Token(TokenType.SEMICOLON, ";"),
        ]
        self.assertEquals(tokens, expected_tokens)

    def test_funtion_declaration(self) -> None:
        source: str = """
            let sum = x::int, y::int -> int {
                => x + y
            }
            let print = x::int -> void {
                => null
            }
        """
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for _ in range(30):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "sum"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.TYPEASSIGN, "::"),
            Token(TokenType.CLASSNAME, "int"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.IDENT, "y"),
            Token(TokenType.TYPEASSIGN, "::"),
            Token(TokenType.CLASSNAME, "int"),
            Token(TokenType.OUTPUTFUNTION, "->"),
            Token(TokenType.CLASSNAME, "int"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RETURN, "=>"),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.IDENT, "y"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "print"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.TYPEASSIGN, "::"),
            Token(TokenType.CLASSNAME, "int"),
            Token(TokenType.OUTPUTFUNTION, "->"),
            Token(TokenType.CLASSNAME, "void"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RETURN, "=>"),
            Token(TokenType.NULL, "null"),
            Token(TokenType.RBRACE, "}"),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_funtion_call(self) -> None:
        source: str = "let variable = suma(2,3)"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for _ in range(9):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "variable"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.IDENT, "suma"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.INT, "2"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.INT, "3"),
            Token(TokenType.RPAREN, ")"),
        ]
        self.assertEquals(tokens, expected_tokens)

    def test_control_statements(self) -> None:
        source: str = """
            if 5 < 10 then true else false
        """
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for _ in range(8):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.IF, "if"),
            Token(TokenType.INT, "5"),
            Token(TokenType.LT, "<"),
            Token(TokenType.INT, "10"),
            Token(TokenType.THEN, "then"),
            Token(TokenType.TRUE, "true"),
            Token(TokenType.ELSE, "else"),
            Token(TokenType.FALSE, "false"),
        ]
        self.assertEquals(tokens, expected_tokens)

    def test_two_character_operator(self) -> None:

        source: str = """
            10 == 10
            10 != 10
            10 >= 10
            10 <= 10
            10 ** 10
            10 || 10
            10 && 10
        """
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for _ in range(21):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.INT, "10"),
            Token(TokenType.EQ, "=="),
            Token(TokenType.INT, "10"),
            Token(TokenType.INT, "10"),
            Token(TokenType.NOT_EQ, "!="),
            Token(TokenType.INT, "10"),
            Token(TokenType.INT, "10"),
            Token(TokenType.G_OR_EQ_T, ">="),
            Token(TokenType.INT, "10"),
            Token(TokenType.INT, "10"),
            Token(TokenType.L_OR_EQ_T, "<="),
            Token(TokenType.INT, "10"),
            Token(TokenType.INT, "10"),
            Token(TokenType.EXPONENTIATION, "**"),
            Token(TokenType.INT, "10"),
            Token(TokenType.INT, "10"),
            Token(TokenType.OR, "||"),
            Token(TokenType.INT, "10"),
            Token(TokenType.INT, "10"),
            Token(TokenType.AND, "&&"),
            Token(TokenType.INT, "10"),
        ]
        self.assertEquals(tokens, expected_tokens)
