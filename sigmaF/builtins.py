import math
from typing import cast, Dict, Type, Union, Optional

from sigmaF.object import (
    Boolean,
    Builtin,
    Float,
    Function,
    Error,
    Integer,
    ValueList,
    ValueTuple,
    Void,
    Object,
    String,
)

from sigmaF.untils import (
    _to_str_type,
    _get_types,
    _WRONG_NUMBER_OF_ARGS,
    _UNSUPPORTED_ARGUMENT_TYPE,
    _PARSE_WRONG,
    _WRONG_TYPE_APPEND,
    _WRONG_ARGS,
    TRUE,
    FALSE,
    NULL,
)


def length(*args: Object) -> Object:

    argument: Optional[Union[String, ValueList, ValueTuple]] = None
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 1))
    elif type(args[0]) == String:
        argument = cast(String, args[0])
        return Integer(len(argument.value))
    elif type(args[0]) == ValueList:
        argument = cast(ValueList, args[0])
        return Integer(len(argument.values))
    elif type(args[0]) == ValueTuple:
        argument = cast(ValueTuple, args[0])
        return Integer(len(argument.values))
    else:
        return Error(_UNSUPPORTED_ARGUMENT_TYPE.format("length", args[0].type().name))


def println(*args: Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 1))
    else:
        type_arg: Type = type(args[0])
        argument: Optional[
            Union[String, Integer, Float, Boolean, ValueList, ValueTuple, Function]
        ] = None
        if type_arg == Error:
            return args[0]

        elif type_arg == String:
            argument = cast(String, args[0])
            string = argument.inspect().replace("\\n", "\n").replace("\\t", "\t")
            print(string)

        elif type_arg == Integer:
            argument = cast(Integer, args[0])
            print(argument.inspect())

        elif type_arg == Float:
            argument = cast(Float, args[0])
            print(argument.inspect())

        elif type_arg == ValueList:
            argument = cast(ValueList, args[0])
            print(argument.inspect())

        elif type_arg == ValueTuple:
            argument = cast(ValueTuple, args[0])
            print(argument.inspect())

        elif type_arg == Boolean:
            argument = cast(Boolean, args[0])
            print(argument.inspect())

        elif type_arg == Function:
            argument = cast(Function, args[0])
            print(argument.inspect())

        else:
            return Error(
                _UNSUPPORTED_ARGUMENT_TYPE.format("printLn", args[0].type().name)
            )

        return NULL


def negation_boolean(*args: Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 1))
    else:
        type_arg: Type = type(args[0])
        argument: Optional[Boolean] = None

        if type_arg == Boolean:
            argument = cast(Boolean, args[0])
            return FALSE if argument.value else TRUE
        else:
            return Error(_UNSUPPORTED_ARGUMENT_TYPE.format("not", args[0].type().name))


def pow_impure(*args: Object) -> Object:
    if len(args) != 2:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 2))
    else:
        type_radicant: Type = type(args[0])
        type_index: Type = type(args[1])
        radicant: Optional[Union[Integer, Float]] = None
        index: Optional[Union[Integer, Float]] = None

        if type_radicant == Integer and type_index == Integer:
            radicant = cast(Integer, args[0])
            index = cast(Integer, args[1])

            root_math = math.pow(radicant.value, 1 / index.value)
            return Float(root_math)
        elif type_radicant == Float and type_index == Float:
            radicant = cast(Float, args[0])
            index = cast(Float, args[1])

            root_math = math.pow(radicant.value, 1 / index.value)
            return Float(root_math)
        elif type_radicant == Float and type_index == Integer:
            radicant = cast(Float, args[0])
            index = cast(Integer, args[1])

            root_math = math.pow(radicant.value, 1 / index.value)
            return Float(root_math)
        elif type_radicant == Integer and type_index == Float:
            radicant = cast(Integer, args[0])
            index = cast(Float, args[1])

            root_math = math.pow(radicant.value, 1 / index.value)
            return Float(root_math)
        else:
            return Error(_UNSUPPORTED_ARGUMENT_TYPE.format("pow", args[0].type().name))


def parse(*args: Object) -> Object:
    if len(args) != 2:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 2))

    elif not args[0].type() == Object and args[1].type() == String:
        types = [arg.type().name for arg in args]
        return Error(
            _UNSUPPORTED_ARGUMENT_TYPE.format("pow", f"{types[0]} and {types[1]}")
        )

    else:
        arg: Optional[Union[Integer, String, Float, ValueList, ValueTuple]] = None
        type_arg: Type = type(args[0])
        type_parse: str = cast(String, args[1]).inspect()

        if type_arg == Integer and type_parse == "float":
            arg = cast(Integer, args[0])
            return Float(float(arg.value))
        elif type_arg == Integer and type_parse == "str":
            arg = cast(Integer, args[0])
            return String(str(arg.value))
        elif type_arg == Float and type_parse == "int":
            arg = cast(Float, args[0])
            return Integer(int(arg.value))
        elif type_arg == Float and type_parse == "str":
            arg = cast(Float, args[0])
            return String(str(arg.value))
        elif type_arg == ValueList and type_parse == "tuple":
            arg = cast(ValueList, args[0])
            return ValueTuple(arg.values)
        elif type_arg == ValueTuple and type_parse == "list":
            arg = cast(ValueTuple, args[0])
            return ValueList(arg.values)
        elif type_arg == String and type_parse == "list":
            arg = cast(String, args[0])
            return ValueList([String(value_list) for value_list in list(arg.value)])
        else:
            return Error(_PARSE_WRONG.format(args[0].type().name, args[1].inspect()))


def append(*args: Object) -> Object:
    if len(args) == 2:
        
        list_, item = args

        if list_.type() is not ValueList:
            return Error(_UNSUPPORTED_ARGUMENT_TYPE.format(list_.type().name, "ValueList"))

        list_ = cast(ValueList, list_)
        
        
        if len(list_.values) > 0 and type(item) is not type(list_.values[0]):
            return Error(_WRONG_TYPE_APPEND.format(item.type(), list_.values[0].type()))

        list_.values.append(item)

        return list_
    else:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 2))


def get_type(*args: Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 1))

    return String(value=_to_str_type(_get_types(args[0])))


BUILTIN: Dict[str, Builtin] = {
    "length": Builtin(fn=length, io_type="builtin fn (list|tuple|str) -> int"),
    "printLn": Builtin(fn=println, io_type="builtin fn (any) -> null"),
    "not": Builtin(fn=negation_boolean, io_type="builtin fn (bool) -> bool"),
    "pow": Builtin(fn=pow_impure, io_type="builtin fn (int|float, int|float) -> null"),
    "parse": Builtin(
        fn=parse, io_type="builtin fn (int|float|str|list|tuple, str) -> null"
    ),
    "append": Builtin(fn=append, io_type="builtin fn (list, any) -> list"),
    "type": Builtin(fn=get_type, io_type="builtin fn (any) -> str"),
}
