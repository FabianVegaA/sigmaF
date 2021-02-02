import readline

from os import system, name
from typing import List

from sigmaF.ast import Program
from sigmaF.parser import (
    Parser,
)
from sigmaF.lexer import Lexer
from sigmaF.token import (
    Token,
    TokenType,
)
from sigmaF.evaluator import evaluate

EOF_TOKEN: Token = Token(TokenType.EOF, '')


def _print_parse_errors(errors: List[str]):
    for error in errors:
        print(error)


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def start_repl() -> None:
    while (source := input('>> ')) != 'exit()':

        if source == "clear()":
            clear()
        else:
            lexer: Lexer = Lexer(source)
            parser: Parser = Parser(lexer)

            program: Program = parser.parse_program()

            if len(parser.errors) > 0:
                _print_parse_errors(parser.errors)
                continue

            evaluated = evaluate(program)

            if evaluated is not None:
                print(evaluated.inspect())

        while(token := lexer.next_token()) != EOF_TOKEN:
            print(token)
