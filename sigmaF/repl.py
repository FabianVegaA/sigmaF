from sigmaF.lexer import Lexer
from sigmaF.token import (
    Token,
    TokenType,
)

EOF_TOKEN: Token = Token(TokenType.EOF, '')


def start_repl() -> None:
    while (source := input('>> ')) != 'exit()':
        lexer: Lexer = Lexer(source)

        while(token := lexer.next_token()) != EOF_TOKEN:
            print(token)
