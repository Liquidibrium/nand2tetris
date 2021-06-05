from collections import deque

ONE_LINE_COMMENT = "//"
MULTI_LINE_COMMENT_STARTS = "/*"
MULTI_LINE_COMMENT_ENDS = "*/"
SPACE = " "

KEYWORDS = {
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return",
}
SYMBOL = "symbol"
KEYWORD = "keyword"
IDENTIFIER = "identifier"
INT_CONSTANT = "integerConstant"
STRING_CONSTANT = "stringConstant"
SYMBOLS = {
    "{",
    "}",
    "(",
    ")",
    "[",
    "]",
    ".",
    ",",
    ";",
    "+",
    "-",
    "*",
    "/",
    "&",
    "|",
    "<",
    ">",
    "=",
    "~",
}


class Token:
    def __init__(self, value, category):
        self.value = value
        self.category = category

    def token_category(self):
        return self.category

    def token_value(self):
        return self.value


# remove comments and white spaces from beginning and end of line
def filter_inline_comment(line: str) -> str:
    index: int = line.find("//")
    if index != -1:
        line = line[:index].rstrip()
    return line


def get_token_category(only_word: str):
    if only_word in KEYWORDS:
        return KEYWORD

    if only_word.isnumeric():
        return INT_CONSTANT
    return IDENTIFIER


class Tokenizer:
    def __init__(self, jack_file):
        self.jack_file = jack_file
        self.tokens = deque()

    def tokenize(self):
        multi_line_comment = False
        for line in self.jack_file:
            line = line.strip()
            if line:
                # Remove Comments
                if not multi_line_comment:
                    line = filter_inline_comment(line)
                    if not line:
                        continue
                comment_starting_index = line.find(MULTI_LINE_COMMENT_STARTS)
                if comment_starting_index != -1:  # found comment /*
                    if comment_starting_index == 0:  # line starts with /*
                        if line.endswith(MULTI_LINE_COMMENT_ENDS):  # Ends with */
                            continue
                        comment_ending_index = line.find(MULTI_LINE_COMMENT_ENDS)
                        if comment_ending_index != -1:  # found */ in middle of line
                            line = line[:comment_starting_index] + \
                                   line[comment_ending_index + len(MULTI_LINE_COMMENT_ENDS):]
                        else:  # not found ending
                            multi_line_comment = True
                            continue
                    else:
                        line = line[:comment_starting_index].rstrip()
                else:  # NOT FOUND */
                    if line.endswith(MULTI_LINE_COMMENT_ENDS):  # Ends with */
                        multi_line_comment = False
                        continue
                    comment_ending_index = line.find(MULTI_LINE_COMMENT_ENDS)
                    if comment_ending_index != -1:  # found */ in middle of line
                        multi_line_comment = False
                        line = line[comment_ending_index + len(MULTI_LINE_COMMENT_ENDS):].lstrip()
                    elif multi_line_comment:
                        continue

                # main logic
                # Here
                parts = line.split('"')
                string_const = False
                for part in parts:
                    if string_const:
                        self.tokens.append(Token(part, STRING_CONSTANT))
                        string_const = False
                    else:
                        words = part.split()
                        for word in words:
                            self.__get_tokens(word)
                        string_const = True

    def __get_tokens(self, word):
        # if not word:
        #     return
        if word in SYMBOLS:
            if word == ">":
                word = "&gt;"
            elif word == "<":
                word = "&lt;"
            elif word == "&":
                word = "&amp;"
            self.tokens.append(Token(word, SYMBOL))
            return

        not_with_symbol = True
        for symbol in SYMBOLS:
            symbol_index = word.find(symbol)
            if symbol_index == -1:
                continue
            not_with_symbol = False
            if symbol_index == 0:
                self.tokens.append(Token(symbol, SYMBOL))
                self.__get_tokens(word[1:])
            elif symbol_index == len(word) - 1:
                self.__get_tokens(word[:symbol_index])
                self.tokens.append(Token(symbol, SYMBOL))
            else:
                self.__get_tokens(word[:symbol_index])
                self.tokens.append(Token(symbol, SYMBOL))
                self.__get_tokens(word[symbol_index + 1:])
            break
        if not_with_symbol:
            category = get_token_category(word)
            self.tokens.append(Token(word, category))

    def has_more_token(self):
        return len(self.tokens) != 0

    def next_token(self):
        return self.tokens.popleft()
