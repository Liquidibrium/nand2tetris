symbols = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
}

global_variable_index = 16


def parse_line():
    pass


def translate_A_instruction():
    pass


def translate_C_instruction():
    pass


def process_label_symbol():
    pass


def parse_pseudo_command(line: str, line_number: int):
    if "(" == line[0]:
        label_symbol = line[1:].strip(")")
        symbols[label_symbol] = line_number


def translate_variable_symbol(variable_symbol):
    global global_variable_index
    symbols[variable_symbol] = global_variable_index
    global_variable_index += 1


def assemble(asm_file: str) -> None:
    with open(asm_file) as f:
        pass
