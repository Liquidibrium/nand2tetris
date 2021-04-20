// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// n = R0
// m = R1
// mult = 0
// LOOP:
//     if m == 0 goto STOP
//     m -= 1
//     mult +=n
//     goto LOOP
// STOP:
//     R2 = mult

@R0
D=M
@n
M=D // n = R0
@R1
D=M
@m 
M=D // m =R1 
@mult 
M=0 // mult = 0
(LOOP)
@m
D=M
@STOP 
D;JEQ // if m == 0 goto STOP
D=D-1
@m 
M=D
@mult
D=M
@n
D=D+M
@mult
M=D // mult = mult + n
@LOOP
0;JMP
(STOP)
@mult
D=M
@R2
M=D // RAM[2] = mult
(END)
@END 
0;JMP 