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
    EOF = auto()
    FUNCTION = auto()
    IDENT = auto()
    ILLEGAL = auto()
    INT = auto()
    LBRACE = auto()
    LET = auto()
    LPAREN = auto()
    PLUS = auto()
    RBRACE = auto()
    RPAREN = auto()
    SEMICOLON = auto()
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
        'int':TokenType.CLASSNAME,
        'str':TokenType.CLASSNAME,
        'float':TokenType.CLASSNAME,
        'set':TokenType.CLASSNAME,
        '->': TokenType.OUTPUTFUNTION,
        '::': TokenType.TYPEASSIGN,
    }

    return keywords.get(literal, TokenType.IDENT)
