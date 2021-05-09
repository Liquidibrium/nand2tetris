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

# global index for new allocated variables
global_variable_index = 16

# remove comments, which begins with //
# and remove space, new line and tab characters from line
def parse_line(line):
    index = line.find("//")
    if index != -1:
        line = line[:index]
    return line.replace(" ", "").replace("\n", "").replace("\t", "")


# translates line to A instruction,
# the returned value is 16 byte long string,
# instruction line is passed without "@,
# if label is in symbool table,
# then the proper value is returned
# if not in symbols, new variable is allocated,
# variable and variable index is add in symbols
def translate_A_instruction(instruction_line):
    if instruction_line[0].isdigit():
        address = int(instruction_line)
    elif instruction_line in symbols:
        address = symbols[instruction_line]
    else:
        global global_variable_index
        symbols[instruction_line] = global_variable_index
        address = global_variable_index
        global_variable_index += 1
    return format(address, "016b")


# translates line into c binary code
# instructuin line is looke like this
# dest = comp ; jump
# dest and jump is optional
# so dest_dict and jump_dict contains "" as key for null 
def translate_C_instruction(instruction_line):
    dest_end_index = instruction_line.find("=")
    compare_start_index = dest_end_index + 1
    if dest_end_index == -1:
        compare_start_index = dest_end_index = 0
    destination = dest_dict[instruction_line[:dest_end_index]]

    compare_end_index = instruction_line.find(";")
    jumber_start_index = compare_end_index + 1
    if compare_end_index == -1:
        jumber_start_index = compare_end_index = len(instruction_line)

    compare = comp_dict[instruction_line[compare_start_index:compare_end_index]]
    jumper = jump_dict[instruction_line[jumber_start_index:]]
    return "111" + compare + destination + jumper


# lable is add in symbols with line number
def parse_pseudo_command(line: str, line_number: int):
    label_symbol = line[:-1]
    symbols[label_symbol] = line_number


# append line to file
def fwrite_line(instruction_line, file_name):
    with open(file_name, "a") as f:
        print(instruction_line, file=f)


# filters commnets, spaces and
# adds labels with proper line number value into symbols
# middle file is generated and to extension is added t /.asmt
# middle file name is returned 
def first_pass(asm_file):
    middle_file_name = f"{asm_file}t"
    with open(asm_file) as f:
        count_line = 0
        for line in f:
            parsed_line = parse_line(line)
            if parsed_line:
                if parsed_line[0] == "(": # indicated label 
                    parse_pseudo_command(line[1:], count_line)
                    continue
                count_line += 1
                fwrite_line(parsed_line, middle_file_name) # parseed line is saved into middle file
    return middle_file_name


# for each line it is A or C instruction,
# the translated result is out file
def second_pass(asm_file, out_file_name):
    with open(asm_file) as f:
        for line in f:
            line = line.split("\n")[0]
            if line[0] == "@": # indicates A instruction 
                instruction = translate_A_instruction(line[1:])
            else:
                instruction = translate_C_instruction(line)
            fwrite_line(instruction, out_file_name)


# process file containts two passes
# first pass parses comments, spaces
# and saves lane labels in symbols, makes temporary file with .asmt
# on second pass the .asmt file is converted into .hack instructions
def process_file(asm_file: str) -> None:
    # file_name = asm_file.split(".asm")[0]
    middle_file = first_pass(asm_file)
    second_pass(middle_file, f"{asm_file}.hack")


def assemble(asm_file: str) -> None:
    process_file(asm_file)
