from typing import (
    cast,
    List,
    Tuple
)
from unittest import TestCase

from sigmaF.ast import Program
from sigmaF.evaluator import evaluate
from sigmaF.lexer import Lexer
from sigmaF.parser import Parser
from sigmaF.object import (
    Boolean,
    Float,
    Integer,
    String,
    Object,
)


class EvaluatorTest(TestCase):

    def test_boolean_evaluation(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ('true', True),
            ('false', False),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_boolean_object(evaluated, expected)

    def test_float_evaluation(self) -> None:
        tests: List[Tuple[str, float]] = [
            ('5.0', 5.0),
            ('10.0', 10.0),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_float_object(evaluated, expected)

    def test_integer_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('5', 5),
            ('10', 10),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_string_evaluation(self) -> None:
        tests: List[Tuple[str, str]] = [
            ('"sigmaF"', 'sigmaF'),
            ('"Hello, World"', 'Hello, World'),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_string_object(evaluated, expected)

    def _evaluate_tests(self, source: str) -> Object:
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        evaluated = evaluate(program)

        assert evaluated is not None
        return evaluated

    def _test_boolean_object(self, evaluated: Object, expected: bool) -> None:
        self.assertIsInstance(evaluated, Boolean)

        evaluated = cast(Boolean, evaluated)
        self.assertEquals(evaluated.value, expected)

    def _test_float_object(self, evaluated: Object, expected: float) -> None:
        self.assertIsInstance(evaluated, Float)

        evaluated = cast(Float, evaluated)
        self.assertEquals(evaluated.value, expected)

    def _test_integer_object(self, evaluated: Object, expected: int) -> None:
        self.assertIsInstance(evaluated, Integer)

        evaluated = cast(Integer, evaluated)
        self.assertEquals(evaluated.value, expected)

    def _test_string_object(self, evaluated: Object, expected: str) -> None:
        self.assertIsInstance(evaluated, String)

        evaluated = cast(String, evaluated)
        self.assertEquals(evaluated.value, expected)
