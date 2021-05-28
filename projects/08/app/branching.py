from typing import Tuple


def _goto(label_name: str) -> Tuple[str, ...]:
    return "//goto ", f"@{label_name}", "0;JMP"


def _if_goto(label_name: str) -> Tuple[str, ...]:
    return "//if goto ", "@SP", "AM=M-1", "D=M", f"@{label_name}", "D;JNE"


def _label(label_name: str) -> Tuple[str, ...]:
    return "//label", f"({label_name})"


# can be rewritten only with lambda function
branch_dict = {"goto": _goto, "if-goto": _if_goto, "label": _label}
