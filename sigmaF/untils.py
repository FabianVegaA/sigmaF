from typing import Any, cast, Dict, List, Optional, Type, Union, Tuple

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


TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Void()


_INCOMPATIBLE_COMPOSITION_FUNCTION = (
    "Imcompatible Composition: It is not possible the composition of {} and {}"
)
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


_WRONG_NUMBER_OF_ARGS = "Incorrect Number of arguments for length, it was received {} arguments, and is needed only {}"
_UNSUPPORTED_ARGUMENT_TYPE = "Argument to {} without support, it was received a {}"
_PARSE_WRONG = "It is not possible to parser since {} to {}"
_WRONG_TYPE_APPEND = "It is not possible to append a {} to a list of {}"


TYPE_REGISTER_OBJECT: Dict[ObjectType, str] = {
    ObjectType.INTEGER: "int",
    ObjectType.STRING: "str",
    ObjectType.BOOLEAN: "bool",
    ObjectType.FLOAT: "float",
    ObjectType.LIST: "list",
    ObjectType.TUPLE: "tuple",
    ObjectType.FUNCTION: "function",
    ObjectType.VOID: "void",
    ObjectType.ERROR: "error",
}


def _to_str_type(
    types_: Tuple[ObjectType, Optional[List[Tuple[ObjectType, Any]]]]
) -> str:
    if types_[0] is ObjectType.LIST:
        if types_[1] is None:
            return "list"
        else:
            return f"[{_to_str_type(types_[1][0])}]"
    elif types_[0] is ObjectType.TUPLE:
        if types_[1] is None:
            return "tuple"
        else:
            return "({})".format(",".join([_to_str_type(item) for item in types_[1]]))

    else:
        return TYPE_REGISTER_OBJECT[types_[0]]


def _get_types(
    data: Object,
) -> Tuple[ObjectType, Optional[List[Tuple[ObjectType, Any]]]]:
    if data.type() is ObjectType.LIST:
        list_value = cast(ValueList, data)
        if len(list_value.values) == 0:
            return (ObjectType.LIST, None)
        return (
            ObjectType.LIST,
            [_get_types(list_value.values[0])],
        )
    elif data.type() is ObjectType.TUPLE:
        tuple_value = cast(ValueTuple, data)
        return (
            ObjectType.TUPLE,
            [_get_types(item) for item in tuple_value.values],
        )
    else:
        return (data.type(), None)
