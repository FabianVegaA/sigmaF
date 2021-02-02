from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Optional,
    List
)
from sigmaF.token import Token


class ASTNode(ABC):

    @abstractmethod
    def token_literal(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Statement(ASTNode):

    def __init__(self, token: Token) -> None:
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal


class Expression(ASTNode):

    def __init__(self, token: Token) -> None:
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal


class Program(ASTNode):

    def __init__(self, statements: List[Statement]) -> None:
        self.statements = statements

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()

        return ''

    # def tree(self) -> None:
    #     for statement in self.statements:
    #         print(f'\n{statement}')

    def __str__(self) -> str:
        out: List[str] = []
        for statement in self.statements:
            out.append(str(statement))

        return ''.join(out)


class Identifier(Expression):

    def __init__(self,
                 token: Token,
                 value: str) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return self.value


class LetStatement(Statement):

    def __init__(self,
                 token: Token,
                 name: Optional[Identifier] = None,
                 value: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f'{self.token_literal()} {str(self.name)} = {str(self.value)};'


class ReturnStatement(Statement):
    def __init__(self,
                 token: Token,
                 return_value: Optional[Expression] = None
                 ) -> None:
        super().__init__(token)
        self.return_value = return_value

    def __str__(self) -> str:
        return f'{self.token_literal()} {self.return_value};'


class ExpressionStatement(Statement):
    def __init__(self,
                 token: Token,
                 expression: Optional[Expression] = None
                 ) -> None:
        super().__init__(token)
        self.expression = expression

    def __str__(self):
        return str(self.expression)


class Integer(Expression):
    def __init__(self,
                 token: Token,
                 value: Optional[int] = None
                 ) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Float(Expression):
    def __init__(self,
                 token: Token,
                 value: Optional[float] = None
                 ) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class String(Expression):
    def __init__(self,
                 token: Token,
                 value: Optional[str] = None
                 ) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Prefix(Expression):

    def __init__(self,
                 token: Token,
                 operator: str,
                 right: Optional[Expression] = None
                 ):
        super().__init__(token)
        self.operator = operator
        self.right = right

    def __str__(self):
        return f'({self.operator}{str(self.right)})'


class Infix(Expression):

    def __init__(self,
                 token: Token,
                 left: Expression,
                 operator: str,
                 right: Optional[Expression] = None
                 ) -> None:
        super().__init__(token)
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f'({str(self.left)} {self.operator} {str(self.right)})'


class Boolean(Expression):

    def __init__(self,
                 token: Token,
                 value: Optional[bool] = None
                 ) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self):
        return self.token_literal()


class Block(Statement):
    def __init__(self,
                 token: Token,
                 statements: List[Statement]
                 ) -> None:
        super().__init__(token)
        self.statements = statements

    def __str__(self) -> str:
        out: List[str] = [str(statement) for statement in self.statements]

        return ' '.join(out)


class If(Expression):

    def __init__(self,
                 token: Token,
                 condition: Optional[Expression] = None,
                 consequence: Optional[Block] = None,
                 alternative: Optional[Block] = None,
                 ) -> None:
        super().__init__(token)
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self) -> str:
        out: str = f'if {str(self.condition)} {str(self.consequence)}'

        if self.alternative:
            out += f' else {str(self.alternative)}'

        return out


class Function(Expression):

    def __init__(self,
                 token: Token,
                 parameters: List[Identifier] = [],
                 type_parameters: List[Identifier] = [],
                 type_output: Optional[str] = None,
                 body: Optional[Block] = None
                 ) -> None:
        super().__init__(token)
        self.parameters = parameters
        self.type_parameters = type_parameters
        self.type_output = type_output
        self.body = body

    def __str__(self) -> str:
        param_and_type_list: List[str] = [f'{parameter}::{type_parameter}' for parameter, type_parameter in zip(
            self.parameters, self.type_parameters)]

        params: str = ', '.join(param_and_type_list)

        return f'function: {params} -> {str(self.type_output)} {str(self.body)} '


class Call(Expression):

    def __init__(self,
                 token: Token,
                 function: Expression,
                 arguments: Optional[List[Expression]] = None
                 ) -> None:
        super().__init__(token)
        self.function = function
        self.arguments = arguments

    def __str__(self) -> str:
        assert self.arguments is not None
        arg_list: List[str] = [str(argument) for argument in self.arguments]
        args: str = ', '.join(arg_list)

        return f'{str(self.function)}({args})'
