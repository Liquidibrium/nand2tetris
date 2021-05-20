from typing import Tuple

count_call: int = 0

# same as Stack._PUSH
PUSH_D_IN_STACK: Tuple[str, ...] = ("@SP", "A=M", "M=D", "@SP", "M=M+1")


def function_command(function_name_label: str, num_variables: str) -> Tuple[str, ...]:
    result: Tuple[str, ...] = (f"({function_name_label})",)
    for _ in range(int(num_variables)):
        result += ("@0", "D=A") + PUSH_D_IN_STACK
    return result


# restore memory segment from temp R13 , endFrame--
def _return_memory_segment(segment: str) -> Tuple:
    return ("@R13", "D=M-1", "AM=D", "D=M", f"@{segment }", "M=D")


def return_command() -> Tuple:
    init_return = (
        # store endframe in temp reg 13
        "@LCL",
        "D=M",
        "@R13",
        "M=D",
        # save return address (endframe - 5) in temp register 14
        "@5",
        "A=D-A",
        "D=M",
        "@R14",
        "M=D",
        "@ARG",  # return value into arg
        "D=M",
        "@SP",
        "D=D+A",
        # pop from stack , same as StackPop._POP, used temp register  R15
        "@R15",
        "M=D",
        "@SP",
        "AM=M-1",
        "D=M",
        "@R15",
        "A=M",
        "M=D",
        # SP = ARG + 1
        "@ARG",
        "D=M",
        "@SP",
        "M=D+1",
    )
    that = _return_memory_segment("THAT")
    this = _return_memory_segment("THIS")
    arg = _return_memory_segment("ARG")
    lcl = _return_memory_segment("LCL")
    # goto  saved return address saved in R14
    goto_ret = ("@R14", "A=M", "0;JMP")
    return init_return + that + this + arg + lcl + goto_ret


def _save_memory_segment(segment: str) -> Tuple:
    return (
        f"//save {segment}",
        f"@{segment}",
        "D=M",
    ) + PUSH_D_IN_STACK


def call_command(function_name: str, num_arguments: str) -> Tuple[str, ...]:
    global count_call
    count_call += 1
    return_label = f"{function_name}$ret.{count_call}"
    save_return_address = ("//call", f"@{return_label}", "D=A") + PUSH_D_IN_STACK

    save_lcl = _save_memory_segment("LCL")
    save_arg = _save_memory_segment("ARG")
    save_this = _save_memory_segment("THIS")
    save_that = _save_memory_segment("THAT")
    end_call = (
        # reposition ARG
        "@SP",
        "D=M",
        f"@{int(num_arguments)+5}",  # calculate return address
        "D=D-A",
        "@ARG",
        "M=D",
        # reposition LCL
        "@SP",
        "D=M",
        "@LCL",
        "M=D",
        # goto function
        f"@{function_name }",
        "0;JMP",
        # return address label
        f"({return_label })",
    )
    return save_return_address + save_lcl + save_arg + save_this + save_that + end_call


# Bootstrap code
# SP = 256
# call Sys.init
def init_asm_code(file_name: str) -> Tuple[str, ...]:
    return (
        "@256",
        "D=A",
        "@SP",
        "M=D",
    ) + call_command("Sys.init", "0")
