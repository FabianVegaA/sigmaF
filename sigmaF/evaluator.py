from typing import (
    cast,
    List,
    Optional,
)

import sigmaF.ast as ast
from sigmaF.object import (
    Boolean,
    Float,
    Integer,
    Null,
    String,
    Object,
)

TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Null()


def evaluate(node: ast.ASTNode) -> Optional[Object]:
    node_type = type(node)

    if node_type == ast.Program:
        node = cast(ast.Program, node)

        return _evaluate_statements(node.statements)

    elif node_type == ast.ExpressionStatement:
        node = cast(ast.ExpressionStatement, node)

        assert node.expression is not None
        return evaluate(node.expression)

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

    elif node_type == ast.String:
        node = cast(ast.String, node)

        assert node.value is not None

        return _to_string_object(node.value)

    return None


def _evaluate_statements(statements: List[ast.Statement]) -> Optional[Object]:
    result: Optional[Object] = None

    for statement in statements:
        result = evaluate(statement)

    return result


def _to_boolean_object(value: bool) -> Boolean:
    return TRUE if value else FALSE


def _to_string_object(value: str) -> String:
    return String(value[1:-1])  # Extract the quotes of the string
