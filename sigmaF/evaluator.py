from typing import Any, cast, Dict, List, Optional, Type, Union

from sigmaF.token import Token, TokenType
import sigmaF.ast as ast
from sigmaF.object import (
    Boolean,
    Builtin,
    Float,
    Function,
    Environment,
    Error,
    Integer,
    Identifier,
    ValueList,
    ValueTuple,
    Void,
    Return,
    String,
    Object,
    ObjectType,
)
from sigmaF.builtins import BUILTIN

TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Void()

_NOT_A_FUNCTION = "It is not a function: {}"
_TYPE_MISMATCH = (
    "Type Discrepancy: It is not possible to do the operation '{}', for an {} and a {}"
)
_UNKNOW_PREFIX_OPERATOR = "Unknown Operator: The operator '{}' is unknown for {}"
_UNKNOW_INFIX_OPERATOR = "Unknown Operator: The operator '{}' is unknown between {}"
_DIVISION_BY_ZERO = "Division by zero: It is not possible to divide by zero {}"
_UNKNOW_IDENTIFIER = "Identifier not found: {}"
_NON_MODIFIABLE_VALUE = "Non-modifiable Value: The value of {} is not modifiable"
_WRONG_NUMBER_INDEXES = "Wrong number of indexes: {} indexes were delivered and between 1 and 3 are required"
_INDIX_FAILED = "Out range: The length of the {} is {}"
_TUPLE_FAIL = "Tuple with more of one type: The tuple have {} type and {} type"
_NOT_AN_ITERABLE = (
    "Not a iterable: The object delivered is not a iterable type is of type {}"
)
_WRONG_ARGS = (
    "Arguments wrongs: The function expected to receive types {} and receives {}"
)
_WRONG_OUTPUT = "Output wrongs: The function expected to return type {} and return {}"
_INCOMPATIBLE_LIST_OPTERATION = "Incompatible list operation: It is not possible to do the operation {} between a {} List and a {} List"
_WRONG_NUMBER_OF_INDEXES_TUPLE = "Wrong number of indexes: The tuple only required an index, and it was delivered {} indexes"
_INCOMPATIBLE_TUPLE_OPTERATION = "Incompatible tuple operation: It is not possible to do the operation {} between a {} Tuple and a {} Tuple"
_INCOMPATIBLE_NULL_OPTERATION = "Incompatible null operation: It is not possible to do the operation {} between a {} and {}"

TYPE_REGISTER_LITERAL: Dict[str, ObjectType] = {
    "int": ObjectType.INTEGER,
    "str": ObjectType.STRING,
    "bool": ObjectType.BOOLEAN,
    "float": ObjectType.FLOAT,
    "list": ObjectType.LIST,
    "tuple": ObjectType.TUPLE,
    "function": ObjectType.FUNCTION,
    "void": ObjectType.VOID,
}
TYPE_REGISTER_OBJECT: Dict[ObjectType, str] = {
    ObjectType.INTEGER: "int",
    ObjectType.STRING: "str",
    ObjectType.BOOLEAN: "bool",
    ObjectType.FLOAT: "float",
    ObjectType.LIST: "list",
    ObjectType.TUPLE: "tuple",
    ObjectType.FUNCTION: "function",
}


def evaluate(node: ast.ASTNode, env: Environment) -> Optional[Object]:
    node_type: Type = type(node)
    if node_type == ast.Program:
        node = cast(ast.Program, node)

        return _evaluate_program(node, env)

    elif node_type == ast.ExpressionStatement:
        node = cast(ast.ExpressionStatement, node)

        assert node.expression is not None
        return evaluate(node.expression, env)

    elif node_type == ast.Integer:
        node = cast(ast.Integer, node)

        assert node.value is not None
        return Integer(node.value)

    elif node_type == ast.Float:
        node = cast(ast.Float, node)

        assert node.value is not None
        return Float(node.value)

    elif node_type == ast.Boolean:
        node = cast(ast.Boolean, node)

        assert node.value is not None
        return _to_boolean_object(node.value)
    elif node_type == ast.Void:
        node = cast(ast.Void, node)

        assert node.value is None
        return _to_void_object(node.value)

    elif node_type == ast.String:
        node = cast(ast.String, node)

        assert node.value is not None

        return _to_string_object(node.value)

    elif node_type == ast.Prefix:
        node = cast(ast.Prefix, node)

        assert node.right is not None
        right = evaluate(node.right, env)

        assert right is not None
        return _evaluate_prefix_expression(node.operator, right)

    elif node_type == ast.Infix:
        node = cast(ast.Infix, node)

        assert node.left is not None and node.right is not None
        left = evaluate(node.left, env)
        right = evaluate(node.right, env)

        assert right is not None and left is not None
        return _evaluate_infix_expression(node.operator, left, right)
    elif node_type == ast.Block:
        node = cast(ast.Block, node)

        return _evaluate_block_statement(node, env)
    elif node_type == ast.If:
        node = cast(ast.If, node)

        return _evaluate_if_expression(node, env)
    elif node_type == ast.ReturnStatement:
        node = cast(ast.ReturnStatement, node)

        assert node.return_value is not None
        value = evaluate(node.return_value, env)

        assert value is not None
        return Return(value)
    elif node_type == ast.LetStatement:
        node = cast(ast.LetStatement, node)

        assert node.value is not None
        value = evaluate(node.value, env)

        assert node.name is not None

        if not node.name.value in env._store:
            env[node.name.value] = value
        else:
            return _new_error(_NON_MODIFIABLE_VALUE, [node.name.value])

    elif node_type == ast.Identifier:
        node = cast(ast.Identifier, node)

        return _evaluate_identifier(node, env)

    elif node_type == ast.Function:
        node = cast(ast.Function, node)

        assert node.body is not None
        return Function(
            node.parameters, node.type_parameters, node.type_output, node.body, env
        )
    elif node_type == ast.Call:
        node = cast(ast.Call, node)

        function = evaluate(node.function, env)
        assert function is not None
        if function.type() is ObjectType.ERROR:
            return function

        assert node.arguments is not None
        args = _evaluate_expression(node.arguments, env)

        if not _check_type_args_function(function, args):
            function = cast(Function, function)

            type_params = function.type_parameters

            type_args = []
            for arg in args:
                if arg.type() is ObjectType.ERROR:
                    return arg
                type_args.append(TYPE_REGISTER_OBJECT[arg.type()])

            return _new_error(
                _WRONG_ARGS,
                [
                    ", ".join([type_param.value for type_param in type_params[0:-1]])
                    + f", and {type_params[-1].value}"
                    if len(type_args) > 1
                    else type_params[0].value,
                    " ,".join(type_args[0:-1]) + f", and {type_args[-1]}"
                    if len(type_args) > 1
                    else type_args[0],
                ],
            )

        return_fn = _apply_function(function, args)

        if type(function) == Builtin:

            return return_fn
        elif type(function) == Function and _check_type_out_function(
            function, return_fn
        ):

            return return_fn
        elif type(function) == Error:

            return return_fn
        else:

            function = cast(Function, function)

            if return_fn.type() is ObjectType.ERROR:
                return return_fn

            return _new_error(
                _WRONG_OUTPUT,
                [function.type_output, TYPE_REGISTER_OBJECT[return_fn.type()]],
            )

    elif node_type == ast.ListValues:
        node = cast(ast.ListValues, node)

        items = _evaluate_items(node, env)
        if len(items) > 0:
            if items[0].type() != ObjectType.ERROR:
                return ValueList(items)
            else:
                return items[0]
        else:
            return ValueList([])

    elif node_type == ast.CallList:
        node = cast(ast.CallList, node)

        list_identifier = evaluate(node.list_identifier, env)
        assert list_identifier is not None

        assert node.range is not None
        ranges = _evaluate_expression(node.range, env)

        return _get_values_iter(list_identifier, ranges)
    elif node_type == ast.TupleValues:
        node = cast(ast.TupleValues, node)

        items = _evaluate_items(node, env)
        return _check_type_tuple(items)

    return None


def _check_type_tuple(items: List[Object]) -> Object:
    for item in items:
        if item.type() == ObjectType.ERROR:
            return item
    return ValueTuple(items)


def _get_values_iter(iterable: Object, ranges: List[Object]) -> Object:
    if type(iterable) == ValueList:
        return _get_values_list(cast(ValueList, iterable), ranges)

    elif type(iterable) == ValueTuple:
        return _get_values_tuple(cast(ValueTuple, iterable), ranges)

    else:
        if iterable.type() is ObjectType.ERROR:
            return iterable
        return _new_error(_NOT_AN_ITERABLE, [TYPE_REGISTER_OBJECT[iterable.type()]])


def _get_values_tuple(iterable: ValueTuple, ranges: List[Object]) -> Object:
    if len(ranges) == 1:
        assert ranges[0].type() == ObjectType.INTEGER
        index = cast(Integer, ranges[0]).value
        try:
            return iterable.values.__getitem__(index)
        except Exception:
            return _new_error(_INDIX_FAILED, ["tuple", len(iterable.values)])
    else:
        return _new_error(_WRONG_NUMBER_OF_INDEXES_TUPLE, [len(ranges)])


def _get_values_list(iterable: ValueList, ranges: List[Object]) -> Object:

    start: int = 0
    end: int = len(iterable.values)
    index_jump: Optional[int] = None

    if len(ranges) == 3:
        assert (
            ranges[0].type() == ObjectType.INTEGER
            and ranges[1].type() == ObjectType.INTEGER
            and ranges[2].type() == ObjectType.INTEGER
        )
        start = cast(Integer, ranges[0]).value
        end = cast(Integer, ranges[1]).value
        index_jump = cast(Integer, ranges[2]).value
    elif len(ranges) == 2:
        assert not (
            ranges[0].type() == ObjectType.INTEGER
            and type(ranges[1]) == ObjectType.INTEGER
        )
        start = cast(Integer, ranges[0]).value
        end = cast(Integer, ranges[1]).value
        if end > len(iterable.values):
            return NULL
    elif len(ranges) == 1:
        assert ranges[0].type() == ObjectType.INTEGER
        start = cast(Integer, ranges[0]).value
        end = cast(Integer, ranges[0]).value + 1

        try:
            range_list = iterable.values.__getitem__(slice(start, end, index_jump))
            if len(range_list) > 1:
                return ValueList(range_list)
            else:
                return range_list[0]
        except IndexError:
            return _new_error(_INDIX_FAILED, ["list", len(iterable.values)])
    else:
        return _new_error(_WRONG_NUMBER_INDEXES, [len(ranges)])

    try:
        range_list = iterable.values.__getitem__(slice(start, end, index_jump))
        return ValueList(range_list)
    except IndexError:
        return _new_error(_INDIX_FAILED, ["list", len(iterable.values)])


def _check_type_args_function(fn: Object, args: List[Object]) -> Union[bool, Object]:
    if type(fn) == Function:
        fn = cast(Function, fn)
        for idx, arg in enumerate(args):
            if arg.type() is ObjectType.ERROR:
                return arg
            type_param = fn.type_parameters[idx]
            if not arg.type() == TYPE_REGISTER_LITERAL[type_param.value]:
                return False
        return True

    else:
        return True


def _check_type_out_function(fn: Object, out: Object) -> bool:
    assert type(fn) == Function
    fn = cast(Function, fn)

    type_param = fn.type_output
    type_param = cast(Identifier, type_param)
    return bool(out.type() is TYPE_REGISTER_LITERAL[type_param.value])


def _apply_function(function, args: List[Object]) -> Object:

    if type(function) == Function:
        function = cast(Function, function)

        extended_environment = _extend_function_enviroment(function, args)

        evaluated = evaluate(function.body, extended_environment)

        assert evaluated is not None

        return _unwrap_return_value(evaluated)

    elif type(function) == Builtin:
        function = cast(Builtin, function)

        return function.fn(*args)

    else:
        return _new_error(_NOT_A_FUNCTION, [function.type().name])


def _extend_function_enviroment(fn: Function, args: List[Object]) -> Environment:
    env: Environment = Environment(outer=fn.env)
    for idx, param in enumerate(fn.parameters):
        env[param.value] = args[idx]

    return env


def _unwrap_return_value(obj: Object) -> Object:
    if type(obj) == Return:
        obj = cast(Return, obj)
        return obj.value

    return obj


def _evaluate_items(
    node: Union[ast.TupleValues, ast.ListValues], env: Environment
) -> List[Object]:
    values: List[Object] = []

    for value in node.values:
        evaluated = evaluate(value, env)

        assert evaluated is not None
        if evaluated.type() is ObjectType.ERROR:
            if type(value) is ast.Identifier:
                return [_new_error(_UNKNOW_IDENTIFIER, [value.value])]
            elif type(value) is ast.CallList:
                return [_new_error(_UNKNOW_IDENTIFIER, [value.list_identifier])]
            else:
                return [_new_error(_UNKNOW_IDENTIFIER, ["unknow identifier"])]

        values.append(evaluated)
    return values


def _evaluate_expression(
    expressions: List[ast.Expression], env: Environment
) -> List[Object]:
    result: List[Object] = []

    for expression in expressions:
        evaluated = evaluate(expression, env)

        assert evaluated is not None
        result.append(evaluated)

    return result


def _evaluate_identifier(node: ast.Identifier, env: Environment) -> Object:
    try:
        return env[node.value]
    except KeyError:
        return BUILTIN.get(node.value, _new_error(_UNKNOW_IDENTIFIER, [node.value]))


def _evaluate_if_expression(
    if_expression: ast.If, env: Environment
) -> Optional[Object]:
    assert if_expression.condition is not None
    condition = evaluate(if_expression.condition, env)

    assert condition is not None
    if _is_truthy(condition):
        assert if_expression.consequence is not None
        return evaluate(if_expression.consequence, env)
    elif if_expression.alternative is not None:
        return evaluate(if_expression.alternative, env)
    else:
        return NULL


def _is_truthy(obj: Object) -> bool:
    if obj is TRUE:
        return True
    elif obj is FALSE:
        return False
    else:
        return False


def _evaluate_block_statement(block: ast.Block, env: Environment) -> Optional[Object]:
    result: Optional[Object] = None

    for statement in block.statements:
        result = evaluate(statement, env)
        if result is not None and (
            result.type() == ObjectType.RETURN or result.type() == ObjectType.ERROR
        ):
            return result
    return result


def _evaluate_infix_expression(operator: str, left: Object, right: Object) -> Object:

    if left.type() is ObjectType.ERROR:
        return left
    elif right.type() is ObjectType.ERROR:
        return right
    elif left.type() == ObjectType.INTEGER and right.type() == ObjectType.INTEGER:

        if left.inspect() == "null" or right.inspect() == "null":
            return NULL

        return _evaluate_interger_infix_expression(operator, left, right)
    elif left.type() == ObjectType.FLOAT and right.type() == ObjectType.FLOAT:
        return _evaluate_float_infix_expression(operator, left, right)
    elif left.type() == ObjectType.STRING and right.type() == ObjectType.STRING:
        return _evaluate_string_infix_expression(operator, left, right)
    elif left.type() == ObjectType.BOOLEAN and right.type() == ObjectType.BOOLEAN:
        return _evaluate_bool_infix_expression(operator, left, right)
    elif left.type() == ObjectType.LIST and right.type() == ObjectType.LIST:
        return _evaluate_list_infix_expression(operator, left, right)
    elif left.type() == ObjectType.TUPLE and right.type() == ObjectType.TUPLE:
        return _evaluate_tuple_infix_expression(operator, left, right)
    elif left.type() == ObjectType.FUNCTION and right.type() == ObjectType.FUNCTION:

        return _evaluate_function_infix_expression(operator, left, right)
    elif left.type() != right.type():
        return _new_error(
            _TYPE_MISMATCH, [operator, left.type().name, right.type().name]
        )
    else:
        return _new_error(_UNKNOW_INFIX_OPERATOR, [operator, right.type().name])


def _evaluate_bool_infix_expression(
    operator: str, left: Object, right: Object
) -> Object:

    left_value: bool = cast(Boolean, left).value
    right_value: bool = cast(Boolean, right).value

    if operator == "==":
        return _to_boolean_object(left_value is right_value)
    elif operator == "!=":
        return _to_boolean_object(left_value is not right_value)
    elif operator == "||":
        return _to_boolean_object(left_value or right_value)
    elif operator == "&&":
        return _to_boolean_object(left_value and right_value)
    else:
        return _new_error(_UNKNOW_INFIX_OPERATOR, [operator, left.type().name])


def _evaluate_list_infix_expression(
    operator: str, left: Object, right: Object
) -> Object:
    left_list: list = cast(ValueList, left).values
    right_list: list = cast(ValueList, right).values

    if operator == "+":
        if len(left_list) > 1 and len(right_list) > 1:
            if left_list[0].type() == right_list[0].type():
                return ValueList(values=left_list + right_list)
            else:
                return _new_error(
                    _INCOMPATIBLE_LIST_OPTERATION,
                    [operator, left_list[0].type().name, right_list[0].type().name],
                )
        return ValueList(values=left_list + right_list)
    elif operator == "==":
        return _to_boolean_object(left_list == right_list)
    elif operator == "!=":
        return _to_boolean_object(left_list != right_list)
    else:
        return _new_error(_UNKNOW_INFIX_OPERATOR, [operator, right.type().name])


def _evaluate_tuple_infix_expression(
    operator: str, left: Object, right: Object
) -> Object:
    left_tuple: list = cast(ValueTuple, left).values
    right_tuple: list = cast(ValueTuple, right).values

    if operator == "+":
        if (
            len(left_tuple) == len(right_tuple)
            and left_tuple[0].type() == right_tuple[0].type()
        ):

            values = [
                _evaluate_infix_expression("+", l1, l2)
                for l1, l2 in zip(left_tuple, right_tuple)
            ]

            if values[0].type() != ObjectType.ERROR:
                return ValueTuple(values=values)
            else:
                return values[0]
        else:
            return _new_error(
                _INCOMPATIBLE_TUPLE_OPTERATION,
                [operator, left_tuple[0].type().name, right_tuple[0].type().name],
            )
    elif operator == "-":
        if (
            len(left_tuple) == len(right_tuple)
            and left_tuple[0].type() == right_tuple[0].type()
        ):

            values = [
                _evaluate_infix_expression("-", l1, l2)
                for l1, l2 in zip(left_tuple, right_tuple)
            ]

            if values[0].type() != ObjectType.ERROR:
                return ValueTuple(values=values)
            else:
                return values[0]
        else:
            return _new_error(
                _INCOMPATIBLE_TUPLE_OPTERATION,
                [operator, left_tuple[0].type().name, right_tuple[0].type().name],
            )
    elif operator == "==":
        if (
            len(left_tuple) == len(right_tuple)
            and left_tuple[0].type() == right_tuple[0].type()
        ):

            left_tuple = list(map(lambda e: e.value, left_tuple))
            right_tuple = list(map(lambda e: e.value, right_tuple))

            return _to_boolean_object(left_tuple == right_tuple)
        else:
            return _new_error(
                _INCOMPATIBLE_TUPLE_OPTERATION,
                [operator, left_tuple[0].type().name, right_tuple[0].type().name],
            )

    elif operator == "!=":
        if (
            len(left_tuple) == len(right_tuple)
            and left_tuple[0].type() == right_tuple[0].type()
        ):

            left_tuple = list(map(lambda e: e.value, left_tuple))
            right_tuple = list(map(lambda e: e.value, right_tuple))

            return _to_boolean_object(left_tuple != right_tuple)
        else:
            return _new_error(
                _INCOMPATIBLE_TUPLE_OPTERATION,
                [operator, left_tuple[0].type().name, right_tuple[0].type().name],
            )
    else:
        return _new_error(_UNKNOW_INFIX_OPERATOR, [operator, right.type().name])


def _evaluate_float_infix_expression(
    operator: str, left: Object, right: Object
) -> Object:

    left_value: float = cast(Float, left).value
    right_value: float = cast(Float, right).value

    if operator == "+":
        return Float(left_value + right_value)
    elif operator == "-":
        return Float(left_value - right_value)
    elif operator == "*":
        return Float(left_value * right_value)
    elif operator == "**":
        return Float(left_value ** right_value)
    elif operator == "/":
        if right_value == 0:
            return _new_error(_DIVISION_BY_ZERO, [""])
        return Float(left_value / right_value)
    elif operator == "%":
        return Float(left_value % right_value)
    elif operator == "<":
        return _to_boolean_object(left_value < right_value)
    elif operator == ">":
        return _to_boolean_object(left_value > right_value)
    elif operator == ">=":
        return _to_boolean_object(left_value >= right_value)
    elif operator == "<=":
        return _to_boolean_object(left_value <= right_value)
    elif operator == "==":
        return _to_boolean_object(left_value == right_value)
    elif operator == "!=":
        return _to_boolean_object(left_value != right_value)
    else:
        return _new_error(_UNKNOW_INFIX_OPERATOR, [operator, right.type().name])


def _evaluate_interger_infix_expression(
    operator: str, left: Object, right: Object
) -> Object:
    left_value: int = cast(Integer, left).value
    right_value: int = cast(Integer, right).value

    if operator == "+":
        return Integer(left_value + right_value)
    elif operator == "-":
        return Integer(left_value - right_value)
    elif operator == "*":
        return Integer(left_value * right_value)
    elif operator == "**":
        return Integer(left_value ** right_value)
    elif operator == "/":
        if right_value == 0:
            return _new_error(_DIVISION_BY_ZERO, [""])

        if left_value % right_value == 0:
            return Integer(left_value // right_value)
        else:
            return _evaluate_float_infix_expression(operator, left, right)
    elif operator == "%":
        return Integer(left_value % right_value)
    elif operator == "<":
        return _to_boolean_object(left_value < right_value)
    elif operator == ">":
        return _to_boolean_object(left_value > right_value)
    elif operator == ">=":
        return _to_boolean_object(left_value >= right_value)
    elif operator == "<=":
        return _to_boolean_object(left_value <= right_value)
    elif operator == "==":
        return _to_boolean_object(left_value == right_value)
    elif operator == "!=":
        return _to_boolean_object(left_value != right_value)
    else:
        return _new_error(_UNKNOW_INFIX_OPERATOR, [operator, right.type().name])


def _evaluate_string_infix_expression(
    operator: str, left: Object, right: Object
) -> Object:
    left_value: str = cast(String, left).value
    right_value: str = cast(String, right).value

    if operator == "+":
        return String(left_value + right_value)
    elif operator == "==":
        return _to_boolean_object(left_value == right_value)
    elif operator == "!=":
        return _to_boolean_object(left_value != right_value)
    else:
        return _new_error(_UNKNOW_INFIX_OPERATOR, [operator, right.type().name])


def _evaluate_function_infix_expression(
    operator: str, left: Object, right: Object
) -> Object:
    left_value: Function = cast(Function, left)
    right_value: Function = cast(Function, right)
    if operator == ".":
        # right_fn . left_fn =
        # fn left_parameters::left_types -> right_types {
        #       => right_fn(left_fn(left_parameters));
        # }
        # TODO: implement multi-parameter function
        # TODO: check output and input types
        new_function: Optional[Object] = evaluate(
            ast.Function(
                token=Token(TokenType.FUNCTION, "fn"),
                parameters=left_value.parameters,
                type_parameters=left_value.type_parameters,
                type_output=right_value.type_output,
                body=ast.Block(
                    token=Token(TokenType.LBRACE, "{"),
                    statements=[
                        ast.ReturnStatement(
                            token=Token(TokenType.RETURN, literal="=>"),
                            return_value=ast.Call(
                                token=Token(
                                    TokenType.LPAREN,
                                    "(",
                                ),
                                function=ast.Function(
                                    token=Token(TokenType.FUNCTION, "fn"),
                                    parameters=left_value.parameters,
                                    type_parameters=left_value.type_parameters,
                                    type_output=left_value.type_output,
                                    body=left_value.body,
                                ),
                                arguments=[
                                    ast.Call(
                                        token=Token(
                                            TokenType.LPAREN,
                                            "(",
                                        ),
                                        function=ast.Function(
                                            token=Token(TokenType.FUNCTION, "fn"),
                                            parameters=right_value.parameters,
                                            type_parameters=right_value.type_parameters,
                                            type_output=right_value.type_output,
                                            body=right_value.body,
                                        ),
                                        arguments=[
                                            cast(ast.Expression, ident)
                                            for ident in left_value.parameters
                                        ],
                                    )
                                ],
                            ),
                        )
                    ],
                ),
            ),
            Environment(),
        )
        assert new_function is not None
        return new_function
    else:
        return _new_error(_UNKNOW_INFIX_OPERATOR, [operator, right.type().name])


def _evaluate_minus_operator_expression(right: Object) -> Object:
    if type(right) == Integer:
        right = cast(Integer, right)

        return Integer(-right.value)
    elif type(right) == Float:
        right = cast(Float, right)

        return Float(-right.value)
    else:
        return _new_error(_UNKNOW_PREFIX_OPERATOR, ["-", right.type().name])


def _evaluate_prefix_expression(operator: str, right: Object) -> Object:
    if operator == "-":
        return _evaluate_minus_operator_expression(right)
    else:
        return _new_error(_UNKNOW_PREFIX_OPERATOR, [operator, right.type().name])


def _evaluate_program(program: ast.Program, env: Environment) -> Optional[Object]:
    result: Optional[Object] = None

    for statement in program.statements:
        result = evaluate(statement, env)

        if type(result) == Return:
            result = cast(Return, result)
            return result.value
        elif type(result) == Error:
            return result

    return result


def _new_error(message: str, args: List[Any]) -> Error:
    return Error(message.format(*args))


def _to_boolean_object(value: bool) -> Boolean:
    return TRUE if value else FALSE


def _to_void_object(value: None) -> Void:
    return NULL


def _to_string_object(value: str) -> String:
    return String(value[1:-1])  # Extract the quotes of the string
