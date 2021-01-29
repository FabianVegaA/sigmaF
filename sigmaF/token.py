from enum import(
    auto,
    Enum,
    unique
)
from typing import (
    Dict,
    NamedTuple
)


@unique
class TokenType(Enum):
    ASSIGN = auto()
    COMMA = auto()
    CLASSNAME = auto()
    DIVISION = auto()
    ELSE = auto()
    EQ = auto()
    EOF = auto()
    EXPONENTIATION = auto()
    FALSE = auto()
    FLOAT = auto()
    FUNCTION = auto()
    G_OR_EQ_T = auto()
    GT = auto()
    IDENT = auto()
    IF = auto()
    ILLEGAL = auto()
    INT = auto()
    LBRACE = auto()
    L_OR_EQ_T = auto()
    LET = auto()
    LPAREN = auto()
    LT = auto()
    MINUS = auto()
    MODULUS = auto()
    MULTIPLICATION = auto()
    NOT_EQ = auto()
    PLUS = auto()
    RETURN = auto()
    RBRACE = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    STRING = auto()
    THEN = auto()
    TRUE = auto()
    TYPEASSIGN = auto()
    OUTPUTFUNTION = auto()


class Token(NamedTuple):
    token_type: TokenType
    literal: str

    def __str__(self) -> str:
        return f'Type: {self.token_type}, Literal: {self.literal}'


def lookup_token_type(literal: str) -> TokenType:
    keywords: Dict[str, TokenType] = {
        'let': TokenType.LET,
        'false': TokenType.FALSE,
        'true': TokenType.TRUE,
        'if': TokenType.IF,
        'then': TokenType.THEN,
        'else': TokenType.ELSE,
        'int': TokenType.CLASSNAME,
        'str': TokenType.CLASSNAME,
        'float': TokenType.CLASSNAME,
        'set': TokenType.CLASSNAME,
    }

    return keywords.get(literal, TokenType.IDENT)
