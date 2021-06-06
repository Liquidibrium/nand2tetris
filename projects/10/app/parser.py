from typing import TextIO
from app.constants import *
from app.tokenizer import Token, Tokenizer

STATEMENTS = (LET_TAG_NAME, IF_TAG_NAME, WHILE_TAG_NAME, DO_TAG_NAME, RETURN_TAG_NAME)


def starting_tag(tag_name: str) -> str:
    return f"<{tag_name}>"


def ending_tag(tag_name: str) -> str:
    return f"</{tag_name}>"


def get_line_tags(token: Token) -> str:
    return f"{starting_tag(token.category)} {token.value} {ending_tag(token.category)}"


class CompileEngine:
    def __init__(self, tokenizer: Tokenizer, out_file: TextIO):
        self.tokenizer = tokenizer
        self.out_file = out_file

    def write_infile(self, line: str, level: int = 0) -> None:
        self.out_file.write(("  " * level) + line + "\n")

    def compile_for_tokenizer_test(self) -> None:
        self.write_infile(starting_tag(TOKENS_TAG_NAME))
        while self.tokenizer.has_more_token():
            token = self.tokenizer.next_token()
            self.write_infile(get_line_tags(token))

        self.write_infile(ending_tag(TOKENS_TAG_NAME))

    def compile(self) -> None:
        level = 0
        while self.tokenizer.has_more_token():
            self.compile_class(level)

    def compile_class(self, level):
        token = self.tokenizer.next_token()
        self.write_infile(starting_tag(CLASS_TAG_NAME))  # <class>
        self.write_infile(get_line_tags(token), level + 1)  # class
        next_token = self.tokenizer.next_token()  # class name
        self.write_infile(get_line_tags(next_token), level + 1)
        next_token = self.tokenizer.next_token()  # {
        self.write_infile(get_line_tags(next_token), level + 1)

        while self.tokenizer.has_more_token():
            next_token = self.tokenizer.next_token()
            while next_token.additional_info == CLASS_VAR_DEC_TAG_NAME:
                self.compile_class_var(level + 1, next_token)
                next_token = self.tokenizer.next_token()
            while next_token.additional_info == SUBROUTINE_DEC_TAG_NAME:
                self.compile_subroutine(level + 1, next_token)
                next_token = self.tokenizer.next_token()

        self.write_infile(get_line_tags(next_token), level + 1)
        self.write_infile(ending_tag(CLASS_TAG_NAME))  # </class>

    def compile_class_var(self, level, token):
        self.write_infile(starting_tag(CLASS_VAR_DEC_TAG_NAME), level)
        self.compile_variable(token, level)
        self.write_infile(starting_tag(CLASS_VAR_DEC_TAG_NAME), level)

    def compile_variable(self, token, level):
        self.write_infile(get_line_tags(token), level)
        token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(token), level)
        ident_token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(ident_token), level)

        next_token = self.tokenizer.next_token()
        while next_token.value == ',':
            self.write_infile(get_line_tags(next_token), level)
            next_token = self.tokenizer.next_token()
            self.write_infile(get_line_tags(next_token), level)
            next_token = self.tokenizer.next_token()

        self.write_infile(get_line_tags(next_token), level)

    def compile_subroutine_body(self, level):
        self.write_infile(starting_tag(SUBROUTINE_BODY_TAG_NAME), level)
        next_token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(next_token), level + 1)  # return type
        next_token = self.tokenizer.next_token()
        if next_token.value == '}':
            self.write_infile(get_line_tags(next_token), level)  # return type
            self.write_infile(ending_tag(SUBROUTINE_BODY_TAG_NAME), level)
            return

        while next_token.additional_info == VAR_DEC_TAG_NAME:
            self.compile_subroutine_variable(next_token, level + 1)
            next_token = self.tokenizer.next_token()

        if next_token.additional_info in STATEMENTS:
            self.compile_statements(next_token, level + 1)

        self.write_infile(get_line_tags(next_token), level + 1)  # return type
        self.write_infile(ending_tag(SUBROUTINE_BODY_TAG_NAME), level)

    def compile_parameters(self, level, next_token):
        self.write_infile(starting_tag(PARAMETER_LIST_TAG_NAME), level)
        if next_token.value == ')':
            self.write_infile(ending_tag(PARAMETER_LIST_TAG_NAME), level)
            self.write_infile(get_line_tags(next_token), level)
            return
        self.write_infile(get_line_tags(next_token), level)
        next_token = self.tokenizer.next_token()

        self.write_infile(get_line_tags(next_token), level)
        next_token = self.tokenizer.next_token()

        while next_token.value != ')':
            self.write_infile(get_line_tags(next_token), level)
            next_token = self.tokenizer.next_token()
            self.write_infile(get_line_tags(next_token), level)
            next_token = self.tokenizer.next_token()
            self.write_infile(get_line_tags(next_token), level)
            next_token = self.tokenizer.next_token()

        self.write_infile(ending_tag(PARAMETER_LIST_TAG_NAME), level)
        self.write_infile(get_line_tags(next_token), level)

    def compile_subroutine(self, level, next_token):
        self.write_infile(starting_tag(SUBROUTINE_DEC_TAG_NAME), level)
        self.write_infile(get_line_tags(next_token), level + 1)  # keyword
        next_token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(next_token), level + 1)  # return type
        next_token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(next_token), level + 1)  # name
        next_token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(next_token), level + 1)  # (

        next_token = self.tokenizer.next_token()
        self.compile_parameters(level + 1, next_token)
        self.compile_subroutine_body(level + 1)
        self.write_infile(ending_tag(SUBROUTINE_DEC_TAG_NAME), level)

    def compile_subroutine_variable(self, next_token, level):
        self.write_infile(starting_tag(VAR_DEC_TAG_NAME), level)
        self.compile_variable(next_token, level + 1)
        self.write_infile(ending_tag(VAR_DEC_TAG_NAME), level)

    def compile_statements(self, token, level) -> None:
        self.write_infile(starting_tag(STATEMENTS_TAG_NAME), level)
        while token.value != '}':
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

    def compile_if(self, token, level: int) -> None:
        self.write_infile(starting_tag(IF_TAG_NAME), level)
        self.write_infile(get_line_tags(token), level + 1)  # if

        token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(token), level)  # (
        token = self.tokenizer.next_token()
        self.compile_expression(token, level + 1)
        token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(token), level)  # )

        token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(token), level)  # {

        token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(token), level)  # )
        token = self.tokenizer.next_token()
        if token.additional_info in STATEMENTS:
            self.compile_statements(token, level + 1)
            token = self.tokenizer.next_token()

        self.write_infile(get_line_tags(token), level)  # }

        token = self.tokenizer.next_token()
        if token.value == ELSE:
            self.write_infile(get_line_tags(token), level)  # else
            token = self.tokenizer.next_token()
            self.write_infile(get_line_tags(token), level)  # {
            token = self.tokenizer.next_token()
            self.compile_statements(token, level + 1)
            token = self.tokenizer.next_token()
            self.write_infile(get_line_tags(token), level)  # }

        self.write_infile(ending_tag(IF_TAG_NAME), level)

    def compile_term(self, token, level) -> None:
        print(token, level)
        self.write_infile(starting_tag(TERM_TAG_NAME), level)
        if token.category in (KEYWORD, STRING_CONSTANT, INT_CONSTANT):
            self.write_infile(get_line_tags(token), level + 1)
        elif token.category == SYMBOL:
            if token.additional_info == UNARY_OPERATOR:
                self.write_infile(get_line_tags(token), level + 1)
                token = self.tokenizer.next_token()
                self.compile_term(token, level + 1)
            else:
                self.write_infile(get_line_tags(token), level + 1)
                token = self.tokenizer.next_token()
                self.compile_expression(token, level + 1)
                token = self.tokenizer.next_token()
                self.write_infile(get_line_tags(token), level + 1)
        elif token.category == IDENTIFIER:
            self.write_infile(get_line_tags(token), level + 1)
            token = self.tokenizer.next_token()
            if token.value == '.':
                self.write_infile(get_line_tags(token), level + 1)
                token = self.tokenizer.next_token()
                self.write_infile(get_line_tags(token), level + 1)
                token = self.tokenizer.next_token()
                self.write_infile(get_line_tags(token), level + 1)
                self.compile_expression_list(level + 1)
            if token.value == '(':
                self.write_infile(get_line_tags(token), level + 1)
                self.compile_expression_list(level + 1)

                token = self.tokenizer.next_token()
                self.write_infile(get_line_tags(token), level + 1)

                token = self.tokenizer.next_token()
                self.write_infile(get_line_tags(token), level + 1)
            elif token.value == '[':
                self.write_infile(get_line_tags(token), level + 1)
                token = self.tokenizer.next_token()
                self.compile_expression(token, level + 1)
                token = self.tokenizer.next_token()
                self.write_infile(get_line_tags(token), level + 1)

        self.write_infile(ending_tag(TERM_TAG_NAME), level)

    def compile_while(self, token, level) -> None:
        self.write_infile(starting_tag(WHILE_TAG_NAME), level)
        self.write_infile(get_line_tags(token), level + 1)

        token = self.tokenizer.next_token()  # (
        self.write_infile(get_line_tags(token), level + 1)
        token = self.tokenizer.next_token()
        self.compile_expression(token, level + 1)
        token = self.tokenizer.next_token()  # )
        self.write_infile(get_line_tags(token), level + 1)
        token = self.tokenizer.next_token()  # {
        self.write_infile(get_line_tags(token), level + 1)
        token = self.tokenizer.next_token()
        self.compile_statements(token, level + 1)
        token = self.tokenizer.next_token()  # {
        self.write_infile(get_line_tags(token), level + 1)
        self.write_infile(starting_tag(WHILE_TAG_NAME), level)

    def compile_let(self, next_token, level):
        self.write_infile(starting_tag(LET_TAG_NAME), level)
        self.write_infile(get_line_tags(next_token), level + 1)  # let
        next_token = self.tokenizer.next_token()  # variable name
        self.write_infile(get_line_tags(next_token), level + 1)
        next_token = self.tokenizer.next_token()
        if next_token.value == '[':
            self.write_infile(get_line_tags(next_token), level + 1)

            token = self.tokenizer.next_token()
            self.compile_expression(token, level + 1)
            # next_token = self.tokenizer.next_token()  # ]
            # self.write_infile(get_line_tags(next_token), level + 1)
            next_token = self.tokenizer.next_token()

        # =
        self.write_infile(get_line_tags(next_token), level + 1)
        token = self.tokenizer.next_token()
        self.compile_expression(token, level + 1)

        next_token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(next_token), level + 1)

        self.write_infile(ending_tag(LET_TAG_NAME), level)

    def compile_do(self, token, level):
        self.write_infile(starting_tag(DO_TAG_NAME), level)
        self.write_infile(get_line_tags(token), level)

        token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(token), level)

        token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(token), level)
        if token.value == '(':
            self.compile_expression_list(level + 1)
        elif token.value == ".":
            token = self.tokenizer.next_token()
            self.write_infile(get_line_tags(token), level)

            token = self.tokenizer.next_token()
            self.write_infile(get_line_tags(token), level)
            self.compile_expression_list(level + 1)

        token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(token), level)

        token = self.tokenizer.next_token()
        self.write_infile(get_line_tags(token), level)

        self.write_infile(ending_tag(DO_TAG_NAME), level)

    def compile_return(self, next_token, level):
        self.write_infile(starting_tag(RETURN_TAG_NAME), level)
        self.write_infile(get_line_tags(next_token), level + 1)
        next_token = self.tokenizer.next_token()
        if next_token.value != ";":
            token = self.tokenizer.next_token()
            self.compile_expression(token, level + 1)
            next_token = self.tokenizer.next_token()
        else:
            self.write_infile(get_line_tags(next_token), level + 1)

        self.write_infile(ending_tag(RETURN_TAG_NAME), level)

    def compile_expression(self, token, level):
        self.write_infile(starting_tag(EXPRESSION_TAG_NAME), level)
        self.compile_term(token, level + 1)
        token = self.tokenizer.next_token()

        while token.value not in (',', ')', ';', ']'):
            self.write_infile(get_line_tags(token), level)
            token = self.tokenizer.next_token()
            self.compile_term(token, level + 1)
            token = self.tokenizer.next_token()

        self.write_infile(get_line_tags(token), level)
        self.write_infile(ending_tag(EXPRESSION_TAG_NAME), level)

    def compile_expression_list(self, level):

        self.write_infile(starting_tag(EXPRESSION_LIST_TAG_NAME), level)
        token = self.tokenizer.next_token()
        print("list - ", token)
        if token.value == ')':
            self.write_infile(ending_tag(EXPRESSION_LIST_TAG_NAME), level)
            self.write_infile(get_line_tags(token), level)
            return

        self.compile_expression(token, level + 1)
        token = self.tokenizer.next_token()
        while token.value != ')':
            self.write_infile(get_line_tags(token), level)
            token = self.tokenizer.next_token()
            self.compile_term(token, level + 1)
            token = self.tokenizer.next_token()
        print("error - ", token)
        self.write_infile(ending_tag(EXPRESSION_LIST_TAG_NAME), level)
        self.write_infile(get_line_tags(token), level)
