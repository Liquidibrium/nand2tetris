# Your code starts here:
import os
from typing import List, TextIO, Tuple

from .arithmetic import arith_dict
from .memory import *
from .function import *
from .branching import *

VM_FILE_EXT: str = ".vm"
ASM_FILE_EXT: str = ".asm"


# file name without path and extension


def translate_line(line: str, file_name: str) -> Tuple[str, ...]:
    words: List[str] = line.split()  # split spaces
    if len(words) == 1:
        if words[0] == "return":
            return return_command()
    if len(words) == 3:
        if words[0] == "push":
            return StackPush.to_asm_code(words[1], words[2], file_name)
        if words[0] == "pop":
            return StackPop.to_asm_code(words[1], words[2], file_name)
        if words[0] == "call":
            return call(words[1], words[2], f"{file_name}.{words[1]}$")
        if words[0] == "function":
            return function_command(f"{words[1]}", words[2])

    if len(words) == 2:
        if words[0] == "label":
            return label(f"{file_name}${words[1]}")
        if words[0] == "if-goto":
            return if_goto(f"{file_name}${words[1]}")
        if words[0] == "goto":
            return goto(f"{file_name}${words[1]}")

    # if first word is not push or pop then it is arithmetic command
    arith_func = arith_dict[words[0]]
    return arith_func()


# remove comments and white spaces from beginning and end of line
def filter_line(line: str) -> str:
    index: int = line.find("//")
    if index != -1:
        line = line[:index]
    return line.strip()


# Bootstrap code
# SP = 256
# call Sys.init
def init_asm_code(file_name):
    return ("@256", "D=A", "@SP", "M=D",) + call(
        "Sys.init", 0
    )  # , f"{file_name}$ret.")


def write_in_file(file, asm_lines):
    assembled: str = "\n".join(asm_lines) + "\n"
    file.writelines(assembled)


def translate_file(file_to_read, file_to_write, vm_file_name_without_ext):
    # path_to_vm_file = os.join(path_to_directory, vm_file_name_without_ext + VM_FILE_EXT)
    for line in file_to_read:
        filtered_line: str = filter_line(line)
        if filtered_line:
            # each element in result indicates new line in asm file
            result: Tuple = translate_line(filtered_line, vm_file_name_without_ext)
            write_in_file(file_to_write, result)


def translate(vm_file_or_directory_name: str) -> None:
    if os.path.isdir(vm_file_or_directory_name):
        directory_name = os.path.basename(os.path.dirname(vm_file_or_directory_name))
        path_to_asm_file = os.path.join(
            vm_file_or_directory_name, directory_name + ASM_FILE_EXT
        )
        with open(path_to_asm_file, "w") as file_to_write:
            write_in_file(file_to_write, init_asm_code(directory_name))
            for file_name in os.listdir(vm_file_or_directory_name):
                if file_name.endswith(VM_FILE_EXT):
                    path_to_vm_file = os.path.join(vm_file_or_directory_name, file_name)
                    with open(path_to_vm_file, "r") as file_to_read:
                        translate_file(
                            file_to_read, file_to_write, file_name.split(VM_FILE_EXT)[0]
                        )
    else:
        path_to_file_without_ext = vm_file_or_directory_name.split(VM_FILE_EXT)[0]
        _, vm_file_name_without_ext = os.path.split(path_to_file_without_ext)
        path_to_asm_file: str = path_to_file_without_ext + ASM_FILE_EXT
        with open(path_to_asm_file, "w") as file_to_write, open(
            vm_file_or_directory_name, "r"
        ) as file_to_read:
            write_in_file(file_to_write, init_asm_code(vm_file_name_without_ext))
            translate_file(file_to_read, file_to_write, vm_file_name_without_ext)
