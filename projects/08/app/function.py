count_call = 0


def function_command(function_name_lable, num_variables):
    result = (f"({function_name_lable})",)
    for _ in range(int(num_variables)):
        result += ("@SP", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1")
    return result


def pop_arg():
    return (
        "@ARG",
        "D=M",
        "@SP",
        "D=D+A",
        "@R13",
        "M=D",
        "@SP",
        "AM=M-1",
        "D=M",
        "@R13",
        "A=M",
        "M=D",
    )


def return_memory_segment(segment):
    return ("@R11", "D=M-1", "AM=D", "D=M", f"@{segment }", "M=D")


def return_command():
    p_arg = pop_arg()
    tmp1 = (
        "@LCL",
        "D=M",
        "@R11",
        "M=D",
        "@5",
        "A=D-A",
        "D=M",
        "@R12",
        "M=D",
    )
    tmp2 = (
        "@ARG",
        "D=M",
        "@SP",
        "M=D+1",
    )
    that = return_memory_segment("THAT")
    this = return_memory_segment("THIS")
    arg = return_memory_segment("ARG")
    lcl = return_memory_segment("LCL")
    tmp3 = ("@R12", "A=M", "0;JMP")
    return tmp1 + p_arg + tmp2 + that + this + arg + lcl + tmp3


def save_memory_segment(segment):
    return (
        f"//save {segment}",
        f"@{segment}",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
    )


def call(function_name, num_arguments, lable_pre=None):
    global count_call
    count_call += 1
    return_label = f"{function_name}$ret.{count_call}"
    pre = ("//call", f"@{return_label}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1")

    lcl = save_memory_segment("LCL")
    arg = save_memory_segment("ARG")
    this = save_memory_segment("THIS")
    that = save_memory_segment("THAT")
    post = (
        "@SP",
        "D=M",
        "@5",
        "D=D-A",
        f"@{num_arguments}",
        "D=D-A",
        "@ARG",
        "M=D",
        "@SP",
        "D=M",
        "@LCL",
        "M=D",
        f"@{function_name }",
        "0;JMP",
        f"({return_label })",
    )
    return pre + lcl + arg + this + that + post
