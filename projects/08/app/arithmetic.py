from typing import Callable, Dict, Tuple, Union

__count: int = 0


def __two_arg_func_to_asm(func: str) -> Tuple[str, ...]:
    # decrease *SP, save in A and M,
    # load last value in D,
    # decrease address/stack pointer
    # calculate function
    # and save in M

    return "@SP", "AM=M-1", "D=M", "A=A-1", f"M=M{func}D"


def __jump(cmd: str) -> Tuple[str, ...]:
    # jump function for lt, gt, eq
    # subtract last two values and result save in D reg
    # if (D {cmp} 0):
    #   then Ram[Ram[SP]-1] =  -1
    # else:  Ram[Ram[SP]-1] =  0
    global __count
    __count += 1
    label_true = f"LABEL.{cmd}.TRUE.{__count}"
    label_false = f"LABEL.{cmd}.FALSE.{__count}"
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


def __one_arg_func_to_asm(func: str) -> Tuple[str, ...]:
    return (
        "@SP",
        "A=M-1",
        f"M={func}M",
    )


arith_dict: Dict[str, Union[Callable[[], tuple]]] = {
    "add": lambda: ("//add ",) + __two_arg_func_to_asm("+"),
    "sub": lambda: ("//sub",) + __two_arg_func_to_asm("-"),
    "and": lambda: ("//and",) + __two_arg_func_to_asm("&"),
    "not": lambda: ("//not",) + __one_arg_func_to_asm("!"),
    "neg": lambda: ("//neg",) + __one_arg_func_to_asm("-"),
    "or": lambda: ("//or",) + __two_arg_func_to_asm("|"),
    "gt": lambda: __jump("GT"),
    "lt": lambda: __jump("LT"),
    "eq": lambda: __jump("EQ"),
}
