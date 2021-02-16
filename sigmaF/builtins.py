import math
from typing import (
    cast,
    Dict,
    Type,
    Union,
    Optional
)

from sigmaF.object import (
    Boolean,
    Builtin,
    Float,
    Function,
    Error,
    Integer,
    ValueList,
    Null,
    Object,
    String
)

_WRONG_NUMBER_OF_ARGS = 'Incorrect Number of arguments for length, it was received {} arguments, and is needed only {}'
_UNSUPPORTED_ARGUMENT_TYPE = 'Argument to {} without support, it was received a {}'
_PARSE_WRONG = 'It is not possible to parser since {} to {}'


def length(*args: Object) -> Object:

    argument: Optional[Union[String, ValueList]] = None
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 1))
    elif type(args[0]) == String:
        argument = cast(String, args[0])
        return Integer(len(argument.value))
    elif type(args[0]) == ValueList:
        argument = cast(ValueList, args[0])
        return Integer(len(argument.values))
    else:
        return Error(_UNSUPPORTED_ARGUMENT_TYPE.format('length', args[0].type().name))


def printLn(*args: Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 1))
    else:
        type_arg: Type = type(args[0])
        argument: Optional[Union[String, Integer,
                                 Float, Boolean, ValueList, Function]] = None
        if type_arg == String:
            argument = cast(String, args[0])
            print(argument.inspect())

        elif type_arg == Integer:
            argument = cast(Integer, args[0])
            print(argument.inspect())

        elif type_arg == Float:
            argument = cast(Float, args[0])
            print(argument.inspect())

        elif type_arg == ValueList:
            argument = cast(ValueList, args[0])
            print(argument.inspect())

        elif type_arg == Boolean:
            argument = cast(Boolean, args[0])
            print(argument.inspect())

        elif type_arg == Function:
            argument = cast(Function, args[0])
            print(argument.inspect())

        else:
            print('----->', args[0])
            return Error(_UNSUPPORTED_ARGUMENT_TYPE.format('printLn', args[0].type().name))

        return Null()


def negation_bolean(*args: Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 1))
    else:
        type_arg: Type = type(args[0])
        argument: Optional[Boolean] = None

        if type_arg == Boolean:
            argument = cast(Boolean, args[0])
            return Boolean(not argument.value)
        else:
            return Error(_UNSUPPORTED_ARGUMENT_TYPE.format('not', args[0].type().name))


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
            return Error(_UNSUPPORTED_ARGUMENT_TYPE.format('pow', args[0].type().name))


def parse(*args: Object) -> Object:
    if len(args) != 2:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 2))

    elif not args[0].type() == Object and args[1].type() == String:
        types = [arg.type().name for arg in args]
        return Error(_UNSUPPORTED_ARGUMENT_TYPE.format(
            'pow', f'{types[0]} and {types[1]}'))

    else:
        arg: Optional[Union[Integer, String, Float, ValueList]] = None
        type_arg: Type = type(args[0])
        type_parse: str = cast(String, args[1]).inspect()

        if type_arg == Integer and type_parse == "float":
            arg = cast(Integer, args[0])
            return Float(float(arg.value))
        elif type_arg == String and type_parse == "list":
            arg = cast(String, args[0])
            return ValueList([String(value_list) for value_list in list(arg.value)])
        else:
            return Error(_PARSE_WRONG.format(args[0].type().name, args[1].inspect()))


BUILTIN: Dict[str, Builtin] = {
    'length': Builtin(fn=length),
    'printLn': Builtin(fn=printLn),
    'not': Builtin(fn=negation_bolean),
    'pow': Builtin(fn=pow_impure),
    'parse': Builtin(fn=parse),
}
