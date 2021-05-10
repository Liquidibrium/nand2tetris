from typing import Tuple

symbols = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
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
}

dest_dict = {
    "": "000",  # null
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

jump_dict = {
    "": "000",  # null
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

comp_dict = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101",
}


# remove comments, which begins with //
# and remove space, new line and tab characters from line


def parse_line(line: str) -> str:
    index = line.find("//")
    if index != -1:
        line = line[:index]
    return line.replace(" ", "").replace("\n", "").replace("\t", "")


# translates line to A instruction,
# instruction line is passed without "@,
# if label is in symbool table,
# then the proper value is returned
# if not in symbols, new variable is allocated,
# variable and variable index is add in symbols
# the returned value is 16 byte string
# and variable index to indicate if allocation occurred
def translate_A_instruction(
    instruction_line: str, variable_index: int
) -> Tuple[str, int]:
    if instruction_line[0].isdigit():  # check just first symbol
        address = int(instruction_line)
    elif instruction_line in symbols:
        address = symbols[instruction_line]
    else:
        symbols[instruction_line] = variable_index
        address = variable_index
        variable_index += 1
    return (format(address, "016b"), variable_index)


# translates line into c binary code
# instruction line is looks like this
# dest = comp ; jump
# dest and jump is optional
# so dest_dict and jump_dict contains "" as key for null
def translate_C_instruction(instruction_line: str) -> str:
    dest_end_index = instruction_line.find("=")
    comp_start_index = dest_end_index + 1
    if dest_end_index == -1:
        # destination is omittied
        dest_end_index = 0
        comp_start_index = 0
    # if destination is omitted then search key is "", which indicates null
    destination = dest_dict[instruction_line[:dest_end_index]]

    comp_end_index = instruction_line.find(";")
    jump_start_index = comp_end_index + 1
    if comp_end_index == -1:
        # jump is omitted
        comp_end_index = len(instruction_line)
        jump_start_index = comp_end_index

    compare = comp_dict[instruction_line[comp_start_index:comp_end_index]]

    # if jump is omitted then search key is "", which indicates null
    jump = jump_dict[instruction_line[jump_start_index:]]
    return "111" + compare + destination + jump


# label is add in symbols with line number
def parse_pseudo_command(line: str, line_number: int) -> None:
    label_symbol = line[: line.find(")")]
    symbols[label_symbol] = line_number


# write lines in file with mode
# if mode is w it is used to make empty file
# if mode is a then new line translated instruction is add
def fwrite_line(
    instruction_line: str, file_name: str, mode: str, line_end: str = "\n"
) -> None:
    with open(file_name, mode) as f:
        print(instruction_line, end=line_end, file=f)


# filters commnets, spaces and
# adds labels with proper line number value into symbols
# middle file is generated and to extension is added t /.asmt
# middle file name is returned
def first_pass(asm_file: str) -> str:
    middle_file_name = f"{asm_file}t"
    fwrite_line("", middle_file_name, "w", "")
    with open(asm_file) as f:
        count_line = 0
        for line in f:
            parsed_line = parse_line(line)
            if parsed_line:
                if parsed_line[0] == "(":  # indicated label
                    parse_pseudo_command(line[1:], count_line)
                    continue
                count_line += 1
                fwrite_line(
                    parsed_line, middle_file_name, "a"
                )  # parseed line is saved into middle file
    return middle_file_name


# for each line it is A or C instruction,
# the translated result is out file
def second_pass(asm_file: str, out_file_name: str) -> None:
    fwrite_line("", out_file_name, "w", "")
    with open(asm_file) as f:
        # index for new allocated variables
        variable_index = 16
        for line in f:
            line = line.split("\n")[0]
            if line[0] == "@":  # indicates A instruction
                instruction, variable_index = translate_A_instruction(
                    line[1:], variable_index
                )
            else:
                instruction = translate_C_instruction(line)
            fwrite_line(instruction, out_file_name, "a")


# process file containts two passes
# first pass parses comments, spaces
# and saves lane labels in symbols, makes temporary file with .asmt
# on second pass the .asmt file is converted into .hack instructions
def process_file(asm_file: str) -> None:
    middle_file = first_pass(asm_file)
    second_pass(middle_file, f"{asm_file}.hack")


def assemble(asm_file: str) -> None:
    process_file(asm_file)
