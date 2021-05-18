# Your code starts here:
import os
from typing import List, Tuple

from .Arithmetic import arith_dict
from .memory import *

VM_FILE_EXT: str = ".vm"
ASM_FILE_EXT: str = ".asm"


# file name without path and extension


def translate_line(line: str, file_name: str) -> Tuple[str, ...]:
    words: List[str] = line.split()  # split spaces

    if len(words) == 3:
        if words[0] == "push":
            return StackPush.to_asm_code(words[1], words[2], file_name)
        elif words[0] == "pop":
            return StackPop.to_asm_code(words[1], words[2], file_name)

    # if first word is not push or pop then it is arithmetic command
    arith_func = arith_dict[words[0]]
    return arith_func()

# Bootstrap code
# SP = 256
# call Sys.init

# remove comments and white spaces from beginning and end of line
def filter_line(line: str) -> str:
    index: int = line.find("//")
    if index != -1:
        line = line[:index]
    return line.strip()


def translate(vm_file_or_directory_name: str) -> None:
    if os.path.isdir(vm_file_or_directory_name):
        pass
    else:
        pass
    file_name_without_ext = vm_file_or_directory_name.split(VM_FILE_EXT)[0]
    _, _file_name_global = os.path.split(file_name_without_ext)

    asm_file_name: str = file_name_without_ext + ASM_FILE_EXT

    with open(vm_file_or_directory_name, "r") as file_to_read, open(
            asm_file_name, "w"
    ) as file_to_write:
        for line in file_to_read:
            filtered_line: str = filter_line(line)
            if filtered_line:
                # each element in result indicates new line in asm file
                result: Tuple = translate_line(filtered_line, _file_name_global)
                assembled: str = "\n".join(result) + "\n"
                file_to_write.writelines(assembled)
