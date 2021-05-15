# from os import TMP_MAX
import os
from typing import Tuple

filename = ""


class Command:
    @staticmethod
    def save_memory_value_in_D_register() -> Tuple:
        return ("D=M",)

    @staticmethod
    def stack_pointer_increment() -> Tuple:
        return ("@SP", "M=M+1")  # *SP ++

    @staticmethod
    def stack_pointer_decrement() -> Tuple:
        return ("@SP", "M=M-1")  # *SP--

    @staticmethod
    def get_stack_pointer_value_in_A() -> Tuple:
        return ("@SP", "A=M")  # A=*SP

    @staticmethod
    def SP_value_into_D() -> Tuple:  # D = RAM[SP]
        return ("@SP", "A=M", "D=M")

    @staticmethod
    def stack_save_d() -> Tuple:
        return ("@SP", "A=M", "M=D")  # *SP = D


class Arithmetic(Command):
    count = 0

    @staticmethod
    def stack_add() -> Tuple:
        return (
            "//add ",
            "@SP",
            "AM=M-1",
            "D=M",
            "A=A-1",
            "M=D+M",
        )

    @staticmethod
    def stack_sub() -> Tuple:
        return (
            "//sub",
            "@SP",
            "AM=M-1",
            "D=M",
            "A=A-1",
            "M=M-D",
        )

    @staticmethod
    def stack_and() -> Tuple:
        return (
            "//and",
            "@SP",
            "AM=M-1",
            "D=M",
            "A=A-1",
            "M=D&M",
        )

    @staticmethod
    def stack_or() -> Tuple:
        return (
            "//or",
            "@SP",
            "AM=M-1",
            "D=M",
            "A=A-1",
            "M=D|M",
        )

    @staticmethod
    def stack_not() -> Tuple:
        return (
            "//not",
            "@SP",
            "A=M-1",
            "M=!M",
        )

    @staticmethod
    def stack_neg() -> Tuple:
        return (
            "//neg",
            "@SP",
            "A=M-1",
            "M=-M",
        )

    @staticmethod
    def jump(cmd: str) -> Tuple:
        Arithmetic.count += 1
        label_true = f"LABEL.{cmd}.TRUE.{Arithmetic.count}"
        label_false = f"LABEL.{cmd}.FALSE.{Arithmetic.count}"
        return (
            f"//{cmd}",
            "@SP",
            "AM=M-1",
            "D=M",
            "A=A-1",
            "D=M-D",
            f"@{label_true}",
            f"D;J{cmd}",
            "@SP",
            "A=M-1",
            "M=0",
            f"@{label_false}",
            "0;JMP",
            f"({label_true})",
            "@SP",
            "A=M-1",
            "M=-1",
            f"({label_false})",
        )

    @staticmethod
    def stack_gt() -> Tuple:
        return Arithmetic.jump("GT")

    @staticmethod
    def stack_lt() -> Tuple:
        return Arithmetic.jump("LT")

    @staticmethod
    def stack_eq() -> Tuple:
        return Arithmetic.jump("EQ")


class MemoryAccess(Command):
    def __init__(self, name: str) -> None:
        self.name = name


class StackPush(MemoryAccess):
    @staticmethod
    def to_asm_code(segment: str, address: str) -> Tuple:
        if segment == "constant":
            return StackPush.constat(address)
        elif segment == "static":
            return StackPush.static(address)
        elif segment == "temp":
            return StackPush.segment_pointer("R5", address, "A")
        elif segment == "local":
            return StackPush.segment_pointer("LCL", address)
        elif segment == "argument":
            return StackPush.segment_pointer("ARG", address)
        elif segment == "pointer":
            if address == '0':
                return ("//pointer", "@THIS", "D=M")
            return ("//pointer", "@THAT", "D=M")
            # return StackPush.segment_pointer("R3", address, "A")
        else:
            return StackPush.segment_pointer(segment.upper(), address)

    @staticmethod
    def static(address: str) -> Tuple:  # file.address
        return (f"//push static {address}", f"@{filename}.{address}", "D=M")

    @staticmethod
    def constat(address: str) -> Tuple:
        return (f"//push const {address}", f"@{address}", "D=A")

    # local/argument/this/that memo = 'm'  ||   memo = "A" | temp R(5+index), pointer - R(3 + index)
    @staticmethod
    def segment_pointer(
        segment: str, address: str, memo: str = "M"
    ) -> Tuple:  # A -temp, pointer
        return (
            f"//push {segment} {address}",
            f"@{address}",
            "D=A",
            f"@{segment}",
            f"A={memo}+D",
            "D=M",
        )  # D =*SP


class StackPop(MemoryAccess):
    @staticmethod
    def to_asm_code(segment: str, address: str) -> Tuple:
        if segment == "static":
            return StackPop.static(address)
        elif segment == "temp":
            return StackPop.segment_pointer("R5", address, "A")
        elif segment == "local":
            return StackPop.segment_pointer("LCL", address)
        elif segment == "argument":
            return StackPop.segment_pointer("ARG", address)
        elif segment == "pointer":
            if address == '0':
                return ("//pointer", "@THIS", "D=A")
            return ("//pointer", "@THAT", "D=A")
            # return StackPop.segment_pointer("R3", address, "A")
        else:
            return StackPop.segment_pointer(segment.upper(), address)

    @staticmethod
    def static(address: str) -> Tuple:
        return (f"//pop static {address}", f"@{filename}.{address}", "D=A")

    @staticmethod
    def segment_pointer(segment: str, address: str, memo: str = "M") -> Tuple:
        return (
            f"//pop {segment} {address}",
            f"@{segment}",
            f"D={memo}",
            f"@{address}",
            "D=D+A",
        )


Arith_dict = {
    "add": Arithmetic.stack_add,
    "sub": Arithmetic.stack_sub,
    "and": Arithmetic.stack_and,
    "or": Arithmetic.stack_or,
    "not": Arithmetic.stack_not,
    "neg": Arithmetic.stack_neg,
    "gt": Arithmetic.stack_gt,
    "lt": Arithmetic.stack_lt,
    "eq": Arithmetic.stack_eq,
}
#########

# push D -> *SP++
PUSH = ("@SP", "A=M", "M=D", "@SP", "M=M+1")

# pop *SP-- -> *D
POP = ("@R13", "M=D", "@SP", "AM=M-1", "D=M", "@R13", "A=M", "M=D")


def translate_line(line: str) -> Tuple:
    words = line.split()
    if words[0] == "push":
        return StackPush.to_asm_code(words[1], words[2]) + PUSH
    elif words[0] == "pop":
        return StackPop.to_asm_code(words[1], words[2]) + POP

    arith_func = Arith_dict[words[0]]
    return arith_func()


def write_line(line: str, file_name: str, mode: str, line_end: str = "\n") -> None:
    with open(file_name, mode) as f:
        print(line, end=line_end, file=f)


# remove commnets and white spaces from begining and end of line
def filter_line(line: str) -> str:
    index = line.find("//")
    if index != -1:
        line = line[:index]
    return line.strip()


def translate(vm_file_name: str) -> None:
    global filename
    head, filename = os.path.split(vm_file_name)
    file_name = vm_file_name.split(".vm")[0]
    write_line("", file_name + ".asm", "w", "")
    with open(vm_file_name, "r") as file_to_translate:
        for line in file_to_translate:
            filtered_line = filter_line(line)
            if filtered_line:
                result = translate_line(filtered_line)
                assambled = "\n".join(result)
                write_line(assambled, file_name + ".asm", "a")
