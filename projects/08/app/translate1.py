import os
from typing import List, Tuple

from .Arithmetic import arith_dict

VM_FILE_EXT: str = ".vm"
ASM_FILE_EXT: str = ".asm"
# file name without path and extension
_file_name_global: str = ""


class MemoryCommand:
    @staticmethod
    def to_asm_code(segment: str, address: str) -> Tuple[str, ...]:
        pass

    @staticmethod
    def _filter_segment(segment: str, address: str) -> Tuple[str, ...]:
        pass

    @staticmethod
    def _static(address: str, file_name: str) -> Tuple[str, ...]:
        pass

    @staticmethod
    # local/argument/this/that  || temp R5, memo = "A"
    def _segment_pointer(
        segment: str, address: str, memory_location: str = "M"
    ) -> Tuple[str, ...]:
        pass

    @staticmethod
    def _pointer(segment: str) -> Tuple[str, ...]:
        pass

    @staticmethod
    def _constant(address: str) -> Tuple[str, ...]:
        pass


class StackPush(MemoryCommand):
    # *SP=D , *SP++
    __PUSH: Tuple[str, ...] = ("@SP", "A=M", "M=D", "@SP", "M=M+1")

    @staticmethod
    def to_asm_code(segment: str, address: str) -> Tuple[str, ...]:
        return StackPush._filter_segment(segment, address) + StackPush.__PUSH

    @staticmethod
    def _filter_segment(segment: str, address: str) -> Tuple[str, ...]:
        if segment == "constant":
            return StackPush._constant(address)
        elif segment == "static":
            return StackPush._static(address, _file_name_global)
        elif segment == "temp":
            return StackPush._segment_pointer("R5", address, "A")
        elif segment == "local":
            return StackPush._segment_pointer("LCL", address)
        elif segment == "argument":
            return StackPush._segment_pointer("ARG", address)
        elif segment == "pointer":
            if address == "0":
                return StackPush._pointer("THIS")
            return StackPush._pointer("THAT")
        else:  # THIS/THAT
            return StackPush._segment_pointer(segment.upper(), address)

    @staticmethod
    def _static(address: str, file_name: str) -> Tuple[str, ...]:  # file.address
        return (
            f"//push static {address}",
            f"@{file_name}.{address}",
            "D=M",
        )

    @staticmethod
    def _pointer(segment: str) -> Tuple[str, ...]:
        return "//pointer", f"@{segment}", "D=M"

    @staticmethod
    def _constant(address: str) -> Tuple[str, ...]:
        return f"//push const {address}", f"@{address}", "D=A"

    @staticmethod
    def _segment_pointer(
        segment: str, address: str, memory_location: str = "M"
    ) -> Tuple[str, ...]:
        return (
            f"//push {segment} {address}",
            f"@{address}",
            "D=A",
            f"@{segment}",
            f"A={memory_location}+D",  # calculate ptr = (segment + address)
            "D=M",  # save value,  D = *ptr
        )


class StackPop(MemoryCommand):
    # *SP-- = *D
    # use R13 to save D, *R13 = D
    # *SP-- , D=*SP , **R13 = D
    _POP: Tuple[str, ...] = (
        "@R13",
        "M=D",
        "@SP",
        "AM=M-1",
        "D=M",
        "@R13",
        "A=M",
        "M=D",
    )

    @staticmethod
    def to_asm_code(segment: str, address: str) -> Tuple[str, ...]:
        return StackPop._filter_segment(segment, address) + StackPop._POP

    @staticmethod
    def _filter_segment(segment: str, address: str) -> Tuple[str, ...]:
        if segment == "static":
            return StackPop._static(address, _file_name_global)
        elif segment == "temp":
            return StackPop._segment_pointer("R5", address, "A")
        elif segment == "local":
            return StackPop._segment_pointer("LCL", address)
        elif segment == "argument":
            return StackPop._segment_pointer("ARG", address)
        elif segment == "pointer":
            if address == "0":
                return StackPop._pointer("THIS")
            return StackPop._pointer("THAT")
        else:  # THIS/THAT
            return StackPop._segment_pointer(segment.upper(), address)

    @staticmethod
    def _static(address: str, file_name: str) -> Tuple[str, ...]:
        return f"//pop static {address}", f"@{file_name}.{address}", "D=A"

    @staticmethod
    def _pointer(segment: str) -> Tuple[str, ...]:
        return "//pointer", f"@{segment}", "D=A"

    @staticmethod
    def _segment_pointer(
        segment: str, address: str, memory_location: str = "M"
    ) -> Tuple[str, ...]:
        return (
            f"//pop {segment} {address}",
            f"@{segment}",
            f"D={memory_location}",
            f"@{address}",
            "D=D+A",
        )


def translate_line(line: str) -> Tuple[str, ...]:
    words: List[str] = line.split()  # split spaces

    if len(words) == 3:
        if words[0] == "push":
            return StackPush.to_asm_code(words[1], words[2])
        elif words[0] == "pop":
            return StackPop.to_asm_code(words[1], words[2])

    # if first word is not push or pop then it is arithmetic command
    arith_func = arith_dict[words[0]]
    return arith_func()


# remove comments and white spaces from beginning and end of line
def filter_line(line: str) -> str:
    index: int = line.find("//")
    if index != -1:
        line = line[:index]
    return line.strip()


def translate(vm_file_name: str) -> None:
    global _file_name_global
    file_name_without_ext = vm_file_name.split(VM_FILE_EXT)[0]
    _, _file_name_global = os.path.split(file_name_without_ext)

    asm_file_name: str = file_name_without_ext + ASM_FILE_EXT

    with open(vm_file_name, "r") as file_to_read, open(
        asm_file_name, "w"
    ) as file_to_write:
        for line in file_to_read:
            filtered_line: str = filter_line(line)
            if filtered_line:
                # each element in result indicates new line in asm file
                result: Tuple = translate_line(filtered_line)
                assembled: str = "\n".join(result) + "\n"
                file_to_write.writelines(assembled)
