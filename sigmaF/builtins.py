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
            print('----->',args[0])
            return Error(_UNSUPPORTED_ARGUMENT_TYPE.format('printLn', args[0].type().name))

        return Null()


BUILTIN: Dict[str, Builtin] = {
    'length': Builtin(fn=length),
    'printLn': Builtin(fn=printLn),
}
