import readline
import re

from os import system, name

from typing import Optional, List

from sigmaF.ast import Program
from sigmaF.object import Environment, ObjectType
from sigmaF.parser import (
    Parser,
)
from sigmaF.lexer import Lexer
from sigmaF.token import (
    Token,
    TokenType,
)
from sigmaF.evaluator import evaluate


EOF_TOKEN: Token = Token(TokenType.EOF, "")

_FILENOTFOUNT = "File not fount on {}"
_MAXIMUMRECURSIONDEPTH = "Maximum recursion depth exceeded while being evaluated {}"
_EVALUATIONERROR = "There was an error in the evaluation process {}"


def _print_parse_errors(errors: List[str]):
    for error in errors:
        print(error)


def _clean_comments(source: str) -> str:
    pattern_single_line_comment = re.compile(r"\-\-.*(\n|\b)")
    pattern_multiline_comment = re.compile(r"\/\*(\s|.)*?\*\/")

    source = re.sub(pattern_multiline_comment, "", source)
    source = re.sub(pattern_single_line_comment, "", source)

    return source


def _check_errors(source: str, enviroment: Environment) -> str:
    source = _clean_comments(source)

    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()
    env: Environment = enviroment

    if len(parser.errors) > 0:
        _print_parse_errors(parser.errors)
        return ""

    try:
        evaluated = evaluate(program, env)

        if evaluated is not None:
            print(evaluated.inspect())
            return ""
    except RecursionError:
        print("[Error] " + _MAXIMUMRECURSIONDEPTH.format(""))
    except AssertionError:
        print("\n[Error] " + _EVALUATIONERROR.format("") + "\n")

    return source


def read_module(path):
    src = None
    try:
        with open(path, mode="r", encoding="utf-8") as fin:
            lines = fin.readlines()
        src = "\n".join([str(line) for line in lines])
    except FileNotFoundError:
        print("\n[Error] " + _FILENOTFOUNT.format(path) + "\n")
    return src


def clear():
    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


def update(_path: Optional[str], env: Environment):
    if _path is None:
        print(f"[Warning] There is no path to be uploaded")
        return env

    print(f"[Warning] Updated the path: { _path}")

    new_env = Environment()

    source: str = read_module(_path)
    _ = Lexer(_check_errors(source, new_env))

    for key, value in new_env._store.items():
        if key in env.keys():
            env.__delitem__(key)

        env.__setitem__(key, value)
    return env


def process(lexer: Lexer, env: Environment):
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()

    if len(parser.errors) > 0:
        _print_parse_errors(parser.errors)

    try:
        evaluated = evaluate(program, env)

        if evaluated is not None and evaluated.type() is not ObjectType.ERROR:
            print(evaluated.inspect())

        return evaluated

    except RecursionError:
        print("\n[Error] " + _MAXIMUMRECURSIONDEPTH.format("") + "\n")
    except AssertionError:
        print("\n[Error] " + _EVALUATIONERROR.format("") + "\n")


def _stack_groupers(
    source: str, stack: list, left_groupers: str = "([{", right_groupers: str = ")]}"
) -> list:
    for char in source:
        if char in left_groupers:
            stack.append(char)
        for l_grouper, r_grouper in zip(left_groupers, right_groupers):
            if len(stack) > 0 and (stack[-1] == l_grouper and char == r_grouper):
                stack.pop()

    return stack


def read_sublines(source):

    stack = []
    sub_lines = []

    stack = _stack_groupers(source, stack)

    while len(stack) > 0 and (sub_line := input(".. ")) != ";":

        if sub_line != "":
            sub_lines.append(sub_line)
            stack = _stack_groupers(sub_line, stack)

    return "\n".join(sub_lines)


def start_repl(source: str = "", _path: Optional[str] = None) -> None:
    scanned: List[str] = []
    env: Environment = Environment()

    scanned.append(_check_errors(source, env))

    lexer: Lexer = Lexer(" ".join(scanned))

    process(lexer, env)

    _pattern_path = re.compile(r"load\(([\w\.-_\/]+)\)")

    while (source := input(">> ")) != "exit()":

        if source == "clear()":
            clear()
        elif source == "update()":
            env = update(_path, env)
        elif (path := re.match(_pattern_path, source)) is not None:
            env = update(path.group(1), env)
            _path = path.group(1)
        else:
            if source != "":
                source += read_sublines(source)

            scanned.append(_check_errors(source, env))

            lexer = Lexer(" ".join(scanned))

            process(lexer, env)

        while (token := lexer.next_token()) != EOF_TOKEN:
            print(token)
