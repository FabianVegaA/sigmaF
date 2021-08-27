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
            Token(TokenType.ILLEGAL, "¡", num_line=1),
            Token(TokenType.ILLEGAL, "¿", num_line=1),
            Token(TokenType.ILLEGAL, "@", num_line=1),
        ]

        self.assertEqual(tokens, expected_token)

    def test_one_character_operator(self) -> None:
        source: str = "=+-/*<>%."
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for _ in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ASSIGN, "=", num_line=1),
            Token(TokenType.PLUS, "+", num_line=1),
            Token(TokenType.MINUS, "-", num_line=1),
            Token(TokenType.DIVISION, "/", num_line=1),
            Token(TokenType.MULTIPLICATION, "*", num_line=1),
            Token(TokenType.LT, "<", num_line=1),
            Token(TokenType.GT, ">", num_line=1),
            Token(TokenType.MODULUS, "%", num_line=1),
            Token(TokenType.COMPOSITION, ".", num_line=1),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_eof(self) -> None:
        source: str = "+"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for _ in range(len(source) + 1):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.PLUS, "+", num_line=1),
            Token(TokenType.EOF, "", num_line=1),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_delimiters(self) -> None:
        source: str = "(){}[],;"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for _ in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LPAREN, "(", num_line=1),
            Token(TokenType.RPAREN, ")", num_line=1),
            Token(TokenType.LBRACE, "{", num_line=1),
            Token(TokenType.RBRACE, "}", num_line=1),
            Token(TokenType.LBRAKET, "[", num_line=1),
            Token(TokenType.RBRAKET, "]", num_line=1),
            Token(TokenType.COMMA, ",", num_line=1),
            Token(TokenType.SEMICOLON, ";", num_line=1),
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
            Token(TokenType.LET, "let", num_line=2),
            Token(TokenType.IDENT, "x", num_line=2),
            Token(TokenType.ASSIGN, "=", num_line=2),
            Token(TokenType.INT, "5", num_line=2),
            Token(TokenType.SEMICOLON, ";", num_line=2),
            Token(TokenType.LET, "let", num_line=3),
            Token(TokenType.IDENT, "y", num_line=3),
            Token(TokenType.ASSIGN, "=", num_line=3),
            Token(TokenType.STRING, '"cinco"', num_line=3),
            Token(TokenType.SEMICOLON, ";", num_line=3),
            Token(TokenType.LET, "let", num_line=4),
            Token(TokenType.IDENT, "foo", num_line=4),
            Token(TokenType.ASSIGN, "=", num_line=4),
            Token(TokenType.FLOAT, "5.0", num_line=4),
            Token(TokenType.SEMICOLON, ";", num_line=4),
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
            Token(TokenType.LET, "let", num_line=2),
            Token(TokenType.IDENT, "sum", num_line=2),
            Token(TokenType.ASSIGN, "=", num_line=2),
            Token(TokenType.IDENT, "x", num_line=2),
            Token(TokenType.TYPEASSIGN, "::", num_line=2),
            Token(TokenType.CLASSNAME, "int", num_line=2),
            Token(TokenType.COMMA, ",", num_line=2),
            Token(TokenType.IDENT, "y", num_line=2),
            Token(TokenType.TYPEASSIGN, "::", num_line=2),
            Token(TokenType.CLASSNAME, "int", num_line=2),
            Token(TokenType.OUTPUTFUNTION, "->", num_line=2),
            Token(TokenType.CLASSNAME, "int", num_line=2),
            Token(TokenType.LBRACE, "{", num_line=2),
            Token(TokenType.RETURN, "=>", num_line=3),
            Token(TokenType.IDENT, "x", num_line=3),
            Token(TokenType.PLUS, "+", num_line=3),
            Token(TokenType.IDENT, "y", num_line=3),
            Token(TokenType.RBRACE, "}", num_line=4),
            Token(TokenType.LET, "let", num_line=5),
            Token(TokenType.IDENT, "print", num_line=5),
            Token(TokenType.ASSIGN, "=", num_line=5),
            Token(TokenType.IDENT, "x", num_line=5),
            Token(TokenType.TYPEASSIGN, "::", num_line=5),
            Token(TokenType.CLASSNAME, "int", num_line=5),
            Token(TokenType.OUTPUTFUNTION, "->", num_line=5),
            Token(TokenType.CLASSNAME, "void", num_line=5),
            Token(TokenType.LBRACE, "{", num_line=5),
            Token(TokenType.RETURN, "=>", num_line=6),
            Token(TokenType.NULL, "null", num_line=6),
            Token(TokenType.RBRACE, "}", num_line=7),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_funtion_call(self) -> None:
        source: str = "let variable = suma(2,3)"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for _ in range(9):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, "let", num_line=1),
            Token(TokenType.IDENT, "variable", num_line=1),
            Token(TokenType.ASSIGN, "=", num_line=1),
            Token(TokenType.IDENT, "suma", num_line=1),
            Token(TokenType.LPAREN, "(", num_line=1),
            Token(TokenType.INT, "2", num_line=1),
            Token(TokenType.COMMA, ",", num_line=1),
            Token(TokenType.INT, "3", num_line=1),
            Token(TokenType.RPAREN, ")", num_line=1),
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
            Token(TokenType.IF, "if", num_line=2),
            Token(TokenType.INT, "5", num_line=2),
            Token(TokenType.LT, "<", num_line=2),
            Token(TokenType.INT, "10", num_line=2),
            Token(TokenType.THEN, "then", num_line=2),
            Token(TokenType.TRUE, "true", num_line=2),
            Token(TokenType.ELSE, "else", num_line=2),
            Token(TokenType.FALSE, "false", num_line=2),
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
            Token(TokenType.INT, "10", num_line=2),
            Token(TokenType.EQ, "==", num_line=2),
            Token(TokenType.INT, "10", num_line=2),
            Token(TokenType.INT, "10", num_line=3),
            Token(TokenType.NOT_EQ, "!=", num_line=3),
            Token(TokenType.INT, "10", num_line=3),
            Token(TokenType.INT, "10", num_line=4),
            Token(TokenType.G_OR_EQ_T, ">=", num_line=4),
            Token(TokenType.INT, "10", num_line=4),
            Token(TokenType.INT, "10", num_line=5),
            Token(TokenType.L_OR_EQ_T, "<=", num_line=5),
            Token(TokenType.INT, "10", num_line=5),
            Token(TokenType.INT, "10", num_line=6),
            Token(TokenType.EXPONENTIATION, "**", num_line=6),
            Token(TokenType.INT, "10", num_line=6),
            Token(TokenType.INT, "10", num_line=7),
            Token(TokenType.OR, "||", num_line=7),
            Token(TokenType.INT, "10", num_line=7),
            Token(TokenType.INT, "10", num_line=8),
            Token(TokenType.AND, "&&", num_line=8),
            Token(TokenType.INT, "10", num_line=8),
        ]
        self.assertEquals(tokens, expected_tokens)
