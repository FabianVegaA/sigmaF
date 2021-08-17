from enum import IntEnum

from typing import Callable, Dict, List, Tuple, Optional

from sigmaF.ast import (
    Block,
    Boolean,
    Call,
    CallList,
    Function,
    ExpressionStatement,
    Expression,
    Identifier,
    If,
    Integer,
    Float,
    LetStatement,
    ListValues,
    Void,
    TupleValues,
    Prefix,
    Infix,
    Program,
    Statement,
    String,
    ReturnStatement,
)
from sigmaF.lexer import Lexer
from sigmaF.token import Token, TokenType

PrefixParseFn = Callable[[], Optional[Expression]]
PrefixParseFns = Dict[TokenType, PrefixParseFn]
InfixParseFn = Callable[[Expression], Optional[Expression]]
IndixParseFns = Dict[TokenType, InfixParseFn]


class Precedence(IntEnum):
    LOWEST = 1
    AND = 2
    EQUALS = 3
    LESSGREATER = 4
    SUM = 5
    PRODUCT = 6
    POW = 7
    PREFIX = 8
    CALL = 9


PRECEDENCE: Dict[TokenType, Precedence] = {
    TokenType.AND: Precedence.AND,
    TokenType.OR: Precedence.AND,

    TokenType.EQ: Precedence.EQUALS,
    TokenType.NOT_EQ: Precedence.EQUALS,

    TokenType.LT: Precedence.LESSGREATER,
    TokenType.GT: Precedence.LESSGREATER,
    TokenType.L_OR_EQ_T: Precedence.LESSGREATER,
    TokenType.G_OR_EQ_T: Precedence.LESSGREATER,

    TokenType.PLUS: Precedence.SUM,
    TokenType.MINUS: Precedence.SUM,

    TokenType.DIVISION: Precedence.PRODUCT,
    TokenType.MODULUS: Precedence.PRODUCT,
    TokenType.MULTIPLICATION: Precedence.PRODUCT,

    TokenType.EXPONENTIATION: Precedence.POW,

    TokenType.LPAREN: Precedence.CALL,
    TokenType.LBRAKET: Precedence.CALL,

}


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._old_token: Optional[Token] = None
        self._current_token: Optional[Token] = None
        self._peek_token: Optional[Token] = None
        self._errors: List[str] = []

        self._prefix_parse_fns: PrefixParseFns = self._register_prefix_fns()
        self._infix_parse_fns: IndixParseFns = self._register_infix_fns()

        self._advance_tokens()
        self._advance_tokens()

    @property
    def errors(self) -> List[str]:
        return self._errors

    def parse_program(self) -> Program:
        program: Program = Program(statements=[])

        assert self._current_token is not None
        while self._current_token.token_type != TokenType.EOF:
            statement = self._parse_statement()
            if statement is not None:
                program.statements.append(statement)

            self._advance_tokens()

        return program

    def _advance_tokens(self) -> None:
        self._old_token = self._current_token
        self._current_token = self._peek_token
        self._peek_token = self._lexer.next_token()

    def _expected_token(self, token_type: TokenType) -> bool:
        assert self._peek_token is not None
        if self._peek_token.token_type == token_type:
            self._advance_tokens()

            return True

        self._expected_token_error(token_type)
        return False

    def _expected_token_error(self, token_type: TokenType) -> None:
        assert self._peek_token is not None
        error = (
            f"The next token was expected to be of type {token_type} "
            + f", but {self._peek_token.token_type} was obtained"
        )

        self._errors.append(error)

    def _parse_expression(self, precedence: Precedence) -> Optional[Expression]:
        assert self._current_token is not None
        try:
            prefix_parse_fn = self._prefix_parse_fns[self._current_token.token_type]
        except KeyError:
            message = f"It was not found nothing funtion for parse {self._current_token.literal}"
            self._errors.append(message)

            return None

        left_expression = prefix_parse_fn()

        assert self._peek_token is not None
        while (
            not self._peek_token.token_type == TokenType.SEMICOLON
            and precedence < self._peek_precedence()
        ):
            try:
                infix_parse_fn = self._infix_parse_fns[self._peek_token.token_type]

                self._advance_tokens()

                assert left_expression is not None
                left_expression = infix_parse_fn(left_expression)
            except KeyError:
                return left_expression

        return left_expression

    def _parse_identifier(self) -> Identifier:
        assert self._current_token is not None
        return Identifier(token=self._current_token, value=self._current_token.literal)

    def _parse_interger(self) -> Optional[Integer]:
        assert self._current_token is not None
        integer = Integer(token=self._current_token)

        try:
            integer.value = int(self._current_token.literal)
        except ValueError:
            message = (
                f"It was not possible to parse {self._current_token.literal} "
                + "like Integer."
            )
            self._errors.append(message)
            return None
        return integer

    def _parse_float(self) -> Optional[Float]:
        assert self._current_token is not None
        floating = Float(token=self._current_token)

        try:
            floating.value = float(self._current_token.literal)
        except ValueError:
            message = (
                f"It was not possible to parse {self._current_token.literal} "
                + "like Floating."
            )
            self._errors.append(message)
            return None
        return floating

    def _parse_string(self) -> Optional[String]:
        assert self._current_token is not None
        string = String(token=self._current_token)

        try:
            string.value = str(self._current_token.literal)
        except ValueError:
            message = (
                f"It was not possible to parse {self._current_token.literal} "
                + "like String."
            )
            self._errors.append(message)
            return None
        return string

    def _parse_boolean(self) -> Boolean:
        assert self._current_token is not None

        return Boolean(
            token=self._current_token,
            value=self._current_token.token_type == TokenType.TRUE,
        )

    def _parse_null(self) -> Void:
        assert self._current_token is not None

        return Void(token=self._current_token)

    def _parse_expression_statements(self) -> Optional[ExpressionStatement]:
        assert self._current_token is not None
        expression_statement = ExpressionStatement(token=self._current_token)

        expression_statement.expression = self._parse_expression(
            Precedence.LOWEST)

        assert self._peek_token is not None
        if self._peek_token.token_type == TokenType.SEMICOLON:
            self._advance_tokens()

        return expression_statement

    def _parse_let_statement(self) -> Optional[LetStatement]:
        assert self._current_token is not None
        let_statement = LetStatement(token=self._current_token)

        if not self._expected_token(TokenType.IDENT):
            return None

        let_statement.name = self._parse_identifier()
        if not self._expected_token(TokenType.ASSIGN):
            return None

        self._advance_tokens()

        let_statement.value = self._parse_expression(Precedence.LOWEST)

        assert self._peek_token is not None
        if self._peek_token.token_type == TokenType.SEMICOLON:
            self._advance_tokens()

        return let_statement

    def _parse_return_statement(self) -> Optional[ReturnStatement]:
        assert self._current_token is not None
        return_statement = ReturnStatement(token=self._current_token)

        self._advance_tokens()

        return_statement.return_value = self._parse_expression(
            Precedence.LOWEST)
        assert self._peek_token is not None
        if self._peek_token.token_type == TokenType.SEMICOLON:
            self._advance_tokens()

        return return_statement

    def _parse_statement(self) -> Optional[Statement]:
        assert self._current_token is not None
        if self._current_token.token_type == TokenType.LET:
            return self._parse_let_statement()
        elif self._current_token.token_type == TokenType.RETURN:
            return self._parse_return_statement()
        else:
            return self._parse_expression_statements()

    def _parse_prefix_expression(self) -> Prefix:
        assert self._current_token is not None
        prefix_expression = Prefix(
            token=self._current_token, operator=self._current_token.literal
        )

        self._advance_tokens()

        prefix_expression.right = self._parse_expression(Precedence.PREFIX)

        return prefix_expression

    def _current_precedence(self) -> Precedence:
        assert self._current_token is not None
        try:
            return PRECEDENCE[self._current_token.token_type]
        except KeyError:
            return Precedence.LOWEST

    def _peek_precedence(self) -> Precedence:
        assert self._peek_token is not None
        try:
            return PRECEDENCE[self._peek_token.token_type]
        except KeyError:
            return Precedence.LOWEST

    def _parse_infix_expression(self, left: Expression) -> Infix:
        assert self._current_token is not None
        infix = Infix(
            token=self._current_token, operator=self._current_token.literal, left=left
        )
        precedence = self._current_precedence()

        self._advance_tokens()

        infix.right = self._parse_expression(precedence)
        return infix

    def _parse_block(self) -> Block:
        assert self._current_token is not None
        block_statements = Block(token=self._current_token, statements=[])

        self._advance_tokens()

        while (
            not self._current_token.token_type == TokenType.RBRACE
            and not self._current_token.token_type == TokenType.EOF
        ):
            statement = self._parse_statement()
            if statement:
                block_statements.statements.append(statement)

            self._advance_tokens()

        return block_statements

    def _parse_call(self, function: Expression) -> Call:
        assert self._current_token is not None
        call = Call(self._current_token, function)
        call.arguments = self._parse_call_arguments()

        return call

    def _parse_call_arguments(self) -> Optional[List[Expression]]:
        arguments: List[Expression] = []

        assert self._peek_token is not None
        if self._peek_token.token_type == TokenType.RPAREN:
            self._advance_tokens()

            return None

        self._advance_tokens()
        if expression := self._parse_expression(Precedence.LOWEST):
            arguments.append(expression)

        while self._peek_token.token_type == TokenType.COMMA:
            self._advance_tokens()
            self._advance_tokens()

            if expression := self._parse_expression(Precedence.LOWEST):
                arguments.append(expression)
        if not self._expected_token(TokenType.RPAREN):
            return None

        return arguments

    def _parse_if(self) -> Optional[If]:
        assert self._current_token is not None
        if_expression = If(token=self._current_token)

        self._advance_tokens()

        if_expression.condition = self._parse_expression(Precedence.LOWEST)

        if not self._expected_token(TokenType.THEN):
            return None

        if not self._expected_token(TokenType.LBRACE):
            return None

        if_expression.consequence = self._parse_block()

        if (
            self._peek_token is not None
            and self._peek_token.token_type == TokenType.ELSE
        ):
            self._advance_tokens()

            if not self._expected_token(TokenType.LBRACE):
                return None

            if_expression.alternative = self._parse_block()

        return if_expression

    def _parse_function(self) -> Optional[Function]:
        assert self._current_token is not None
        function = Function(token=self._current_token)

        if not self._expected_token(TokenType.IDENT):
            return None

        (
            function.parameters,
            function.type_parameters,
            function.type_output,
        ) = self._parse_function_parameters()

        if not self._expected_token(TokenType.LBRACE):
            return None

        function.body = self._parse_block()

        return function

    def _parse_function_parameters(
        self,
    ) -> Tuple[List[Identifier], List[Identifier], Optional[Identifier]]:
        params: List[Identifier] = []
        type_params: List[Identifier] = []

        assert self._current_token is not None
        identifier = Identifier(
            token=self._current_token, value=self._current_token.literal
        )
        params.append(identifier)

        assert self._peek_token is not None
        assert self._peek_token.token_type is TokenType.TYPEASSIGN
        self._advance_tokens()
        self._advance_tokens()
        identifier = Identifier(
            token=self._current_token, value=self._current_token.literal
        )
        type_params.append(identifier)

        while self._peek_token.token_type == TokenType.COMMA:
            self._advance_tokens()
            self._advance_tokens()

            identifier = Identifier(
                token=self._current_token, value=self._current_token.literal
            )
            params.append(identifier)

            assert self._peek_token is not None
            assert self._peek_token.token_type is TokenType.TYPEASSIGN
            self._advance_tokens()
            self._advance_tokens()
            assert self._peek_token.token_type is not TokenType.CLASSNAME
            identifier = Identifier(
                token=self._current_token, value=self._current_token.literal
            )
            type_params.append(identifier)

        if not self._expected_token(TokenType.OUTPUTFUNTION):
            return ([], [], None)

        assert self._peek_token.token_type is TokenType.CLASSNAME 
        self._advance_tokens()
        type_output: Identifier = Identifier(
            self._current_token, self._current_token.literal
        )

        return params, type_params, type_output

    def _parse_grouped_expression(self) -> Optional[Expression]:
        expression = self._parse_expression(Precedence.LOWEST)
        if self._peek_token is not None and self._peek_token.token_type is TokenType.COMMA:
            return self._parse_tuple(expression)
        if not self._expected_token(TokenType.RPAREN):
            return None

        return expression

    def _parse_tuple(self, fst_value: Optional[Expression]) -> Optional[Expression]:
        assert self._current_token is not None
        tuple_values = TupleValues(token=Token(TokenType.COMMA, "("))

        values = [fst_value]

        self._advance_tokens()

        while self._current_token.token_type == TokenType.COMMA:
            self._advance_tokens()

            if expression := self._parse_expression(Precedence.LOWEST):
                values.append(expression)

                self._advance_tokens()

        if self._current_token.token_type is not TokenType.RPAREN:
            return None

        tuple_values.values = values

        return tuple_values

    def _parse_paren(self) -> Optional[Expression]:
        assert self._current_token is not None and self._peek_token is not None

        self._advance_tokens()

        return self._parse_grouped_expression()

    def _parse_list(self) -> Optional[ListValues]:
        assert self._current_token is not None
        list_values = ListValues(token=self._current_token)

        self._advance_tokens()

        if self._current_token.token_type == TokenType.RBRAKET:
            return list_values

        values = []
        allow_types = [
            TokenType.INT,
            TokenType.FLOAT,
            TokenType.STRING,
            TokenType.TRUE,
            TokenType.FALSE,
            TokenType.IDENT,
            TokenType.FUNCTION,
            TokenType.LBRAKET,
            TokenType.LPAREN,
            TokenType.RPAREN,
            TokenType.MINUS,
        ]

        if self._current_token.token_type not in allow_types:
            return None

        token_type = self._current_token.token_type

        if expression := self._parse_expression(Precedence.LOWEST):
            values.append(expression)

        self._advance_tokens()
        while self._current_token.token_type == TokenType.COMMA:

            self._advance_tokens()

            if self._current_token.token_type != token_type:
                return None

            if expression := self._parse_expression(Precedence.LOWEST):
                values.append(expression)

                self._advance_tokens()

        if self._current_token.token_type is not TokenType.RBRAKET:
            return None
        list_values.values = values

        return list_values

    def _parse_call_list(self, value_list: Expression) -> CallList:
        assert self._current_token is not None
        call_list = CallList(self._current_token, value_list)
        call_list.range = self._parse_call_list_arguments()

        return call_list

    def _parse_call_list_arguments(self) -> Optional[List[Expression]]:
        ranges: List[Expression] = []

        assert self._peek_token is not None
        if self._peek_token.token_type == TokenType.RBRAKET:
            self._advance_tokens()

            return None
        self._advance_tokens()
        if expression := self._parse_expression(Precedence.LOWEST):
            ranges.append(expression)
        while self._peek_token.token_type == TokenType.COMMA:
            self._advance_tokens()
            self._advance_tokens()

            if expression := self._parse_expression(Precedence.LOWEST):
                ranges.append(expression)
        if not self._expected_token(TokenType.RBRAKET):
            return None

        return ranges

    def _register_infix_fns(self) -> IndixParseFns:
        return {
            TokenType.EXPONENTIATION: self._parse_infix_expression,
            TokenType.PLUS: self._parse_infix_expression,
            TokenType.MINUS: self._parse_infix_expression,
            TokenType.DIVISION: self._parse_infix_expression,
            TokenType.MULTIPLICATION: self._parse_infix_expression,
            TokenType.MODULUS: self._parse_infix_expression,
            TokenType.EQ: self._parse_infix_expression,
            TokenType.NOT_EQ: self._parse_infix_expression,
            TokenType.LT: self._parse_infix_expression,
            TokenType.GT: self._parse_infix_expression,
            TokenType.L_OR_EQ_T: self._parse_infix_expression,
            TokenType.G_OR_EQ_T: self._parse_infix_expression,
            TokenType.LPAREN: self._parse_call,
            TokenType.LBRAKET: self._parse_call_list,
            TokenType.AND: self._parse_infix_expression,
            TokenType.OR: self._parse_infix_expression,
        }

    def _register_prefix_fns(self) -> PrefixParseFns:
        return {
            TokenType.FUNCTION: self._parse_function,
            TokenType.IF: self._parse_if,
            TokenType.LPAREN: self._parse_paren,
            TokenType.LBRAKET: self._parse_list,
            TokenType.RBRAKET: self._parse_list,
            TokenType.FALSE: self._parse_boolean,
            TokenType.TRUE: self._parse_boolean,
            TokenType.IDENT: self._parse_identifier,
            TokenType.INT: self._parse_interger,
            TokenType.FLOAT: self._parse_float,
            TokenType.STRING: self._parse_string,
            TokenType.NULL: self._parse_null,
            TokenType.MINUS: self._parse_prefix_expression,
        }
