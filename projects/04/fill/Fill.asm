// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
// WHILE: // while true 
//     index = screen
//     if RAM[KBD] > 0 : color = -1
//     else : color = 0

//     LOOP:
//         if index == KBD : goto WHILE
//         else : 
//             RAM[index]=color
//             idnex = index + 1 
//             goto LOOP

(WHILE) // while true 
@SCREEN
D=A
@index // index is at the first pixel of screen// 
M=D     // index = screen 
@KBD
D=M 
@BLACK
D;JGT   // if pressed then color is  black
@color
M=0 // color is white
@LOOP
0;JMP // goto LOOP
(BLACK) 
@color 
M=-1
(LOOP)
@KBD // KBD-1 is last 16 pixel of screen, so this works 
D=A
@index
D=D-M
@WHILE 
D;JEQ // if index is out of the screen
@color
D=M 
@index // RAM[index]=color
A=M
M=D
@index 
D=M 
M=D+1  // index ++ 
@LOOP
0;JMP

