@256
D=A
@SP
M=D
//call
@Sys.init$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
//save LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//save ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//save THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//save THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@LCL
M=D
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Sys.init$ret.1)
(Sys.init)
//push const 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
//call
@Main.fibonacci$ret.2
D=A
@SP
A=M
M=D
@SP
M=M+1
//save LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//save ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//save THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//save THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@LCL
M=D
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.2)
//label
(Sys$WHILE)
//goto 
@Sys$WHILE
0;JMP
(Main.fibonacci)
//push ARG 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//push const 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//LT
@SP
AM=M-1
D=M
A=A-1
D=M-D
@LABEL.LT.TRUE.1
D;JLT
@SP
A=M-1
M=0
@LABEL.LT.FALSE.1
0;JMP
(LABEL.LT.TRUE.1)
@SP
A=M-1
M=-1
(LABEL.LT.FALSE.1)
//if goto 
@SP
AM=M-1
D=M
@Main$IF_TRUE
D;JNE
//goto 
@Main$IF_FALSE
0;JMP
//label
(Main$IF_TRUE)
//push ARG 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@ARG
D=M
@SP
D=D+A
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
D=M-1
AM=D
D=M
@THAT
M=D
@R13
D=M-1
AM=D
D=M
@THIS
M=D
@R13
D=M-1
AM=D
D=M
@ARG
M=D
@R13
D=M-1
AM=D
D=M
@LCL
M=D
@R14
A=M
0;JMP
//label
(Main$IF_FALSE)
//push ARG 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//push const 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
//call
@Main.fibonacci$ret.3
D=A
@SP
A=M
M=D
@SP
M=M+1
//save LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//save ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//save THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//save THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@LCL
M=D
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.3)
//push ARG 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//push const 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
//call
@Main.fibonacci$ret.4
D=A
@SP
A=M
M=D
@SP
M=M+1
//save LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//save ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//save THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//save THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@LCL
M=D
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.4)
//add 
@SP
AM=M-1
D=M
A=A-1
M=M+D
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@ARG
D=M
@SP
D=D+A
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
D=M-1
AM=D
D=M
@THAT
M=D
@R13
D=M-1
AM=D
D=M
@THIS
M=D
@R13
D=M-1
AM=D
D=M
@ARG
M=D
@R13
D=M-1
AM=D
D=M
@LCL
M=D
@R14
A=M
0;JMP
