from typing import Tuple


def goto(label_name: str) -> Tuple:
    return ("//goto ", f"@{label_name}", "0;JMP")


def if_goto(label_name: str) -> Tuple[str, ...]:
    return ("//if goto ", "@SP", "AM=M-1", "D=M", f"@{label_name}", "D;JNE")  # "A=A-1",


def label(label_name: str) -> Tuple:
    return ("//label", f"({label_name})")
