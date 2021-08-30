import re

from typing import Optional, List

from sigmaF.token import Token, TokenType
from sigmaF.lexer import Lexer
from sigmaF.parser import Parser
from sigmaF.ast import Program
from sigmaF.object import Environment, ObjectType
from sigmaF.evaluator import evaluate


from sigmaF.untils import (
    _FILE_NOT_FOUNT,
    _MAXIMUM_RECURSION_DEPTH,
    _EVALUATION_ERROR,
)


def _clean_comments(source: str) -> str:
    pattern_single_line_comment = re.compile(r"\-\-.*(\n|\b)")
    pattern_multiline_comment = re.compile(r"\/\*(\s|.)*?\*\/")

    source = re.sub(pattern_multiline_comment, "", source)
    source = re.sub(pattern_single_line_comment, "", source)

    return source


def _print_parse_errors(errors: List[str]):
    for error in errors:
        print(error)


def read_module(path):
    with open(path, mode="r", encoding="utf-8") as fin:
        lines = fin.readlines()
    src = "\n".join([str(line) for line in lines])

    return src


def execute_sigmaf(_path: str) -> None:

    env: Environment = Environment()

    source = _clean_comments(read_module(_path))

    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()

    if len(parser.errors) > 0:
        _print_parse_errors(parser.errors)

    try:
        evaluate(program, env)
    except RecursionError:
        print("[Error] " + _MAXIMUM_RECURSION_DEPTH.format(""))
    except AssertionError:
        print("\n[Error] " + _EVALUATION_ERROR.format("") + "\n")
