def goto(label_name):
    return ("//goto ",f"@{label_name}", "0;JMP")


def if_goto(label_name):
    return ("//if goto ","@SP", "AM=M-1", "D=M", #"A=A-1",
             f"@{label_name}", "D;JNE")


def label(label_name):
    return ("//label",f"({label_name})")
