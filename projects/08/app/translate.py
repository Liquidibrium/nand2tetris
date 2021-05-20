# Your code starts here:
import os
from glob import glob
from typing import List, TextIO, Tuple

from .arithmetic import arith_dict
from .branching import branch_dict
from .function import call_command, function_command, init_asm_code, return_command
from .memory import StackPop, StackPush

VM_FILE_EXT: str = ".vm"
ASM_FILE_EXT: str = ".asm"
INIT_FILE_NAME: str = "Sys.vm"


# file name without path and extension


def translate_line(line: str, file_name: str) -> Tuple[str, ...]:
    words: List[str] = line.split()  # split spaces
    if len(words) == 2:
        branch_func = branch_dict[words[0]]
        return branch_func(f"{file_name}${words[1]}")

    if len(words) == 3:
        if words[0] == "push":
            return StackPush.to_asm_code(words[1], words[2], file_name)
        if words[0] == "pop":
            return StackPop.to_asm_code(words[1], words[2], file_name)
        if words[0] == "call":
            return call_command(words[1], words[2])
        if words[0] == "function":
            return function_command(words[1], words[2])

    if words[0] == "return":
        return return_command()
    # if first word is not push or pop then it is arithmetic command
    arith_func = arith_dict[words[0]]
    return arith_func()


# remove comments and white spaces from beginning and end of line
def filter_line(line: str) -> str:
    index: int = line.find("//")
    if index != -1:
        line = line[:index]
    return line.strip()


def write_in_file(file: TextIO, asm_lines: Tuple[str, ...]) -> None:
    assembled: str = "\n".join(asm_lines) + "\n"
    file.write(assembled)


def translate_file(
    file_to_read: TextIO, file_to_write: TextIO, vm_file_name_without_ext: str
) -> None:
    for line in file_to_read:
        filtered_line: str = filter_line(line)
        if filtered_line:
            # each element in result indicates new line in asm file
            result: Tuple = translate_line(filtered_line, vm_file_name_without_ext)
            write_in_file(file_to_write, result)


def translate(vm_file_or_directory_name: str) -> None:
    need_bootstrap: bool = False
    if os.path.isdir(vm_file_or_directory_name):

        directory_name = os.path.basename(os.path.dirname(vm_file_or_directory_name))
        # directory_name is same as translated asm file name
        path_to_asm_file = os.path.join(
            vm_file_or_directory_name, directory_name + ASM_FILE_EXT
        )
        # get all .vm files
        path_to_vm_files = glob(
            os.path.join(vm_file_or_directory_name, "*" + VM_FILE_EXT)
        )
        # check if bootstrap asm code is needed
        for s in path_to_vm_files:
            if INIT_FILE_NAME in s:
                need_bootstrap = True
                break
    else:
        path_to_file_without_ext = vm_file_or_directory_name.split(VM_FILE_EXT)[0]
        path_to_asm_file = path_to_file_without_ext + ASM_FILE_EXT
        path_to_vm_files = [vm_file_or_directory_name]

    with open(path_to_asm_file, "w") as file_to_write:
        if need_bootstrap:
            write_in_file(file_to_write, init_asm_code())
        for path_to_vm_file in path_to_vm_files:
            with open(path_to_vm_file, "r") as file_to_read:
                # get .vm file name without extension and path
                file_name = os.path.split(path_to_vm_file)[1].split(VM_FILE_EXT)[0]
                translate_file(file_to_read, file_to_write, file_name)
