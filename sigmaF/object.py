from abc import (
    ABC,
    abstractmethod,
)
from enum import (
    auto,
    Enum,
)
from typing import (
    Any
)


class ObjectType(Enum):
    BOOLEAN = auto()
    FLOAT = auto()
    INTEGER = auto()
    NULL = auto()
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


# TODO To create the nullable class, this will be able to evaluate for example 'int?' or 'bool?'
