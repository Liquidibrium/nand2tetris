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

ONE_LINE_COMMENT = "//"
MULTI_LINE_COMMENT_STARTS = "/*"
MULTI_LINE_COMMENT_ENDS = "*/"
SPACE = " "

PRIMITIVE_TYPE = "type"
ELSE = "else "
KEYWORDS = {
    "class": CLASS_TAG_NAME,
    "constructor": SUBROUTINE_DEC_TAG_NAME,
    "function": SUBROUTINE_DEC_TAG_NAME,
    "method": SUBROUTINE_DEC_TAG_NAME,
    "field": CLASS_VAR_DEC_TAG_NAME,
    "static": CLASS_VAR_DEC_TAG_NAME,
    "var": VAR_DEC_TAG_NAME,
    "int": PRIMITIVE_TYPE,
    "char": PRIMITIVE_TYPE,
    "boolean": PRIMITIVE_TYPE,
    "void": PRIMITIVE_TYPE,
    "true": TERM_TAG_NAME,
    "false": TERM_TAG_NAME,
    "null": TERM_TAG_NAME,
    "this": TERM_TAG_NAME,
    "let": LET_TAG_NAME,
    "do": DO_TAG_NAME,
    "if": IF_TAG_NAME,
    "else": ELSE,
    "while": WHILE_TAG_NAME,
    "return": RETURN_TAG_NAME,
}
SYMBOL = "symbol"
KEYWORD = "keyword"
IDENTIFIER = "identifier"
INT_CONSTANT = "integerConstant"
STRING_CONSTANT = "stringConstant"

OPERATOR = "operator"
UNARY_OPERATOR = "unary"

SYMBOLS = {
    "{": SYMBOL,
    "}": SYMBOL,
    "(": SYMBOL,
    ")": SYMBOL,
    "[": SYMBOL,
    "]": SYMBOL,
    ".": SYMBOL,
    ",": SYMBOL,
    ";": SYMBOL,
    "+": OPERATOR,
    "*": OPERATOR,
    "/": OPERATOR,
    "&": OPERATOR,
    "|": OPERATOR,
    "<": OPERATOR,
    ">": OPERATOR,
    "=": OPERATOR,
    "-": UNARY_OPERATOR,
    "~": UNARY_OPERATOR,
}
