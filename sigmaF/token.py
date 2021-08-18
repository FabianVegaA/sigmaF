from enum import auto, Enum, unique
from typing import Dict, NamedTuple


@unique
class TokenType(Enum):
    AND = auto()
    ASSIGN = auto()
    COMMA = auto()
    COMPOSITION = auto()
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
    LBRAKET = auto()
    L_OR_EQ_T = auto()
    LET = auto()
    LPAREN = auto()
    LT = auto()
    MINUS = auto()
    MODULUS = auto()
    MULTIPLICATION = auto()
    NOT_EQ = auto()
    NULL = auto()
    PLUS = auto()
    RETURN = auto()
    RBRAKET = auto()
    RBRACE = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    STRING = auto()
    THEN = auto()
    TRUE = auto()
    TYPEASSIGN = auto()
    OR = auto()
    OUTPUTFUNTION = auto()
    VOID = auto()


class Token(NamedTuple):
    token_type: TokenType
    literal: str

    def __str__(self) -> str:
        return f"Type: {self.token_type}, Literal: {self.literal}"


def lookup_token_type(literal: str) -> TokenType:
    keywords: Dict[str, TokenType] = {
        "fn": TokenType.FUNCTION,
        "let": TokenType.LET,
        "false": TokenType.FALSE,
        "true": TokenType.TRUE,
        "if": TokenType.IF,
        "then": TokenType.THEN,
        "else": TokenType.ELSE,
        "return": TokenType.RETURN,
        "bool": TokenType.CLASSNAME,
        "int": TokenType.CLASSNAME,
        "str": TokenType.CLASSNAME,
        "float": TokenType.CLASSNAME,
        "function": TokenType.CLASSNAME,
        "list": TokenType.CLASSNAME,
        "tuple": TokenType.CLASSNAME,
        "void": TokenType.CLASSNAME,
        "null": TokenType.NULL,
    }

    return keywords.get(literal, TokenType.IDENT)
