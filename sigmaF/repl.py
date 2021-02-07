import readline

from os import system, name
from typing import List

from sigmaF.ast import Program
from sigmaF.object import (
    Environment,
    ObjectType
)
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


def _check_errors(source: str, enviroment: Environment) -> str:
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()
    env: Environment = enviroment

    if len(parser.errors) > 0:
        _print_parse_errors(parser.errors)
        return ''

    evaluated = evaluate(program, env)

    if evaluated is not None:
        print(evaluated.inspect())
        return ''
    return source


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def start_repl(source: str = '') -> None:
    scanned: List[str] = []
    env: Environment = Environment()

    scanned.append(_check_errors(source, env))

    lexer: Lexer = Lexer(' '.join(scanned))
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()

    if len(parser.errors) > 0:
        _print_parse_errors(parser.errors)

    evaluated = evaluate(program, env)
    if evaluated is not None and evaluated.type() is not ObjectType.ERROR:
        print(evaluated.inspect())

    while (source := input('>> ')) != 'exit()':

        if source == "clear()":
            clear()
        else:

            scanned.append(_check_errors(source, env))

            lexer: Lexer = Lexer(' '.join(scanned))
            parser: Parser = Parser(lexer)

            program: Program = parser.parse_program()

            if len(parser.errors) > 0:
                _print_parse_errors(parser.errors)
                continue

            evaluated = evaluate(program, env)

            if evaluated is not None and evaluated.type() is not ObjectType.ERROR:
                print(evaluated.inspect())

        while(token := lexer.next_token()) != EOF_TOKEN:
            print(token)
