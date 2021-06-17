from typing import TextIO

# command

CONST = "constant"
ARG = "argument"
LOCAL = "local"
THIS = "this"
THAT = "that"
POINTER = "pointer"
TEMP = "temp"
STATIC = "static"

ADD = "add"
SUB = "sub"
NEG = "neg"
EQ = "eq"
GT = "gt"
LT = "lt"
AND = "and"
OR = "or"
NOT = "not"

arith_dict = {
    "+": "add",
    "-": "sub",
    "!": "neg",
    "=": "eq",
    ">": "gt",
    "<": "lt",
    "&": "and",
    "|": "or",
    "~": "not",
}


class VMWriter:
    def __init__(self, vm_file: TextIO, class_name: str):
        self.vm_file = vm_file
        self.class_name = class_name

    def push(self, segment: str, index: int) -> None:
        self.vm_file.write(f"push {segment} {index}\n")

    def pop(self, segment: str, index: int) -> None:
        self.vm_file.write(f"pop {segment} {index}\n")

    def arithmetic(self, command: str) -> None:
        self.vm_file.write(f"{arith_dict[command]}\n")

    def label(self, label: str) -> None:
        self.vm_file.write(f"label {label}\n")

    def goto(self, label: str) -> None:
        self.vm_file.write(f"goto {label}\n")

    def w_if(self, label: str) -> None:
        self.vm_file.write(f"if-goto {label}\n")

    def call(self, name: str, num_args: int) -> None:
        self.vm_file.write(f"call {name} {num_args}\n")

    def function(self, name: str, num_locals: int) -> None:
        self.vm_file.write(f"function {self.class_name}.{name} {num_locals}\n")

    def w_return(self) -> None:
        self.vm_file.write("return\n")
