from typing import (
    Any,
    cast,
    List,
    Tuple,
)
from unittest import TestCase

from sigmaF.ast import Program
from sigmaF.evaluator import (
    evaluate,
    NULL
)
from sigmaF.lexer import Lexer
from sigmaF.parser import Parser
from sigmaF.object import (
    Boolean,
    Float,
    Environment,
    Error,
    Integer,
    String,
    Object,
)


class EvaluatorTest(TestCase):

    def test_boolean_evaluation(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ('true', True),
            ('false', False),
            ('1 == 1', True),
            ('3 != 3', False),
            ('1 > 3', False),
            ('3 > 2', True),
            ('1 < 3', True),
            ('3 < 2', False),
            ('1 > 3', False),
            ('3 >= 3', True),
            ('1 > 3', False),
            ('3 <= 2', False),
            ('true == true', True),
            ('false != false', False),
            ('(1 > 2) == true', False),
            ('(1 < 2) == true', True),
            ('"hello" != "hola"', True)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_boolean_object(evaluated, expected)

    def test_float_evaluation(self) -> None:
        tests: List[Tuple[str, float]] = [
            ('5.0', 5.0),
            ('10.0', 10.0),
            ('-5.0', -5.0),
            ('-10.0', -10.0),
            ('5 / 2', 2.5),
            ('2.5 * 2.0 + 7.0', 12.0)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_float_object(evaluated, expected)

    def test_integer_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('5', 5),
            ('10', 10),
            ('-5', -5),
            ('-10', -10),
            ('5 + 5', 10),
            ('2 ** 4', 16),
            ('2 * 5 - 3', 7),
            ('10 % 5', 0),
            ('50 / 10 + 32', 37),
            ('-2 ** 5 * 2', -64)

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

    def test_if_else_evaluation(self) -> None:
        tests: List[Tuple[str, Any]] = [
            ('if (true) then {=> 10}', 10),
            ('if (false) then {=> 10}', None),
            ('if (1 < 2) then {=> 10}', 10),
            ('if (1 > 2) then {=> 10}', None),
            ('if (true) then {=> 10} else {=> 20}', 10),
            ('if (false) then {=> 10} else {=> 20}', 20),
            ('if (1 == 1) then {=> 10} else {=> 20}', 10),
            ('if (1 != 1) then {=> 10} else {=> 20}', 20),

        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)

            if type(expected) == bool:
                self._test_boolean_object(evaluated, expected)
            elif type(expected) == int:
                self._test_integer_object(evaluated, expected)
            elif type(expected) == float:
                self._test_float_object(evaluated, expected)
            elif type(expected) == str:
                self._test_string_object(evaluated, expected)
            else:
                self._test_null_object(evaluated)

    def test_return_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('=> 10;', 10),
            ('=> 10; 9;', 10),
            ('9; => 10; 2 * 4;', 10),
            ('3; => 2 * 4; 0', 8),
            ('''
                if 10 > 1 then {
                    if 20 > 10 then {
                        => 1;
                    }
                else{
                    => 0;
                    }
                }
             ''', 1),
        ]
        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_error_handling(self) -> None:
        tests: List[Tuple[str, str]] = [
            ('5 + true', 'Type Discrepancy: It is not possible to do the operation \'+\', for an INTEGER and a BOOLEAN'),
            ('5 + true; 9;', 'Type Discrepancy: It is not possible to do the operation \'+\', for an INTEGER and a BOOLEAN'),
            ('-true;', 'Unknown Operator: The operator \'-\' is unknown for BOOLEAN'),
            ('true - false;',
             'Unknown Operator: The operator \'-\' is unknown between BOOLEAN'),
            ('true + false; true',
             'Unknown Operator: The operator \'+\' is unknown between BOOLEAN'),
            ('''
                if 10 > 1 then {
                    => true * false;
                }
             ''', 'Unknown Operator: The operator \'*\' is unknown between BOOLEAN'),
            ('''
                if 10 > 1 then {
                    => true / false;
                }
             ''', 'Unknown Operator: The operator \'/\' is unknown between BOOLEAN'),
            ('''
                if 10 > 1 then {
                    => true % false;
                }
             ''', 'Unknown Operator: The operator \'%\' is unknown between BOOLEAN'),
            ('foobar;', 'Identifier not found: foobar')
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)

            self.assertIsInstance(evaluated, Error)

            evaluated = cast(Error, evaluated)
            self.assertEquals(evaluated.message, expected)

    def test_assigment_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('let a = 5; a;', 5),
            ('let a = 5; let b = a; b', 5),
            ('let a = 5; let b = 3; b;', 3),
            ('let a = 5; let b = 3; let c = b * a + 5; c;', 20),
        ]
        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def _evaluate_tests(self, source: str) -> Object:
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()
        env: Environment = Environment()

        evaluated = evaluate(program, env)

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

    def _test_null_object(self, evaluated: Object) -> None:
        self.assertEquals(evaluated, NULL)

    def _test_string_object(self, evaluated: Object, expected: str) -> None:
        self.assertIsInstance(evaluated, String)

        evaluated = cast(String, evaluated)
        self.assertEquals(evaluated.value, expected)
