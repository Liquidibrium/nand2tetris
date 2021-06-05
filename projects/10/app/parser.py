#
# def write_in_file(file: TextIO, tokenized_lines: Tuple[str, ...]) -> None:
#     tokenized_lines: str = "\n".join(tokenized_lines) + "\n"
#     file.write(tokenized_lines)
from typing import TextIO

from app.tokenizer import Token, Tokenizer

CLASS_VAR_DEC_TAG_NAME = "classVarDec"
VAR_DEC_TAG_NAME = "varDec"
TOKENS_TAG_NAME = "tokens"
CLASS_TAG_NAME = "class"
SUBROUTINE_DEC_TAG_NAME = "subroutineDec"
PARAMETER_LIST_TAG_NAME = "parameterList"
SUBROUTINE_BODY_TAG_NAME = "subroutineBody"
STATEMENTS_TAG_NAME = "statements"
LET_TAG_NAME = "letStatement"
IF_TAG_NAME = "ifStatement"
WHILE_TAG_NAME = "whileStatement"
DO_TAG_NAME = "doStatement"
RETURN_TAG_NAME = "returnStatement"
EXPRESSION_TAG_NAME = "expression"
TERM_TAG_NAME = "term"
EXPRESSION_LIST_TAG_NAME = "expressionList"


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

    def compile_statements(self) -> None:
        pass

    def compile_if(self) -> None:
        pass

    def compile_term(self) -> None:
        pass

    def compile_expression(self) -> None:
        pass

    def compile_while(self) -> None:
        pass

    def write_infile(self, line: str) -> None:
        self.out_file.write(line + "\n")

    def compile(self) -> None:
        self.write_infile(starting_tag(TOKENS_TAG_NAME))
        while self.tokenizer.has_more_token():
            token = self.tokenizer.next_token()
            self.write_infile(get_line_tags(token))

        self.write_infile(ending_tag(TOKENS_TAG_NAME))
