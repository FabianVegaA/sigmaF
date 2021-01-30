from enum import IntEnum

from typing import (
    Callable,
    Dict,
    List,
    Optional
)

from sigmaF.ast import (
    Boolean,
    ExpressionStatement,
    Expression,
    Identifier,
    Integer,
    LetStatement,
    Prefix,
    Infix,
    Program,
    Statement,
    ReturnStatement,
)
from sigmaF.lexer import Lexer
from sigmaF.token import (
    Token,
    TokenType
)

PrefixParseFn = Callable[[], Optional[Expression]]
PrefixParseFns = Dict[TokenType, PrefixParseFn]
InfixParseFn = Callable[[Expression], Optional[Expression]]
IndixParseFns = Dict[TokenType, InfixParseFn]


class Precedence(IntEnum):
    LOWEST = 1
    EQUALS = 2
    LESSGREATER = 3
    SUM = 4
    PRODUCT = 5
    PREFIX = 6
    CALL = 7


PRECEDENCE: Dict[TokenType, Precedence] = {
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
}


class Parser:

    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
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
        error = f'The next token was expected to be of type {token_type} ' + \
            f', but {self._peek_token.token_type} was obtained'

        self._errors.append(error)

    def _parse_expression(self, precedence: Precedence) -> Optional[Expression]:
        assert self._current_token is not None
        try:
            prefix_parse_fn = self._prefix_parse_fns[self._current_token.token_type]
        except KeyError:
            message = f'It was not found nothing funtion for parse {self._current_token.literal}'
            self._errors.append(message)

            return None

        left_expression = prefix_parse_fn()

        assert self._peek_token is not None
        while not self._peek_token.token_type == TokenType.SEMICOLON and precedence < self._peek_precedence():
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
        return Identifier(
            token=self._current_token,
            value=self._current_token.literal
        )

    def _parse_interger(self) -> Optional[Integer]:
        assert self._current_token is not None
        integer = Integer(token=self._current_token)

        try:
            integer.value = int(self._current_token.literal)
        except ValueError:
            message = f'It was not possible to parse {self._current_token.literal} ' + \
                'like Integer.'
            self._errors.append(message)
            return None
        return integer

    def _parse_boolean(self) -> Boolean:
        assert self._current_token is not None

        return Boolean(token=self._current_token,
                       value=self._current_token.token_type == TokenType.TRUE)

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

        # TODO terminar cuando sepamos parsear expresiones
        while self._current_token.token_type != TokenType.SEMICOLON:
            self._advance_tokens()

        return let_statement

    def _parse_return_statement(self) -> Optional[ReturnStatement]:
        assert self._current_token is not None
        return_statement = ReturnStatement(token=self._current_token)

        self._advance_tokens()

        # TODO finish when I know parser expressions
        while self._current_token.token_type != TokenType.SEMICOLON:
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
        prefix_expression = Prefix(token=self._current_token,
                                   operator=self._current_token.literal)

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
        infix = Infix(token=self._current_token,
                      operator=self._current_token.literal,
                      left=left)
        precedence = self._current_precedence()

        self._advance_tokens()

        infix.right = self._parse_expression(precedence)
        return infix

    def _register_infix_fns(self) -> IndixParseFns:
        return {
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

        }

    def _register_prefix_fns(self) -> PrefixParseFns:
        return {
            TokenType.FALSE: self._parse_boolean,
            TokenType.TRUE: self._parse_boolean,
            TokenType.IDENT: self._parse_identifier,
            TokenType.INT: self._parse_interger,
            TokenType.MINUS: self._parse_prefix_expression,
        }
