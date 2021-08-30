from unittest import TestCase

from typing import Any, cast, List, Tuple, Union


from sigmaF.ast import Program
from sigmaF.evaluator import evaluate, NULL
from sigmaF.lexer import Lexer
from sigmaF.parser import Parser
from sigmaF.object import (
    Boolean,
    Float,
    Function,
    Environment,
    Error,
    Integer,
    ValueList,
    ValueTuple,
    String,
    Object,
)


class EvaluatorTest(TestCase):
    def test_boolean_evaluation(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ("true", True),
            ("false", False),
            ("1 == 1", True),
            ("3 != 3", False),
            ("1 > 3", False),
            ("3 > 2", True),
            ("1 < 3", True),
            ("3 < 2", False),
            ("1 > 3", False),
            ("3 >= 3", True),
            ("1 > 3", False),
            ("3 <= 2", False),
            ("true == true", True),
            ("false != false", False),
            ("(1 > 2) == true", False),
            ("(1 < 2) == true", True),
            ('"hello" != "hola"', True),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_boolean_object(evaluated, expected)

    def test_float_evaluation(self) -> None:
        tests: List[Tuple[str, float]] = [
            ("5.0", 5.0),
            ("10.0", 10.0),
            ("-5.0", -5.0),
            ("-10.0", -10.0),
            ("5 / 2", 2.5),
            ("2.5 * 2.0 + 7.0", 12.0),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_float_object(evaluated, expected)

    def test_integer_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ("5", 5),
            ("10", 10),
            ("-5", -5),
            ("-10", -10),
            ("5 + 5", 10),
            ("2 ** 4", 16),
            ("2 * 5 - 3", 7),
            ("10 % 5", 0),
            ("50 / 10 + 32", 37),
            ("-2 ** 5 * 2", -64),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_string_evaluation(self) -> None:
        tests: List[Tuple[str, str]] = [
            ('"sigmaF"', "sigmaF"),
            ('"Hello, World"', "Hello, World"),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_string_object(evaluated, expected)

    def test_if_else_evaluation(self) -> None:
        tests: List[Tuple[str, Any]] = [
            ("if (true) then {=> 10}", 10),
            ("if (false) then {=> 10}", None),
            ("if (1 < 2) then {=> 10}", 10),
            ("if (1 > 2) then {=> 10}", None),
            ("if (true) then {=> 10} else {=> 20}", 10),
            ("if (false) then {=> 10} else {=> 20}", 20),
            ("if (1 == 1) then {=> 10} else {=> 20}", 10),
            ("if (1 != 1) then {=> 10} else {=> 20}", 20),
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
            ("=> 10;", 10),
            ("=> 10; 9;", 10),
            ("9; => 10; 2 * 4;", 10),
            ("3; => 2 * 4; 0", 8),
            (
                """
                if 10 > 1 then {
                    if 20 > 10 then {
                        => 1;
                    }
                else{
                    => 0;
                    }
                }
             """,
                1,
            ),
        ]
        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_error_handling(self) -> None:
        tests: List[Tuple[str, str]] = [
            (
                "5 + true",
                "Type Discrepancy: It is not possible to do the operation '+', for an INTEGER and a BOOLEAN",
            ),
            (
                "5 + true; 9;",
                "Type Discrepancy: It is not possible to do the operation '+', for an INTEGER and a BOOLEAN",
            ),
            ("-true;", "Unknown Operator: The operator '-' is unknown for BOOLEAN"),
            (
                "true - false;",
                "Unknown Operator: The operator '-' is unknown between BOOLEAN",
            ),
            (
                "true + false; true",
                "Unknown Operator: The operator '+' is unknown between BOOLEAN",
            ),
            (
                """
                if 10 > 1 then {
                    => true * false;
                }
             """,
                "Unknown Operator: The operator '*' is unknown between BOOLEAN",
            ),
            (
                """
                if 10 > 1 then {
                    => true / false;
                }
             """,
                "Unknown Operator: The operator '/' is unknown between BOOLEAN",
            ),
            (
                """
                if 10 > 1 then {
                    => true % false;
                }
             """,
                "Unknown Operator: The operator '%' is unknown between BOOLEAN",
            ),
            ("foobar;", "Identifier not found: foobar"),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)

            self.assertIsInstance(evaluated, Error)

            evaluated = cast(Error, evaluated)
            self.assertEquals(evaluated.message, expected)

    def test_assigment_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ("let a = 5; a;", 5),
            ("let a = 5; let b = a; b", 5),
            ("let a = 5; let b = 3; b;", 3),
            ("let a = 5; let b = 3; let c = b * a + 5; c;", 20),
        ]
        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_function_evaluation(self):
        source: str = "fn x::int -> int {=> x + 2;}"

        evaluated = self._evaluate_tests(source)

        self.assertIsInstance(evaluated, Function)

        evaluated = cast(Function, evaluated)
        self.assertEquals(len(evaluated.parameters), 1)
        self.assertEquals(len(evaluated.type_parameters), 1)
        self.assertEquals(str(evaluated.parameters[0]), "x")
        self.assertEquals(str(evaluated.type_parameters[0]), "int")
        self.assertEquals(str(evaluated.type_output), "int")
        self.assertEquals(str(evaluated.body), "=> (x + 2);")

    def test_function_call(self) -> None:
        tests: List[Tuple[str, int]] = [
            ("let identity = fn x::int -> int { x }; identity(5);", 5),
            (
                """
             let identity = fn x::int -> int {
                 => x;
             };
             identity(5)
             """,
                5,
            ),
            (
                """
             let double = fn x::int -> int {
                 => x * 2;
             };
             double(5);
             """,
                10,
            ),
            (
                """
             let sum = fn x::int, y::int -> int {
                 => x + y;
             };
             sum(3,8);
             """,
                11,
            ),
            (
                """
             let sum = fn x::int, y::int -> int {
                 => x + y;
             };
             sum( 5 + 5, sum(10, 10));
             """,
                30,
            ),
            ("fn x::int -> int {=> x}(5);", 5),
            ("fn x::[int] -> int {=> length(x);}([1,2,3,4,5]);", 5),
            (
                """
            let sum = fn x::[int] -> int {
                if length(x) == 0 then {return 0;}
                return x[0] + sum(x[1, length(x)]); 
            }
            sum([1,2,3,4,5]);
             """,
                15,
            ),
            (
                """
             let init = fn xs::[a] -> a {
                 return xs[0];
             }
             init([1,2,3]);
             """,
                1,
            ),
            (
                """
             let last = fn xs::[a] -> a {
                 return xs[length(xs)-1];
             }
             last([1,2,3]);
             """,
                3,
            ),
            (
                """
             let sum_tuple = fn t::(a,a) -> int {
                 return t[0] + t[1];
             }
             sum_tuple((1,2));
             """,
                3,
            ),
            (
                """
             let tail = fn l::[a] -> [a] {return l[1,length(l)];}
             let lsum = fn l::[a] -> a {
                 if length(l) == 1 then {return l[0];};
                 return l[0] + lsum(tail(l));
             }
             lsum([1,2,3,4,5,6,7,8,9,10]);
             """,
                55,
            ),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_function_call_void(self) -> None:
        tests: List[str] = [
            """
             let nullable = fn i::int -> void {=> null;}
             nullable(5);           
             """,
            """
             let nullable = fn n::void -> void {=> n;}
             nullable(null);           
             """,
        ]

        for source in tests:
            evaluated = self._evaluate_tests(source)
            self._test_null_object(evaluated)

    def test_composition_functions(self) -> None:
        tests: List[Tuple[str, int]] = [
            (
                """
             let two = fn x::int -> int {=> x * 2;}
             let five = fn i::int -> int {=> i * 5;}
             let ten = five . two;
             ten(3);
             """,
                30,
            ),
            (
                """
             (fn x::int -> int {=> x * 2;} . fn x::int -> int {=> x * 5;})(1);
             """,
                10,
            ),
            (
                """
             let two = fn x::int -> int {=> x * 2;}
             let five = fn i::int -> int {=> i * 5;}
             let ten = fn i::int -> int {=> i * 10;};
             two . five . ten (3);
             """,
                300,
            ),
            (
                """
            let tail = fn l::[int] -> [int] { return l[1,length(l)]; }
            let sum = fn xs::[int] -> int {
                if length(xs) == 1 then { return xs[0]; }
                return xs[0] + sum . tail(xs);
            }
            sum([1,2,3,4,5]);
             """,
                15,
            ),
            (
                """
            let sum_tuple = fn x::int, y::int -> int { return x + y; }
            let by_two = fn x::str -> (int, int) { 
                let len = length(x);
                return (len, len * 2); 
            }
            
            sum_tuple . by_two ("a");
            """,
                3,
            ),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_function_call_error(self) -> None:
        tests: List[Tuple[str, str]] = [
            (
                """let identity = fn x::int -> str {
                => x; 
            } 
            identity(5);
             """,
                "Output wrongs: The function expected to return type str and return int",
            ),
            (
                """
             let identity = fn x::int -> float {
                 => x;
             };
             identity(5)
             """,
                "Output wrongs: The function expected to return type float and return int",
            ),
            (
                """
             let double = fn x::int -> list {
                 => x * 2;
             };
             double(5);
             """,
                "Output wrongs: The function expected to return type list and return int",
            ),
            (
                """
             let sum = fn x::int, y::int -> tuple {
                 => x + y;
             };
             sum(3,8);
             """,
                "Output wrongs: The function expected to return type tuple and return int",
            ),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_error_object(evaluated, expected)

    def test_builtin_function(self) -> None:
        tests: List[Tuple[str, Union[str, int]]] = [
            ('length("");', 0),
            ('length("Hello, World!");', 13),
            ('length("Supercalifragilisticexpialidocious");', 34),
            (
                "length(1);",
                "Argument to length without support, it was received a INTEGER",
            ),
            (
                'length("one", "two");',
                "Incorrect Number of arguments for length, it was received 2 arguments, and is needed only 1",
            ),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)

            if type(expected) == int:
                expected = cast(int, expected)
                self._test_integer_object(evaluated, expected)

            else:
                expected = cast(str, expected)
                self._test_error_object(evaluated, expected)

    def test_list(self) -> None:
        tests: List[Tuple[str, list]] = [
            ("[1,2,3]", [1, 2, 3]),
            ("[1.0, 2.0, 3.0]", [1.0, 2.0, 3.0]),
            ('["Hello", "World","!"]', ["Hello", "World", "!"]),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)

            evaluated = cast(ValueList, evaluated)
            for item_evaluated, item_expected in zip(evaluated.values, expected):
                assert item_evaluated != item_expected and type(item_evaluated) != type(
                    item_expected
                )

    def test_tuple(self) -> None:
        tests: List[Tuple[str, list]] = [
            ("(1,2,3)", [1, 2, 3]),
            ("(1.0, 2.0, 3.0)", [1.0, 2.0, 3.0]),
            ('("Hello", "World","!")', ["Hello", "World", "!"]),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)

            evaluated = cast(ValueTuple, evaluated)
            for item_evaluated, item_expected in zip(evaluated.values, expected):
                assert item_evaluated != item_expected and type(item_evaluated) != type(
                    item_expected
                )

    def test_list_call(self) -> None:
        tests: List[Tuple[str, int]] = [
            ("let identity = [1,2,3]; identity[1];", 2),
            (
                """
             let identity = [1,2,3];
             identity[0];
             """,
                1,
            ),
            (
                """
             let double = [1,1,2,3,4,5];
             double[5];
             """,
                5,
            ),
            (
                """
             let sum = [1,1,2,3,5,8,13,21];
             sum[7];
             """,
                21,
            ),
            (
                """
             let sum = [1,4,5,4,4,4,5];
             sum[1 + 1];
             """,
                5,
            ),
            ("[1,2,3,4,5][0];", 1),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_tuple_call(self) -> None:
        tests: List[Tuple[str, int]] = [
            ("let identity = (1,2,3); identity[1];", 2),
            (
                """
             let identity = (1,2,3);
             identity[0];
             """,
                1,
            ),
            (
                """
             let double = (1,1,2,3,4,5);
             double[5];
             """,
                5,
            ),
            (
                """
             let sum = (1,1,2,3,5,8,13,21);
             sum[7];
             """,
                21,
            ),
            (
                """
             let sum = (1,4,5,4,4,4,5);
             sum[1 + 1];
             """,
                5,
            ),
            ("(1,2,3,4,5)[0];", 1),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_call_list(self) -> None:
        tests: List[Tuple[str, str]] = [
            (
                "let identity = [1,2,3]; identity[3];",
                "Out range: The length of the list is 3",
            ),
            (
                "let identity = [1,2,3,1,2,3]; identity[100];",
                "Out range: The length of the list is 6",
            ),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_error_object(evaluated, expected)

    def test_call_tuple(self) -> None:
        tests: List[Tuple[str, str]] = [
            (
                "let identity = (1,2,3); identity[3];",
                "Out range: The length of the tuple is 3",
            ),
            (
                "let identity = (1,2,3,1,2,3); identity[100];",
                "Out range: The length of the tuple is 6",
            ),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_error_object(evaluated, expected)

    def test_bool_operator(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ("true || true;", True),
            ("true || false;", True),
            ("false || true;", True),
            ("false || false;", False),
            ("true && true;", True),
            ("true && false;", False),
            ("false && true;", False),
            ("false && false;", False),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_boolean_object(evaluated, expected)

    def test_empy_list(self) -> None:
        tests: List[Tuple[str, list]] = [
            ("[] + []", []),
            ("[1,2,3] + [4,5,6]", [1, 2, 3, 4, 5, 6]),
            ("[1,2,3] + []", [1, 2, 3]),
            ("[] + [1,2,3]", [1, 2, 3]),
        ]
        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_list_object(evaluated, expected)

    def _test_error_object(self, evaluated: Object, expected: str) -> None:
        self.assertIsInstance(evaluated, Error)

        evaluated = cast(Error, evaluated)
        self.assertEqual(evaluated.message, expected)

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
        print(evaluated.inspect())
        self.assertIsInstance(evaluated, Integer)

        evaluated = cast(Integer, evaluated)
        self.assertEquals(evaluated.value, expected)

    def _test_null_object(self, evaluated: Object) -> None:
        self.assertEquals(evaluated, NULL)

    def _test_string_object(self, evaluated: Object, expected: str) -> None:
        self.assertIsInstance(evaluated, String)

        evaluated = cast(String, evaluated)
        self.assertEquals(evaluated.value, expected)

    def _test_list_object(self, evaluated: Object, expected: list) -> None:
        self.assertIsInstance(evaluated, ValueList)

        evaluated = cast(ValueList, evaluated)
        if len(evaluated.values) > 0:
            for index, value in enumerate(evaluated.values):
                if type(value) == Integer:
                    self._test_integer_object(value, expected[index])
                elif type(value) == String:
                    self._test_string_object(value, expected[index])
                elif type(value) == Float:
                    self._test_float_object(value, expected[index])
                elif type(value) == ValueList:
                    self._test_list_object(value, expected[index])
                elif type(value) == Boolean:
                    self._test_boolean_object(value, expected[index])
                elif type(value) == ValueTuple:
                    self._test_list_object(value, expected[index])
                else:
                    self._test_null_object(value)
        else:
            self.assertListEqual(evaluated.values, expected)
