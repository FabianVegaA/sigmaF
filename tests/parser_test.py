from unittest import TestCase
from typing import (
    Any,
    Type,
    Tuple,
    cast,
    List,
)
from sigmaF.ast import (
    Block,
    Boolean,
    Call,
    CallList,
    Function,
    Infix,
    If,
    Prefix,
    Expression,
    Identifier,
    Integer,
    Program,
    LetStatement,
    ListValues,
    Void,
    TupleValues,
    ReturnStatement,
    ExpressionStatement,
)
from sigmaF.lexer import Lexer
from sigmaF.parser import Parser


class ParserTest(TestCase):
    def test_parser_program(self) -> None:
        source: str = "let x = 5;"
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertIsNotNone(program)
        self.assertIsInstance(program, Program)

    def test_let_statements(self) -> None:
        source: str = """
                let x = 5 ;
                let y = 10;
                let foo = 20;
                let float_val = 3.14159;
                let string_val = "This is a string;"
            """
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEqual(len(program.statements), 5)

        for statement in program.statements:
            self.assertEqual(statement.token_literal(), "let")
            self.assertIsInstance(statement, LetStatement)

    def test_names_in_let_statements(self) -> None:
        source: str = """
                let x = 5 ;
                let y = 10 ;
                let foo = 20 ;
            """
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        names: List[str] = []
        for statement in program.statements:
            statement = cast(LetStatement, statement)
            assert statement.name is not None
            names.append(statement.name.value)

        expected_names: List[str] = ["x", "y", "foo"]

        self.assertEquals(names, expected_names)

    def test_parse_errors(self) -> None:
        source: str = "let x 5;"
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEquals(len(parser.errors), 1)

    def test_return_statement(self) -> None:
        source: str = """
            => 5;
            => "Hello, World";
        """
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEquals(len(program.statements), 2)
        for statement in program.statements:
            self.assertEquals(statement.token_literal(), "=>")
            self.assertIsInstance(statement, ReturnStatement)

    def test_identifier_expression(self) -> None:
        source: str = "foobar;"
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        expression_statement = cast(ExpressionStatement, program.statements[0])

        assert expression_statement.expression is not None
        self._test_literal_expression(
            expression_statement.expression, "foobar")

    def test_infix_statements(self) -> None:
        source: str = """
            5 + 5;
            5 - 5;
            5 * 5;
            5 / 5;
            5 % 5;
            5 > 5;
            5 >= 5;
            5 < 5;
            5 <= 5;
            5 == 5;
            5 != 5;
            true == true;
            true != false;
        """
        lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(
            parser, program, expected_statement_count=13)

        expected_operators_and_values: List[Tuple[Any, str, Any]] = [
            (5, "+", 5),
            (5, "-", 5),
            (5, "*", 5),
            (5, "/", 5),
            (5, "%", 5),
            (5, ">", 5),
            (5, ">=", 5),
            (5, "<", 5),
            (5, "<=", 5),
            (5, "==", 5),
            (5, "!=", 5),
            (True, "==", True),
            (True, "!=", False),
        ]

        for statement, (expected_left, expected_operator, expected_right) in zip(
            program.statements, expected_operators_and_values
        ):
            statement = cast(ExpressionStatement, statement)
            assert statement.expression is not None
            self.assertIsInstance(statement.expression, Infix)
            self._test_infix_expression(
                statement.expression, expected_left, expected_operator, expected_right
            )

    def test_boolean_expression(self) -> None:
        source: str = """
            true;
            false;
        """
        lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(
            parser, program, expected_statement_count=2)

        expected_values: List[bool] = [True, False]

        for statement, expected_value in zip(program.statements, expected_values):
            expression_statement = cast(ExpressionStatement, statement)

            assert expression_statement.expression is not None
            self._test_literal_expression(
                expression_statement.expression, expected_value
            )

    def test_void_expression(self) -> None:
        source: str = """
            null;
        """
        lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        expected_values: List[None] = [None]

        for statement, expected_value in zip(program.statements, expected_values):
            expression_statement = cast(ExpressionStatement, statement)

            assert expression_statement.expression is not None
            self._test_literal_expression(
                expression_statement.expression, expected_value
            )

    def test_operator_precedence(self) -> None:
        test_sources: List[Tuple[str, str, int]] = [
            ("-a * b;", "((-a) * b)", 1),
            ("a + b / c;", "(a + (b / c))", 1),
            ("3 + 4; -5 * 5;", "(3 + 4)((-5) * 5)", 2),
            ("2 * 3 / 5 * -6 % 7;", "((((2 * 3) / 5) * (-6)) % 7)", 1),
            ("-3 ** 2;", "((-3) ** 2)", 1),
            ("2 * 4 / 5 ** 7;", "((2 * 4) / (5 ** 7))", 1),
            ("-1 + 2 % -3 + 345354**4;", "(((-1) + (2 % (-3))) + (345354 ** 4))", 1),
            (
                "-4 + 6 * 5; 45 / 6 * 8 - -1;",
                "((-4) + (6 * 5))(((45 / 6) * 8) - (-1))",
                2,
            ),
            ("a + 4 - 5 + -3 + -b;", "((((a + 4) - 5) + (-3)) + (-b))", 1),
            ("a ** 4 + 5 - -46 ** 6;", "(((a ** 4) + 5) - ((-46) ** 6))", 1),
            ("a ** 5 % 3 / 2;", "(((a ** 5) % 3) / 2)", 1),
            ("-5 * 45 ** 5 - 15 % 2;", "(((-5) * (45 ** 5)) - (15 % 2))", 1),
            ("34 ** 3 / 7 % 45 + -102", "((((34 ** 3) / 7) % 45) + (-102))", 1),
            ("3 ** (4 % 7) + 23 * -21", "((3 ** (4 % 7)) + (23 * (-21)))", 1),
            ("5 >= 34 == 4 < 2 == (a == a)",
             "(((5 >= 34) == (4 < 2)) == (a == a))", 1),
            ("a + sum(b * c) + d;", "((a + sum((b * c))) + d)", 1),
            (
                "sum(a, b, 1, 2 * 3, 4 + 5, sum(6, 7 * 8));",
                "sum(a, b, 1, (2 * 3), (4 + 5), sum(6, (7 * 8)))",
                1,
            ),
            ("4 % 2 == 0 && 2 > 0;", "(((4 % 2) == 0) && (2 > 0))", 1),
            ("-4 + 2 == 0 || 2 > 0;", "((((-4) + 2) == 0) || (2 > 0))", 1)
        ]

        for source, expected_result, expected_statement_count in test_sources:
            lexer: Lexer = Lexer(source)
            parser: Parser = Parser(lexer)

            program: Program = parser.parse_program()

            self._test_program_statements(
                parser, program, expected_statement_count)
            self.assertEquals(str(program), expected_result)

    def test_call_expression(self) -> None:
        source: str = "sum(1, 2 * 3, 4 + 5);"
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        call = cast(Call, cast(ExpressionStatement,
                               program.statements[0]).expression)

        self.assertIsInstance(call, Call)
        self._test_identifier(call.function, "sum")

        # Test arguments
        assert call.arguments is not None
        self.assertEquals(len(call.arguments), 3)
        self._test_literal_expression(call.arguments[0], 1)
        self._test_infix_expression(call.arguments[1], 2, "*", 3)
        self._test_infix_expression(call.arguments[2], 4, "+", 5)

    def test_if_expression(self) -> None:
        source: str = "if x > y then {z}"
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        # Test correct node type
        if_expression = cast(
            If, cast(ExpressionStatement, program.statements[0]).expression
        )
        self.assertIsInstance(if_expression, If)

        # Test condition
        assert if_expression.condition is not None
        self._test_infix_expression(if_expression.condition, "x", ">", "y")

        assert if_expression.consequence is not None
        self.assertIsInstance(if_expression.consequence, Block)
        self.assertEquals(len(if_expression.consequence.statements), 1)

        consequence_statement = cast(
            ExpressionStatement, if_expression.consequence.statements[0]
        )
        assert consequence_statement.expression is not None
        self._test_identifier(consequence_statement.expression, "z")

        # Test alternative
        self.assertIsNone(if_expression.alternative)

    def test_if_else_expression(self) -> None:
        source: str = "if x > y then {z} else {w}"
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        # Test correct node type
        if_expression = cast(
            If, cast(ExpressionStatement, program.statements[0]).expression
        )
        self.assertIsInstance(if_expression, If)

        # Test condition
        assert if_expression.condition is not None
        self._test_infix_expression(if_expression.condition, "x", ">", "y")

        assert if_expression.consequence is not None
        self.assertIsInstance(if_expression.consequence, Block)
        self.assertEquals(len(if_expression.consequence.statements), 1)

        consequence_statement = cast(
            ExpressionStatement, if_expression.consequence.statements[0]
        )
        assert consequence_statement.expression is not None
        self._test_identifier(consequence_statement.expression, "z")

        # Test alternative
        assert if_expression.alternative is not None
        self.assertIsInstance(if_expression.alternative, Block)
        self.assertEquals(len(if_expression.alternative.statements), 1)

        alternative_statement = cast(
            ExpressionStatement, if_expression.alternative.statements[0]
        )
        assert alternative_statement.expression is not None
        self._test_identifier(alternative_statement.expression, "w")

    def test_function_parameters(self) -> None:
        tests = [
            {
                "input": "fn x::int -> int {1}",
                "expected_params": ["x"],
                "expected_type_params": ["int"],
                "expected_type_output": "int",
            },
            {
                "input": "fn x::int, y::int -> int {1}",
                "expected_params": ["x", "y"],
                "expected_type_params": ["int", "int"],
                "expected_type_output": "int",
            },
            {
                "input": "fn x::int, y::int, z::int -> int {1}",
                "expected_params": ["x", "y", "z"],
                "expected_type_params": ["int", "int", "int"],
                "expected_type_output": "int",
            },
        ]

        for test in tests:
            lexer: Lexer = Lexer(str(test["input"]))
            parser: Parser = Parser(lexer)

            program: Program = parser.parse_program()

            function = cast(
                Function, cast(ExpressionStatement,
                               program.statements[0]).expression
            )

            self.assertEquals(len(function.parameters),
                              len(test["expected_params"]))

            for idx, param in enumerate(test["expected_params"]):
                self._test_literal_expression(function.parameters[idx], param)

            for idx, type_param in enumerate(test["expected_type_params"]):
                self._test_literal_expression(
                    function.type_parameters[idx], type_param)

            assert function.type_output is not None
            self.assertEquals(function.type_output.value,
                              test["expected_type_output"])

    def test_list(self) -> None:
        tests: List[Tuple[str, List[int]]] = [
            ("[];", []),
            ("[1,2,3];", [1, 2, 3]),
            ("[1,1,2,3,5];", [1, 1, 2, 3, 5]),
            ("[2,3,5,7,11];", [2, 3, 5, 7, 11]),
        ]

        for source, expected in tests:
            lexer: Lexer = Lexer(source)
            parser: Parser = Parser(lexer)

            program: Program = parser.parse_program()

            list_values = cast(
                ListValues, cast(ExpressionStatement,
                                 program.statements[0]).expression
            )

            self.assertIsNotNone(list_values)
            for item, expect in zip(list_values.values, expected):
                self.assertEquals(item.value, expect)

    def test_tuple(self) -> None:
        tests: List[Tuple[str, List[int]]] = [
            ("(1,2);", [1, 2]),
            ("(1,2,3);", [1, 2, 3]),
            ("(1,1,2,3,5);", [1, 1, 2, 3, 5]),
            ("(2,3,5,7,11);", [2, 3, 5, 7, 11]),
        ]

        for source, expected in tests:
            lexer: Lexer = Lexer(source)
            parser: Parser = Parser(lexer)

            program: Program = parser.parse_program()

            tuple_values = cast(
                TupleValues, cast(ExpressionStatement,
                                  program.statements[0]).expression
            )

            self.assertIsNotNone(tuple_values)
            for item, expect in zip(tuple_values.values, expected):
                self.assertEquals(item.value, expect)

    def test_tuple_and_list(self) -> None:
        tests: List[Tuple[str, List[List[int]]]] = [
            ("[(1,2)]", [[1, 2]]),
            ("[(1,2), (2,3)]", [[1, 2], [2, 3]]),
        ]

        for source, expected in tests:
            lexer: Lexer = Lexer(source)
            parser: Parser = Parser(lexer)

            program: Program = parser.parse_program()

            list_values = cast(
                ListValues, cast(ExpressionStatement,
                                 program.statements[0]).expression
            )

            self.assertIsNotNone(list_values)
            for items, expects in zip(list_values.values, expected):
                for item, expect in zip(items.values, expects):
                    self.assertEquals(item.value, expect)

    def test_call_list(self) -> None:
        source: str = "value_list[1, 2 * 3];"
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        call_list = cast(
            CallList, cast(ExpressionStatement,
                           program.statements[0]).expression
        )

        self.assertIsInstance(call_list, CallList)
        self._test_identifier(call_list.list_identifier, "value_list")

        # Test arguments
        assert call_list.range is not None
        self.assertEquals(len(call_list.range), 2)
        self._test_literal_expression(call_list.range[0], 1)
        self._test_infix_expression(call_list.range[1], 2, "*", 3)

    # TODO: Implement this test algebraic list type
    # def test_algebraic_list(self) -> None:
    #     tests: List[Tuples[str, List[str]]] = [
    #         ("[];", [""]),
    #         ("[int];", ["int"]),
    #         ("[float];", ["float"]),
    #         ("[(int, str)];", [("int", "str")]),
    #     ]

    #     for source, expected in tests:
    #         lexer: Lexer = Lexer(source)
    #         parser: Parser = Parser(lexer)

    #         program: Program = parser.parse_program()

    #         list_values = cast(
    #             ListValues, cast(ExpressionStatement,
    #                              program.statements[0]).expression
    #         )

    #         self.assertIsNotNone(list_values)
    #         for item, expect in zip(list_values.values, expected):
    #             self._test_literal_expression(item.value, expect)

    def _test_infix_expression(
        self,
        expression: Expression,
        expected_left: Any,
        expected_operator: str,
        expected_right: Any,
    ):
        infix = cast(Infix, expression)

        assert infix.left is not None
        self._test_literal_expression(infix.left, expected_left)

        self.assertEquals(infix.operator, expected_operator)

        assert infix.right is not None
        self._test_literal_expression(infix.right, expected_right)

    def _test_function_literal(self) -> None:
        source: str = "fn x::int, y::int -> int {=> x + y}"
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        # Test correct node type
        function_literal = cast(
            Function, cast(ExpressionStatement,
                           program.statements[0]).expression
        )

        self.assertIsInstance(function_literal, Function)

        # Test params
        self.assertEquals(len(function_literal.parameters), 2)
        self._test_literal_expression(function_literal.parameters[0], "x")
        self._test_literal_expression(function_literal.parameters[1], "y")

        self._test_literal_expression(
            function_literal.type_parameters[0], "int")
        self._test_literal_expression(
            function_literal.type_parameters[1], "int")

        # Test output
        assert function_literal.type_output is not None
        self.assertEquals(function_literal.type_output, "int")

        # Test body
        assert function_literal.body is not None
        self.assertEquals(len(function_literal.body.statements), 1)

        body = cast(ExpressionStatement, function_literal.body.statements[0])
        assert body.expression is not None
        self._test_infix_expression(body.expression, "x", "+", "y")

    def _test_program_statements(
        self, parser: Parser, program: Program, expected_statement_count: int = 1
    ) -> None:
        if len(parser.errors) > 0:
            print(parser.errors)
        self.assertEquals(len(parser.errors), 0)

        self.assertEquals(len(program.statements), expected_statement_count)
        self.assertIsInstance(program.statements[0], ExpressionStatement)

    def _test_literal_expression(
        self, expression: Expression, expected_value: Any
    ) -> None:
        value_type: Type = type(expected_value)

        if value_type == str:
            self._test_identifier(expression, expected_value)
        elif value_type == int:
            self._test_interger(expression, expected_value)
        elif value_type == bool:
            self._test_boolean(expression, expected_value)
        elif value_type == type(None):
            self._test_void(expression, expected_value)
        else:
            self.fail(f"Unhandle type of expression. Got={value_type}")

    def _test_boolean(self, expression: Expression, expected_value: bool) -> None:
        self.assertIsInstance(expression, Boolean)

        boolean = cast(Boolean, expression)
        self.assertEquals(boolean.value, expected_value)
        self.assertEquals(boolean.token.literal,
                          "true" if expected_value else "false")

    def _test_void(self, expression: Expression, expected_value: Any) -> None:
        self.assertIsInstance(expression, Void)

        void = cast(Void, expression)
        self.assertEquals(void.value, expected_value)
        self.assertEquals(void.token.literal, "null")

    def _test_identifier(self, expression: Expression, expected_value: Any) -> None:
        self.assertIsInstance(expression, Identifier)

        identifier = cast(Identifier, expression)
        self.assertEquals(identifier.value, expected_value)
        self.assertEquals(identifier.token.literal, expected_value)

    def _test_interger_expression(self) -> None:
        source: str = "5;"
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        expression_statement = cast(ExpressionStatement, program.statements[0])

        assert expression_statement.expression is not None
        self._test_literal_expression(expression_statement.expression, 5)

    def _test_interger(self, expression: Expression, expected_value: int) -> None:
        self.assertIsInstance(expression, Integer)

        interger = cast(Integer, expression)
        self.assertEquals(interger.value, expected_value)
        self.assertEquals(interger.token.literal, str(expected_value))

    def _test_prefix_expression(self) -> None:
        source: str = "-15;"
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()
        self._test_program_statements(
            parser, program, expected_statement_count=1)

        for statement, (expected_operator, expected_value) in zip(
            program.statements, [("-", 15)]
        ):
            statement = cast(ExpressionStatement, statement)
            self.assertIsInstance(statement.expression, Prefix)

            prefix = cast(Prefix, statement.expression)
            self.assertEquals(prefix.operator, expected_operator)

            assert prefix.right is not None
            self._test_literal_expression(prefix.right, expected_value)
