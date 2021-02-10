from abc import (
    ABC,
    abstractmethod,
)
from enum import (
    auto,
    Enum,
)
from typing import (
    Any,
    Dict,
    List,
    Optional
)

from typing_extensions import Protocol

from sigmaF.ast import (
    Block,
    Identifier
)


class ObjectType(Enum):
    BOOLEAN = auto()
    BUILTING = auto()
    FLOAT = auto()
    FUNCTION = auto()
    ERROR = auto()
    INTEGER = auto()
    LIST = auto()
    NULL = auto()
    RETURN = auto()
    STRING = auto()


class Object(ABC):

    @abstractmethod
    def type(self) -> ObjectType:
        pass

    @abstractmethod
    def inspect(self) -> str:
        pass


class Integer(Object):

    def __init__(self, value: int) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.INTEGER

    def inspect(self) -> str:
        return str(self.value)


class Float(Object):

    def __init__(self, value: float) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.FLOAT

    def inspect(self) -> str:
        return str(self.value)


class String(Object):

    def __init__(self, value: str) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.STRING

    def inspect(self) -> str:
        return str(self.value)


class Boolean(Object):

    def __init__(self, value: bool) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.BOOLEAN

    def inspect(self) -> str:
        return 'true' if self.value else 'false'


class Null(Object):

    def type(self) -> ObjectType:
        return ObjectType.INTEGER

    def inspect(self) -> str:
        return 'null'


class Error(Object):

    def __init__(self, message: str) -> None:
        self.message = message

    def type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return f' Error: {self.message}'


class Return(Object):

    def __init__(self, value: Object) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.RETURN

    def inspect(self) -> str:
        return self.value.inspect()


class Environment(Dict):

    def __init__(self, outer=None):
        self._store = dict()
        self._outer = outer

    def __getitem__(self, key):
        try:
            return self._store[key]
        except KeyError as e:
            if self._outer is not None:
                return self._outer[key]

            raise e

    def __setitem__(self, key, value):
        self._store[key] = value

    def __delitem__(self, key):
        del self._store[key]


class Function(Object):

    def __init__(self,
                 parameters: List[Identifier],
                 type_parameters: List[Identifier],
                 type_output: Optional[Identifier],
                 body: Block,
                 env: Environment
                 ) -> None:
        self.parameters = parameters
        self.type_parameters = type_parameters
        self.type_output = type_output
        self.body = body
        self.env = env

    def type(self) -> ObjectType:
        return ObjectType.FUNCTION

    def inspect(self) -> str:
        params_and_types: str = ', '.join([f'{param}::{type_param}' for param, type_param in zip(
            self.parameters, self.type_parameters)])

        return f'fn {params_and_types} -> {self.type_output} {{\n\t{self.body}\n}}'


class BuiltinFunction(Protocol):

    def __call__(self, *args: Object) -> Object: ...


class Builtin(Object):

    def __init__(self, fn: BuiltinFunction) -> None:
        self.fn = fn

    def type(self) -> ObjectType:
        return ObjectType.BUILTING

    def inspect(self) -> str:
        return 'builtin function'


class ValueList(Object):

    def __init__(self, values: List[Object] = []) -> None:
        self.values = values

    def type(self) -> ObjectType:
        return ObjectType.LIST

    def inspect(self) -> str:
        values_list: List[str] = [value.inspect() for value in self.values]
        
        if len(self.values) > 0 and self.values[0].type() is ObjectType.STRING:
            return ('[\"' + '\", \"'.join(values_list) + '\"]')
        
        return ('[' + ', '.join(values_list) + ']')


# TODO To create the nullable class, this will be able to evaluate for example 'int?' or 'bool?'
