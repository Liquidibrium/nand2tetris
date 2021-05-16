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


def stack_eq() -> Tuple[str, ...]:
    return __jump("EQ")


def stack_lt() -> Tuple[str, ...]:
    return __jump("LT")


def stack_gt() -> Tuple[str, ...]:
    return __jump("GT")


def stack_neg() -> Tuple[str, ...]:
    return ("//neg",) + __one_arg_func_to_asm("-")


def stack_not() -> Tuple[str, ...]:
    return ("//not",) + __one_arg_func_to_asm("!")


def stack_or() -> Tuple[str, ...]:
    return ("//or",) + __two_arg_func_to_asm("|")


def stack_and() -> Tuple[str, ...]:
    return ("//and",) + __two_arg_func_to_asm("&")


def stack_sub() -> Tuple[str, ...]:
    return ("//sub",) + __two_arg_func_to_asm("-")


def stack_add() -> Tuple[str, ...]:
    return ("//add ",) + __two_arg_func_to_asm("+")


arith_dict: Dict[str, Union[Callable[[], tuple]]] = {
    "add": stack_add,
    "sub": stack_sub,
    "and": stack_and,
    "or": stack_or,
    "not": stack_not,
    "neg": stack_neg,
    "gt": stack_gt,
    "lt": stack_lt,
    "eq": stack_eq,
}
