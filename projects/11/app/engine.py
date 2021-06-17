from typing import Optional

from app.constants import *
from app.simbol_table import *
from app.tokenizer import Token, Tokenizer
from app.vm_writer import *


class CompileEngine:
    def __init__(self, tokenizer: Tokenizer, vm_file: TextIO, name: str):
        self.vm_writer = VMWriter(vm_file, name)
        self.tokenizer = tokenizer
        self.symbol_table = SymbolTable()
        self.func_type = ""
        self.class_name = name
        self.if_count = 0
        self.while_count = 0

    def compile(self) -> None:
        self.tokenizer.next_token()  # class
        self.tokenizer.next_token()  # name
        self.tokenizer.next_token()  # {
        next_token = self.tokenizer.next_token()
        while next_token.additional_info == CLASS_VAR_DEC_TAG_NAME:
            self.compile_variable(next_token)
            next_token = self.tokenizer.next_token()
        while next_token.additional_info == SUBROUTINE_DEC_TAG_NAME:
            self.compile_subroutine(next_token)
            next_token = self.tokenizer.next_token()

    def compile_variable(self, token: Token) -> None:
        s_kind = token.value  # field | static | var
        s_type = self.tokenizer.next_token().value
        s_name = self.tokenizer.next_token().value
        self.symbol_table.define(s_name, s_type, s_kind)
        next_token = self.tokenizer.next_token()
        while next_token.value == ",":
            s_name = self.tokenizer.next_token().value  # name
            self.symbol_table.define(s_name, s_type, s_kind)
            next_token = self.tokenizer.next_token()  # , or ;

    def compile_subroutine(self, next_token: Token) -> None:
        self.symbol_table.start_subroutine()
        # function | method | constructor
        self.func_type = next_token.value
        self.tokenizer.next_token()  # return type
        func_name = self.tokenizer.next_token().value  # name
        self.tokenizer.next_token()  # (
        self.compile_parameters()
        self.compile_subroutine_body(func_name)
        self.symbol_table.end_sub_routine()

    def compile_parameters(self) -> None:
        next_token = self.tokenizer.next_token()
        if next_token.value == ")":
            return
        s_type = next_token.value  # type
        s_name = self.tokenizer.next_token().value  # name
        if self.func_type == METHOD:
            self.symbol_table.define(THIS, s_type, ARG_KIND)
        self.symbol_table.define(s_name, s_type, ARG_KIND)
        next_token = self.tokenizer.next_token()
        while next_token.value != ")":
            s_type = self.tokenizer.next_token().value  # type
            s_name = self.tokenizer.next_token().value  # name
            self.symbol_table.define(s_name, s_type, ARG_KIND)
            next_token = self.tokenizer.next_token()

    def compile_subroutine_body(self, func_name: str) -> None:
        self.tokenizer.next_token()
        next_token = self.tokenizer.peek_next_token()
        if next_token.value == "}":
            return
        while next_token.additional_info == VAR_DEC_TAG_NAME:
            next_token = self.tokenizer.next_token()
            self.compile_variable(next_token)
            next_token = self.tokenizer.peek_next_token()
        self.vm_writer.function(func_name, self.symbol_table.var_count(VAR_KIND))
        if self.func_type == CONSTRUCTOR:
            self.symbol_table.end_sub_routine()
            self.vm_writer.push(CONST, self.symbol_table.var_count(FIELD_KIND))
            self.vm_writer.call("Memory.alloc", 1)
            self.vm_writer.pop(POINTER, 0)
            self.symbol_table.start_sub()
        elif self.func_type == METHOD:
            self.vm_writer.push(ARG, 0)
            self.vm_writer.pop(POINTER, 0)
        if next_token.additional_info in STATEMENTS:
            next_token = self.tokenizer.next_token()
            self.compile_statements(next_token)
            self.tokenizer.peek_next_token()

    def compile_statements(self, token: Token) -> None:
        while token.value != "}":
            if token.additional_info == LET_TAG_NAME:
                self.compile_let()
            elif token.additional_info == IF_TAG_NAME:
                self.compile_if()
            elif token.additional_info == WHILE_TAG_NAME:
                self.compile_while()
            elif token.additional_info == DO_TAG_NAME:
                self.compile_do()
            elif token.additional_info == RETURN_TAG_NAME:
                self.compile_return()
            token = self.tokenizer.next_token()

    def compile_if(self) -> None:
        self.tokenizer.next_token()
        token = self.tokenizer.next_token()
        self.compile_expression(token)
        self.tokenizer.next_token()
        self.vm_writer.arithmetic("~")
        self.if_count += 1
        first_label = IF_FALSE + str(self.if_count)
        self.vm_writer.w_if(first_label)
        self.tokenizer.next_token()
        token = self.tokenizer.next_token()
        if token.value != "}":
            self.compile_statements(token)
        second_label = IF_END + str(self.if_count)
        self.if_count += 1
        self.vm_writer.goto(second_label)
        self.vm_writer.label(first_label)
        token = self.tokenizer.peek_next_token()
        if token.additional_info == ELSE:
            self.tokenizer.next_token()  # else
            self.tokenizer.next_token()  # {
            token = self.tokenizer.next_token()
            self.compile_statements(token)
        self.vm_writer.label(second_label)

    def compile_while(self) -> None:
        first_label = WHILE_EXP + str(self.while_count)
        second_label = WHILE_END + str(self.while_count)
        self.while_count += 1
        self.vm_writer.label(first_label)
        self.tokenizer.next_token()  # (
        token = self.tokenizer.next_token()
        self.compile_expression(token)
        self.vm_writer.arithmetic("~")
        self.vm_writer.w_if(second_label)
        self.tokenizer.next_token()  # )
        self.tokenizer.next_token()  # {
        token = self.tokenizer.next_token()
        self.compile_statements(token)
        self.vm_writer.goto(first_label)
        self.vm_writer.label(second_label)

    def push_variable(self, s_name: str) -> None:
        kind = self.symbol_table.kind_of(s_name)
        if kind == ARG_KIND:
            self.vm_writer.push(ARG, self.symbol_table.index_of(s_name))
        elif kind == VAR_KIND:
            self.vm_writer.push(LOCAL, self.symbol_table.index_of(s_name))
        else:
            self.symbol_table.end_sub_routine()
            if self.symbol_table.kind_of(s_name) != NONE_KIND:
                self.vm_writer.push(THIS, self.symbol_table.index_of(s_name))
            self.symbol_table.start_sub()

    def multiplexer(self, is_arr: bool, s_name: str, type: str):
        if is_arr:
            self.write_array()
        else:
            self.vm_writer.pop(type, self.symbol_table.index_of(s_name))

    def compile_let(self) -> None:

        s_name = self.tokenizer.next_token().value  # variable name
        is_arr = False
        next_token = self.tokenizer.next_token()
        if next_token.value == "[":
            is_arr = True
            self.push_variable(s_name)  # array name
            token = self.tokenizer.next_token()
            self.compile_expression(token)
            self.vm_writer.arithmetic("+")
            self.tokenizer.next_token()  # ]

            self.tokenizer.next_token()

        token = self.tokenizer.next_token()
        self.compile_expression(token)

        self.tokenizer.next_token()  # ;
        kind = self.symbol_table.kind_of(s_name)
        if kind == ARG_KIND:
            self.multiplexer(is_arr, s_name, ARG)
        elif kind == VAR_KIND:
            self.multiplexer(is_arr, s_name, LOCAL)
        elif kind == NONE_KIND:
            self.symbol_table.end_sub_routine()
            class_kind = self.symbol_table.kind_of(s_name)
            if class_kind == STATIC_KIND:
                self.vm_writer.pop(STATIC, self.symbol_table.index_of(s_name))
            else:
                assert class_kind == FIELD_KIND
                self.multiplexer(is_arr, s_name, THIS)
            self.symbol_table.start_sub()

    def compile_do(self) -> None:
        s_name = self.tokenizer.next_token().value  # name
        token = self.tokenizer.next_token()
        if token.value == "(":
            if self.func_type == CONSTRUCTOR:
                self.vm_writer.push(POINTER, 0)
            elif self.func_type == METHOD:
                self.vm_writer.push(POINTER, 0)
            num_arg = self.compile_expression_list()
            if self.func_type != FUNCTION:
                self.vm_writer.call(self.class_name + "." + s_name, num_arg + 1)
        elif token.value == ".":
            func_name = self.tokenizer.next_token().value  # fun name
            self.push_object(s_name)
            self.tokenizer.next_token()  # (
            num_arg = self.compile_expression_list()
            self.call(s_name, func_name, num_arg)

        self.tokenizer.next_token()  # )
        self.tokenizer.next_token()  # ;
        self.vm_writer.pop(TEMP, 0)

    def compile_return(self) -> None:
        next_token = self.tokenizer.next_token()
        if next_token.value != ";":
            self.compile_expression(next_token)
            self.tokenizer.next_token()
        else:
            self.vm_writer.push(CONST, 0)
        self.vm_writer.w_return()

    def push_keyword(self, keyword: str) -> None:
        if keyword == NULL or keyword == FALSE:
            self.vm_writer.push(CONST, 0)
        elif keyword == TRUE:
            self.vm_writer.push(CONST, 0)
            self.vm_writer.arithmetic("~")
        elif keyword == THIS:
            self.vm_writer.push(POINTER, 0)

    def push_string(self, string: str) -> None:
        self.vm_writer.push(CONST, len(string))
        self.vm_writer.call("String.new", 1)
        for ch in string:
            self.vm_writer.push(CONST, ord(ch))
            self.vm_writer.call("String.appendChar", 2)

    def push_symbol(self, symbol: str, additional_info: Optional[str]) -> None:
        if additional_info == UNARY_OPERATOR:
            operator = symbol
            token = self.tokenizer.next_token()
            self.compile_term(token)
            if operator == "-":  # neg
                self.vm_writer.arithmetic("!")
            else:
                self.vm_writer.arithmetic(operator)
        elif symbol == "(":
            token = self.tokenizer.next_token()
            self.compile_expression(token)
            self.tokenizer.next_token()
        else:
            token = self.tokenizer.next_token()
            self.compile_expression(token)

    def push_only_identifier(self, identifier: str):
        kind = self.symbol_table.kind_of(identifier)
        if kind == ARG_KIND:
            self.vm_writer.push(ARG, self.symbol_table.index_of(identifier))
        elif kind == VAR_KIND:
            self.vm_writer.push(LOCAL, self.symbol_table.index_of(identifier))
        elif kind == NONE_KIND:
            self.symbol_table.end_sub_routine()
            kind = self.symbol_table.kind_of(identifier)
            if kind == STATIC_KIND:
                self.vm_writer.push(STATIC, self.symbol_table.index_of(identifier))
            elif kind == FIELD_KIND:
                self.vm_writer.push(THIS, self.symbol_table.index_of(identifier))
            else:
                assert False
            self.symbol_table.start_sub()

    def push_identifier(self, identifier: str) -> None:
        token = self.tokenizer.peek_next_token()
        if token.value == ".":
            self.tokenizer.next_token()  # .
            self.push_object(identifier)
            func_name = self.tokenizer.next_token().value  # name
            self.tokenizer.next_token()  # (
            num_args = self.compile_expression_list()
            self.tokenizer.next_token()  # )
            self.call(identifier, func_name, num_args)
        elif token.value == "(":
            if self.func_type == CONSTRUCTOR:
                self.vm_writer.push(POINTER, 0)
            elif self.func_type == METHOD:
                self.vm_writer.push(ARG, 0)
            self.tokenizer.next_token()  # (
            num_args = self.compile_expression_list()
            if self.func_type != FUNCTION:
                self.vm_writer.call(self.class_name + "." + identifier, num_args + 1)
        elif token.value == "[":
            self.push_variable(identifier)
            self.tokenizer.next_token()  # [
            token = self.tokenizer.next_token()
            self.compile_expression(token)
            self.tokenizer.next_token()
            self.vm_writer.arithmetic("+")
            self.vm_writer.pop(POINTER, 1)
            self.vm_writer.push(THAT, 0)
        else:
            self.push_only_identifier(identifier)

    def compile_term(self, token: Token) -> None:
        if token.category == KEYWORD:
            self.push_keyword(token.value)
        elif token.category == STRING_CONSTANT:
            self.push_string(token.value)
        elif token.category == INT_CONSTANT:
            integer = int(token.value)
            self.vm_writer.push(CONST, integer)
        elif token.category == SYMBOL:
            self.push_symbol(token.value, token.additional_info)
        elif token.category == IDENTIFIER:
            self.push_identifier(token.value)

    def compile_expression(self, token: Token) -> None:
        self.compile_term(token)
        token = self.tokenizer.peek_next_token()
        while token.value not in (",", ")", ";", "]"):
            operation = token.value
            self.tokenizer.next_token()
            token = self.tokenizer.next_token()
            self.compile_term(token)
            token = self.tokenizer.peek_next_token()
            if operation == "*":
                self.vm_writer.call("Math.multiply", 2)
            elif operation == "/":
                self.vm_writer.call("Math.divide", 2)
            else:
                self.vm_writer.arithmetic(operation)

    def compile_expression_list(self) -> int:
        token = self.tokenizer.peek_next_token()
        if token.value == ")":
            return 0
        token = self.tokenizer.next_token()
        self.compile_expression(token)
        token = self.tokenizer.peek_next_token()
        num_args = 1
        while token.value == ",":
            self.tokenizer.next_token()  # ,
            token = self.tokenizer.next_token()
            self.compile_expression(token)
            token = self.tokenizer.peek_next_token()
            num_args += 1
        return num_args

    def write_array(self) -> None:
        self.vm_writer.pop(TEMP, 0)
        self.vm_writer.pop(POINTER, 1)
        self.vm_writer.push(TEMP, 0)
        self.vm_writer.pop(THAT, 0)

    def push_object(self, name: str) -> None:
        if self.symbol_table.kind_of(name) != NONE_KIND:
            self.vm_writer.push(LOCAL, self.symbol_table.index_of(name))
        else:
            self.symbol_table.end_sub_routine()
            if self.symbol_table.kind_of(name) != NONE_KIND:
                self.vm_writer.push(THIS, self.symbol_table.index_of(name))
            self.symbol_table.start_sub()

    def write_func_call(self, s_name: str, func_name: str, num_args: int) -> bool:
        if self.symbol_table.kind_of(s_name) != NONE_KIND:
            self.vm_writer.call(
                f"{self.symbol_table.type_of(s_name)}.{func_name}", num_args + 1
            )
            return True
        return False

    def call(self, s_name: str, func_name: str, num_args: int) -> None:
        if not self.write_func_call(s_name, func_name, num_args):
            self.symbol_table.end_sub_routine()
            if not self.write_func_call(s_name, func_name, num_args):
                self.vm_writer.call(f"{s_name}.{func_name}", num_args)
            self.symbol_table.start_sub()
