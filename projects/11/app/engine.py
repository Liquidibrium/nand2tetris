from app.constants import *
from app.simbol_table import *
from app.tokenizer import Token, Tokenizer
from app.vm_writer import *

STATEMENTS = (LET_TAG_NAME, IF_TAG_NAME, WHILE_TAG_NAME, DO_TAG_NAME, RETURN_TAG_NAME)


def starting_tag(tag_name: str) -> str:
    return f"<{tag_name}>"


def ending_tag(tag_name: str) -> str:
    return f"</{tag_name}>"


def get_line_tags(token: Token) -> str:
    return f"{starting_tag(token.category)} {token.value} {ending_tag(token.category)}"


label = "Label_my_"


class CompileEngine:
    def __init__(self, tokenizer: Tokenizer, vm_file: TextIO, name):
        self.vm_writer = VMWriter(vm_file, name)
        self.tokenizer = tokenizer
        self.symbol_table = SymbolTable()
        self.name = name
        self.out_file = None
        self.this_fun_name = None
        self.this_fun_type = None
        self.class_name = name
        self.label_count = 0

    def compile(self):
        with open(self.name + ".xml", 'w') as self.out_file:
            level = 0
            self.write_infile(starting_tag(CLASS_TAG_NAME))  # <class>
            self.write_next_token(level + 1)  # class
            self.write_next_token(level + 1)  # name
            self.write_next_token(level + 1)  # {
            # while self.tokenizer.has_more_token():
            next_token = self.tokenizer.next_token()
            while next_token.additional_info == CLASS_VAR_DEC_TAG_NAME:
                self.compile_class_var(level + 1, next_token)
                next_token = self.tokenizer.next_token()
            while next_token.additional_info == SUBROUTINE_DEC_TAG_NAME:
                self.compile_subroutine(level + 1, next_token)
                next_token = self.tokenizer.next_token()

            self.write_infile(get_line_tags(next_token), level + 1)  # }
            self.write_infile(ending_tag(CLASS_TAG_NAME))  # </class>

    def write_infile(self, line: str, level: int = 0) -> None:
        self.out_file.write(("  " * level) + line + "\n")

    def write_next_token(self, level: int) -> None:
        self.write_infile(get_line_tags(self.tokenizer.next_token()), level)

    def compile_for_tokenizer_test(self) -> None:
        self.write_infile(starting_tag(TOKENS_TAG_NAME))
        while self.tokenizer.has_more_token():
            self.write_next_token(0)

        self.write_infile(ending_tag(TOKENS_TAG_NAME))

    def compile_class_var(self, level: int, token: Token) -> None:
        self.write_infile(starting_tag(CLASS_VAR_DEC_TAG_NAME), level)
        self.compile_variable(token, level + 1)
        self.write_infile(ending_tag(CLASS_VAR_DEC_TAG_NAME), level)

    def compile_variable(self, token: Token, level: int) -> None:
        s_kind = token.value
        self.write_infile(get_line_tags(token), level)  # field | static | var
        s_type = self.tokenizer.peek_next_token().value
        self.write_next_token(level)  # type
        s_name = self.tokenizer.peek_next_token().value
        self.write_next_token(level)  # name
        # print(s_kind,s_type,s_name)
        self.symbol_table.define(s_name, s_type, s_kind)

        next_token = self.tokenizer.next_token()
        while next_token.value == ",":
            self.write_infile(get_line_tags(next_token), level)  # ,

            s_name = self.tokenizer.peek_next_token().value
            self.symbol_table.define(s_name, s_type, s_kind)

            self.write_next_token(level)  # name
            next_token = self.tokenizer.next_token()

        self.write_infile(get_line_tags(next_token), level)  # ;

    def compile_subroutine(self, level: int, next_token: Token) -> None:
        self.symbol_table.start_subroutine()
        self.write_infile(starting_tag(SUBROUTINE_DEC_TAG_NAME), level)

        # function | method | constructor
        self.this_fun_type = next_token.value

        self.write_infile(
            get_line_tags(next_token), level + 1)
        self.write_next_token(level + 1)  # return type

        self.this_fun_name = self.tokenizer.peek_next_token().value

        self.write_next_token(level + 1)  # name
        self.write_next_token(level + 1)  # (
        self.compile_parameters(level + 1)
        self.compile_subroutine_body(level + 1)
        self.write_infile(ending_tag(SUBROUTINE_DEC_TAG_NAME), level)
        self.symbol_table.end_sub_routine()

    def compile_parameters(self, level: int) -> None:
        self.write_infile(starting_tag(PARAMETER_LIST_TAG_NAME), level)
        next_token = self.tokenizer.next_token()
        if next_token.value == ")":
            self.write_infile(ending_tag(PARAMETER_LIST_TAG_NAME), level)
            self.write_infile(get_line_tags(next_token), level)
            return
        s_type = next_token.value
        self.write_infile(get_line_tags(next_token), level + 1)  # type
        s_name = self.tokenizer.peek_next_token().value
        self.write_next_token(level + 1)  # name

        self.symbol_table.define(s_name, s_type, "arg")

        next_token = self.tokenizer.next_token()
        while next_token.value != ")":
            self.write_infile(get_line_tags(next_token), level + 1)  # ,
            s_type = self.tokenizer.next_token().value
            self.write_next_token(level + 1)  # type
            s_name = self.tokenizer.next_token().value
            self.symbol_table.define(s_name, s_type, "arg")
            self.write_next_token(level + 1)  # name
            next_token = self.tokenizer.next_token()

        self.write_infile(ending_tag(PARAMETER_LIST_TAG_NAME), level)
        self.write_infile(get_line_tags(next_token), level)  # )

    def compile_subroutine_body(self, level: int) -> None:
        self.write_infile(starting_tag(SUBROUTINE_BODY_TAG_NAME), level)
        self.write_next_token(level + 1)

        next_token = self.tokenizer.peek_next_token()
        if next_token.value == "}":
            self.write_infile(ending_tag(SUBROUTINE_BODY_TAG_NAME), level)
            # self.write_infile(get_line_tags(next_token), level)
            return

        while next_token.additional_info == VAR_DEC_TAG_NAME:
            next_token = self.tokenizer.next_token()
            self.compile_subroutine_variable(next_token, level + 1)
            next_token = self.tokenizer.peek_next_token()

        self.vm_writer.function(self.this_fun_name, self.symbol_table.var_count(VAR_KIND))
        if self.this_fun_type == 'constructor':
            self.symbol_table.end_sub_routine()
            self.vm_writer.push(CONST, self.symbol_table.var_count(FIELD_KIND))
            self.vm_writer.call("Memory.alloc", 1)
            self.vm_writer.pop(POINTER, 0)

            self.symbol_table.start_sub()
        elif self.this_fun_type == "method":
            self.vm_writer.push(ARG, 0)
            self.vm_writer.push(POINTER, 0)

        if next_token.additional_info in STATEMENTS:
            next_token = self.tokenizer.next_token()
            self.compile_statements(next_token, level + 1)
            next_token = self.tokenizer.peek_next_token()

        self.write_infile(ending_tag(SUBROUTINE_BODY_TAG_NAME), level)
        # self.write_infile(get_line_tags(next_token), level)  # }

    def compile_subroutine_variable(self, next_token: Token, level: int) -> None:
        self.write_infile(starting_tag(VAR_DEC_TAG_NAME), level)
        self.compile_variable(next_token, level + 1)
        self.write_infile(ending_tag(VAR_DEC_TAG_NAME), level)

    def compile_statements(self, token: Token, level: int) -> None:
        self.write_infile(starting_tag(STATEMENTS_TAG_NAME), level)
        while token.value != "}":
            if token.additional_info == LET_TAG_NAME:
                self.compile_let(token, level + 1)
            elif token.additional_info == IF_TAG_NAME:
                self.compile_if(token, level + 1)
            elif token.additional_info == WHILE_TAG_NAME:
                self.compile_while(token, level + 1)
            elif token.additional_info == DO_TAG_NAME:
                self.compile_do(token, level + 1)
            elif token.additional_info == RETURN_TAG_NAME:
                self.compile_return(token, level + 1)
            token = self.tokenizer.next_token()
        self.write_infile(ending_tag(STATEMENTS_TAG_NAME), level)
        self.write_infile(get_line_tags(token), level)  # }

    def compile_if(self, token: Token, level: int) -> None:
        self.write_infile(starting_tag(IF_TAG_NAME), level)
        self.write_infile(get_line_tags(token), level + 1)  # if
        self.write_next_token(level + 1)  # (
        token = self.tokenizer.next_token()
        self.compile_expression(token, level + 1)

        self.write_next_token(level + 1)  # )

        self.vm_writer.arithmetic('~')
        first_label = label + str(self.label_count)
        self.label_count += 1
        self.vm_writer.w_if(first_label)

        self.write_next_token(level + 1)  # {

        token = self.tokenizer.next_token()
        if token.value == "}":
            self.write_infile(starting_tag(STATEMENTS_TAG_NAME), level + 1)
            self.write_infile(ending_tag(STATEMENTS_TAG_NAME), level + 1)
            self.write_infile(get_line_tags(token), level + 1)  # }
        else:
            self.compile_statements(token, level + 1)

        second_label = label + str(self.label_count)
        self.label_count += 1
        self.vm_writer.goto(second_label)

        token = self.tokenizer.peek_next_token()
        if token.additional_info == ELSE:
            token = self.tokenizer.next_token()
            self.write_infile(get_line_tags(token), level + 1)  # else
            token = self.tokenizer.next_token()
            self.write_infile(get_line_tags(token), level + 1)  # {
            self.vm_writer.label(first_label)
            token = self.tokenizer.next_token()
            self.compile_statements(token, level + 1)
            # self.write_next_token(level + 1)  # }
        else:
            self.vm_writer.label(first_label)

        self.vm_writer.label(second_label)

        self.write_infile(ending_tag(IF_TAG_NAME), level)

    def compile_while(self, token: Token, level: int) -> None:
        first_label = label + str(self.label_count)
        self.label_count += 1
        second_label = label + str(self.label_count)
        self.label_count += 1
        self.vm_writer.label(first_label)

        self.write_infile(starting_tag(WHILE_TAG_NAME), level)
        self.write_infile(get_line_tags(token), level + 1)

        self.write_next_token(level + 1)  # (
        token = self.tokenizer.next_token()
        self.compile_expression(token, level + 1)

        self.vm_writer.arithmetic('~')
        self.vm_writer.w_if(second_label)

        self.write_next_token(level + 1)  # )
        self.write_next_token(level + 1)  # {
        token = self.tokenizer.next_token()
        self.compile_statements(token, level + 1)
        self.vm_writer.goto(first_label)
        self.write_infile(ending_tag(WHILE_TAG_NAME), level)
        self.vm_writer.label(second_label)

    def push_variable(self, s_name):
        kind = self.symbol_table.kind_of(s_name)
        if kind == ARG_KIND:
            self.vm_writer.push(ARG, SymbolTable.index_of(s_name))
        elif kind != VAR_KIND:
            self.vm_writer.push(LOCAL, SymbolTable.index_of(s_name))
        else:
            self.symbol_table.end_sub_routine()
            if self.symbol_table.kind_of(s_name) != NONE_KIND:
                self.vm_writer.push(THIS, self.symbol_table.index_of(s_name))
            self.symbol_table.start_sub()

    def compile_let(self, next_token: Token, level: int) -> None:
        self.write_infile(starting_tag(LET_TAG_NAME), level)
        self.write_infile(get_line_tags(next_token), level + 1)  # let

        s_name = self.tokenizer.peek_next_token().value

        self.write_next_token(level + 1)  # variable name
        is_arr = False
        next_token = self.tokenizer.next_token()
        if next_token.value == "[":
            is_arr = True
            self.push_variable(s_name)  # array name
            self.write_infile(get_line_tags(next_token), level + 1)  # [

            token = self.tokenizer.next_token()
            self.compile_expression(token, level + 1)
            self.vm_writer.arithmetic("+")
            self.write_next_token(level + 1)  # ]

            next_token = self.tokenizer.next_token()

        self.write_infile(get_line_tags(next_token), level + 1)  # =

        token = self.tokenizer.next_token()
        self.compile_expression(token, level + 1)

        self.write_next_token(level + 1)  # ;

        self.write_infile(ending_tag(LET_TAG_NAME), level)

        kind = self.symbol_table.kind_of(s_name)
        if kind == ARG_KIND:
            if not is_arr:
                self.vm_writer.pop(ARG, self.symbol_table.index_of(s_name))
            else:
                self.handle_arr()
        elif kind == VAR_KIND:
            if not is_arr:
                self.vm_writer.pop(LOCAL, self.symbol_table.index_of(s_name))
            else:
                self.handle_arr()
        elif kind == NONE_KIND:
            self.symbol_table.end_sub_routine()
            class_kind = self.symbol_table.kind_of(s_name)
            if class_kind == STATIC_KIND:
                self.vm_writer.pop(STATIC, self.symbol_table.index_of(s_name))
            else:
                assert kind == FIELD_KIND
                if not is_arr:
                    self.vm_writer.pop(THIS, self.symbol_table.index_of(s_name))
                else:
                    self.handle_arr()

            self.symbol_table.start_sub()

    def compile_do(self, token: Token, level: int) -> None:
        self.write_infile(starting_tag(DO_TAG_NAME), level)
        self.write_infile(get_line_tags(token), level + 1)  # do
        s_name = self.tokenizer.peek_next_token().value
        self.write_next_token(level + 1)  # name

        token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(token), level + 1)
        if token.value == "(":
            if self.this_fun_type == "constructor":
                self.vm_writer.push(POINTER, 0)
            elif self.this_fun_type == "method":
                self.vm_writer.push(ARG, 0)

            num_arg = self.compile_expression_list(level + 1)
            if self.this_fun_type != "function":
                self.vm_writer.call(self.name + "." + s_name, num_arg + 1)
            # todO
        elif token.value == ".":
            fun_name = self.tokenizer.peek_next_token().value
            self.push_object(fun_name)
            self.write_next_token(level + 1)  # fun name
            self.write_next_token(level + 1)  # (
            num_arg = self.compile_expression_list(level + 1)
            print(num_arg)
            self.call(s_name, fun_name, num_arg)

        self.write_next_token(level + 1)  # )
        self.write_next_token(level + 1)  # ;
        self.vm_writer.pop(TEMP, 0)
        self.write_infile(ending_tag(DO_TAG_NAME), level)

    def compile_return(self, next_token: Token, level: int) -> None:
        self.write_infile(starting_tag(RETURN_TAG_NAME), level)
        self.write_infile(get_line_tags(next_token), level + 1)
        next_token = self.tokenizer.next_token()
        if next_token.value != ";":
            self.compile_expression(next_token, level + 1)
            next_token = self.tokenizer.next_token()
        else:
            self.vm_writer.push(CONST, 0)
        self.vm_writer.w_return()
        self.write_infile(get_line_tags(next_token), level + 1)

        self.write_infile(ending_tag(RETURN_TAG_NAME), level)

    def compile_term(self, token: Token, level: int) -> None:
        self.write_infile(starting_tag(TERM_TAG_NAME), level)
        if token.category == KEYWORD:
            if token.value == "null" or token.value == 'false':
                self.vm_writer.push(CONST, 0)
            elif token.value == "true":
                self.vm_writer.push(CONST, 1)
                self.vm_writer.arithmetic("!")
            elif token.value == "this":
                self.vm_writer.push(POINTER, 0)
        elif token.category == STRING_CONSTANT:
            string = self.tokenizer.peek_next_token().value
            self.vm_writer.push(CONST, len(string))
            self.vm_writer.call("String.new", 1)
            for ch in string:
                self.vm_writer.push(CONST, ord(ch))
                self.vm_writer.call("String.appendChar", 2)
            self.write_infile(get_line_tags(token), level + 1)

        elif token.category == INT_CONSTANT:
            integer = int(token.value)
            self.vm_writer.push(CONST, integer)
            self.write_infile(get_line_tags(token), level + 1)
        elif token.category == SYMBOL:
            if token.additional_info == UNARY_OPERATOR:
                operator = self.tokenizer.peek_next_token().value

                self.write_infile(get_line_tags(token), level + 1)
                token = self.tokenizer.next_token()
                self.compile_term(token, level + 1)
                if operator == '-':
                    self.vm_writer.arithmetic('!')
                else:
                    self.vm_writer.arithmetic(operator)

            elif token.value == "(":
                self.write_infile(get_line_tags(token), level + 1)
                token = self.tokenizer.next_token()
                self.compile_expression(token, level + 1)
                self.write_next_token(level + 1)
            else:
                self.write_infile(get_line_tags(token), level + 1)
                token = self.tokenizer.next_token()
                self.compile_expression(token, level + 1)

        elif token.category == IDENTIFIER:
            s_name = token.value
            only_is_var_name = True
            self.write_infile(get_line_tags(token), level + 1)
            token = self.tokenizer.peek_next_token()
            if token.value == ".":
                only_is_var_name = False
                token = self.tokenizer.next_token()
                self.write_infile(get_line_tags(token), level + 1)  # .
                fun_name = self.tokenizer.peek_next_token().value
                self.write_next_token(level + 1)  # name
                self.write_next_token(level + 1)  # (
                num_args = self.compile_expression_list(level + 1)
                self.write_next_token(level + 1)  # )
                self.call(s_name, fun_name, num_args)
            if token.value == "(":
                only_is_var_name = False
                if self.this_fun_type == "constructor":
                    self.vm_writer.push(POINTER, 0)
                elif self.this_fun_type == "method":
                    self.vm_writer.push(ARG, 0)

                token = self.tokenizer.next_token()
                self.write_infile(get_line_tags(token), level + 1)  # (
                num_args = self.compile_expression_list(level + 1)
                if self.this_fun_type != "function":
                    self.vm_writer.call(self.name + "." + s_name, num_args + 1)
                # TODO
            elif token.value == "[":
                only_is_var_name = False
                self.push_variable(s_name)
                token = self.tokenizer.next_token()
                self.write_infile(get_line_tags(token), level + 1)  # [
                token = self.tokenizer.next_token()
                self.compile_expression(token, level + 1)
                self.write_next_token(level + 1)
                self.vm_writer.arithmetic("+")
                self.vm_writer.pop(POINTER, 1)
                self.vm_writer.push(THAT, 0)
            if only_is_var_name:
                kind = self.symbol_table.kind_of(s_name)
                if kind == ARG_KIND:
                    self.vm_writer.push(ARG, self.symbol_table.index_of(s_name))
                elif kind == VAR_KIND:
                    self.vm_writer.push(LOCAL, self.symbol_table.index_of(s_name))
                elif kind == NONE_KIND:
                    self.symbol_table.end_sub_routine()
                    kind = self.symbol_table.kind_of(s_name)
                    if kind == STATIC_KIND:
                        self.vm_writer.push(STATIC, self.symbol_table.index_of(s_name))
                    elif kind == FIELD_KIND:
                        self.vm_writer.push(THIS, self.symbol_table.index_of(s_name))

                    self.symbol_table.start_sub()

        self.write_infile(ending_tag(TERM_TAG_NAME), level)

    def compile_expression(self, token: Token, level: int) -> None:
        self.write_infile(starting_tag(EXPRESSION_TAG_NAME), level)
        self.compile_term(token, level + 1)

        token = self.tokenizer.peek_next_token()

        while token.value not in (",", ")", ";", "]"):
            operation = token.value
            self.write_next_token(level)
            token = self.tokenizer.next_token()
            self.compile_term(token, level + 1)
            token = self.tokenizer.peek_next_token()
            if operation == "*":
                self.vm_writer.call("Math.multiply", 2)
            elif operation == "/":
                self.vm_writer.call("Math.devide", 2)
            else:
                self.vm_writer.arithmetic(operation)

        self.write_infile(ending_tag(EXPRESSION_TAG_NAME), level)

    def compile_expression_list(self, level: int) -> int:
        self.write_infile(starting_tag(EXPRESSION_LIST_TAG_NAME), level)
        token = self.tokenizer.peek_next_token()
        if token.value == ")":
            self.write_infile(ending_tag(EXPRESSION_LIST_TAG_NAME), level)
            return 0
        token = self.tokenizer.next_token()
        self.compile_expression(token, level + 1)
        token = self.tokenizer.peek_next_token()
        num_args = 1
        while token.value == ",":
            token = self.tokenizer.next_token()
            self.write_infile(get_line_tags(token), level)  # ,
            token = self.tokenizer.next_token()
            self.compile_expression(token, level + 1)
            token = self.tokenizer.peek_next_token()
            num_args += 1
        self.write_infile(ending_tag(EXPRESSION_LIST_TAG_NAME), level)
        return num_args

    def handle_arr(self):
        self.vm_writer.pop(TEMP, 0)
        self.vm_writer.pop(POINTER, 1)
        self.vm_writer.pop(TEMP, 0)
        self.vm_writer.pop(THAT, 0)

    def push_object(self, name):
        if self.symbol_table.kind_of(name) != NONE_KIND:
            self.vm_writer.push(LOCAL, self.symbol_table.index_of(name))
        else:
            self.symbol_table.end_sub_routine()
            if self.symbol_table.kind_of(name) != NONE_KIND:
                self.vm_writer.push(THIS, self.symbol_table.index_of(name))
            self.symbol_table.start_sub()

    def call(self, s_name, fun_name, num_args):
        print(s_name, fun_name, num_args)
        if self.symbol_table.kind_of(s_name) != NONE_KIND:
            self.vm_writer.call(self.symbol_table.type_of(fun_name), num_args + 1)
        else:
            self.symbol_table.end_sub_routine()
            if self.symbol_table.kind_of(s_name) != NONE_KIND:
                self.vm_writer.call(f"{self.symbol_table.type_of(s_name)}.{fun_name}", num_args + 1)
            else:
                self.vm_writer.call(f"{s_name}.{fun_name}", num_args)
            self.symbol_table.start_sub()
