from unittest import TestCase

from sigmaF.ast import (
    Identifier,
    Program,
    LetStatement,
    ExpressionStatement,
    Integer,
    ReturnStatement,
)
from sigmaF.token import Token, TokenType


class ASTTest(TestCase):
    def test_let_statement(self) -> None:
        program: Program = Program(
            statements=[
                LetStatement(
                    token=Token(TokenType.LET, literal="let"),
                    name=Identifier(
                        token=Token(TokenType.IDENT, literal="my_val"), value="my_val"
                    ),
                    value=Identifier(
                        token=Token(TokenType.IDENT, literal="other_val"),
                        value="other_val",
                    ),
                )
            ]
        )

        program_str = str(program)

        self.assertEquals(program_str, "let my_val = other_val;")

    def test_return_statement(self) -> None:
        program: Program = Program(
            statements=[
                ReturnStatement(
                    token=Token(TokenType.RETURN, literal="=>"),
                    return_value=Identifier(
                        token=Token(TokenType.IDENT, literal="my_val"), value="my_val"
                    ),
                )
            ]
        )

        program_str = str(program)

        self.assertEquals(program_str, "=> my_val;")

    def test_integer_expressions(self) -> None:
        program: Program = Program(
            statements=[
                ExpressionStatement(
                    token=Token(TokenType.INT, literal="5"),
                    expression=Integer(
                        token=Token(TokenType.INT, literal="5"), value=5
                    ),
                ),
            ]
        )

        program_str = str(program)

        self.assertEquals(program_str, "5")
