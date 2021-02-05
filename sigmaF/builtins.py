from typing import (
    cast,
    Dict
)

from sigmaF.object import (
    Builtin,
    Error,
    Integer,
    Object,
    String
)

_WRONG_NUMBER_OF_ARGS = 'Incorrect Number of arguments for length, it was received {} arguments, and is needed only {}'
_UNSUPPORTED_ARGUMENT_TYPE = 'Argument to {} without support, it was received a {}'


def length(*args: Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 1))
    elif type(args[0]) == String:
        argument = cast(String, args[0])
        return Integer(len(argument.value))
    else:
        return Error(_UNSUPPORTED_ARGUMENT_TYPE.format('length', args[0].type().name))


BUILTIN: Dict[str, Builtin] = {
    'length': Builtin(fn=length)
}
