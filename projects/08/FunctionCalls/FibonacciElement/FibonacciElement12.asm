@256 // 0
D=A // 1
@SP // 2
M=D // 3
@Sys.initRET0 // 4
D=A // 5
@SP // 6
A=M // 7
M=D // 8
@SP // 9
M=M+1 // 10
@LCL // 11
D=M // 12
@SP // 13
A=M // 14
M=D // 15
@SP // 16
M=M+1 // 17
@ARG // 18
D=M // 19
@SP // 20
A=M // 21
M=D // 22
@SP // 23
M=M+1 // 24
@THIS // 25
D=M // 26
@SP // 27
A=M // 28
M=D // 29
@SP // 30
M=M+1 // 31
@THAT // 32
D=M // 33
@SP // 34
A=M // 35
M=D // 36
@SP // 37
M=M+1 // 38
@SP // 39
D=M // 40
@LCL // 41
M=D // 42
@5 // 43
D=D-A // 44
@ARG // 45
M=D // 46
@Sys.init // 47
0;JMP // 48
(Sys.initRET0)
//////
// Sys
// function Sys.init 0
(Sys.init)
// push constant 4
@4 // 49
D=A // 50
@SP // 51
A=M // 52
M=D // 53
@SP // 54
M=M+1 // 55
// call Main.fibonacci 1
@Main.fibonacciRET1 // 56
D=A // 57
@SP // 58
A=M // 59
M=D // 60
@SP // 61
M=M+1 // 62
@LCL // 63
D=M // 64
@SP // 65
A=M // 66
M=D // 67
@SP // 68
M=M+1 // 69
@ARG // 70
D=M // 71
@SP // 72
A=M // 73
M=D // 74
@SP // 75
M=M+1 // 76
@THIS // 77
D=M // 78
@SP // 79
A=M // 80
M=D // 81
@SP // 82
M=M+1 // 83
@THAT // 84
D=M // 85
@SP // 86
A=M // 87
M=D // 88
@SP // 89
M=M+1 // 90
@SP // 91
D=M // 92
@LCL // 93
M=D // 94
@6 // 95
D=D-A // 96
@ARG // 97
M=D // 98
@Main.fibonacci // 99
0;JMP // 100
(Main.fibonacciRET1)
// label WHILE
(Sys$WHILE)
// goto WHILE
@Sys$WHILE // 101
0;JMP // 102
//////
// Main
// function Main.fibonacci 0
(Main.fibonacci)
// push argument 0
@ARG // 103
D=M // 104
@0 // 105
A=D+A // 106
D=M // 107
@SP // 108
A=M // 109
M=D // 110
@SP // 111
M=M+1 // 112
// push constant 2
@2 // 113
D=A // 114
@SP // 115
A=M // 116
M=D // 117
@SP // 118
M=M+1 // 119
// lt
@SP // 120
M=M-1 // 121
A=M // 122
D=M // 123
@SP // 124
M=M-1 // 125
@SP // 126
A=M // 127
D=M-D // 128
@BOOL0 // 129
D;JLT // 130
@SP // 131
A=M // 132
M=0 // 133
@ENDBOOL0 // 134
0;JMP // 135
(BOOL0)
@SP // 136
A=M // 137
M=-1 // 138
(ENDBOOL0)
@SP // 139
M=M+1 // 140
// if-goto IF_TRUE
@SP // 141
M=M-1 // 142
A=M // 143
D=M // 144
@Main$IF_TRUE // 145
D;JNE // 146
// goto IF_FALSE
@Main$IF_FALSE // 147
0;JMP // 148
// label IF_TRUE
(Main$IF_TRUE)
// push argument 0
@ARG // 149
D=M // 150
@0 // 151
A=D+A // 152
D=M // 153
@SP // 154
A=M // 155
M=D // 156
@SP // 157
M=M+1 // 158
// return
@LCL // 159
D=M // 160
@R13 // 161
M=D // 162
@R13 // 163
D=M // 164
@5 // 165
D=D-A // 166
A=D // 167
D=M // 168
@R14 // 169
M=D // 170
@SP // 171
M=M-1 // 172
A=M // 173
D=M // 174
@ARG // 175
A=M // 176
M=D // 177
@ARG // 178
D=M // 179
@SP // 180
M=D+1 // 181
@R13 // 182
D=M // 183
@1 // 184
D=D-A // 185
A=D // 186
D=M // 187
@THAT // 188
M=D // 189
@R13 // 190
D=M // 191
@2 // 192
D=D-A // 193
A=D // 194
D=M // 195
@THIS // 196
M=D // 197
@R13 // 198
D=M // 199
@3 // 200
D=D-A // 201
A=D // 202
D=M // 203
@ARG // 204
M=D // 205
@R13 // 206
D=M // 207
@4 // 208
D=D-A // 209
A=D // 210
D=M // 211
@LCL // 212
M=D // 213
@R14 // 214
A=M // 215
0;JMP // 216
// label IF_FALSE
(Main$IF_FALSE)
// push argument 0
@ARG // 217
D=M // 218
@0 // 219
A=D+A // 220
D=M // 221
@SP // 222
A=M // 223
M=D // 224
@SP // 225
M=M+1 // 226
// push constant 2
@2 // 227
D=A // 228
@SP // 229
A=M // 230
M=D // 231
@SP // 232
M=M+1 // 233
// sub
@SP // 234
M=M-1 // 235
A=M // 236
D=M // 237
@SP // 238
M=M-1 // 239
@SP // 240
A=M // 241
M=M-D // 242
@SP // 243
M=M+1 // 244
// call Main.fibonacci 1
@Main.fibonacciRET2 // 245
D=A // 246
@SP // 247
A=M // 248
M=D // 249
@SP // 250
M=M+1 // 251
@LCL // 252
D=M // 253
@SP // 254
A=M // 255
M=D // 256
@SP // 257
M=M+1 // 258
@ARG // 259
D=M // 260
@SP // 261
A=M // 262
M=D // 263
@SP // 264
M=M+1 // 265
@THIS // 266
D=M // 267
@SP // 268
A=M // 269
M=D // 270
@SP // 271
M=M+1 // 272
@THAT // 273
D=M // 274
@SP // 275
A=M // 276
M=D // 277
@SP // 278
M=M+1 // 279
@SP // 280
D=M // 281
@LCL // 282
M=D // 283
@6 // 284
D=D-A // 285
@ARG // 286
M=D // 287
@Main.fibonacci // 288
0;JMP // 289
(Main.fibonacciRET2)
// push argument 0
@ARG // 290
D=M // 291
@0 // 292
A=D+A // 293
D=M // 294
@SP // 295
A=M // 296
M=D // 297
@SP // 298
M=M+1 // 299
// push constant 1
@1 // 300
D=A // 301
@SP // 302
A=M // 303
M=D // 304
@SP // 305
M=M+1 // 306
// sub
@SP // 307
M=M-1 // 308
A=M // 309
D=M // 310
@SP // 311
M=M-1 // 312
@SP // 313
A=M // 314
M=M-D // 315
@SP // 316
M=M+1 // 317
// call Main.fibonacci 1
@Main.fibonacciRET3 // 318
D=A // 319
@SP // 320
A=M // 321
M=D // 322
@SP // 323
M=M+1 // 324
@LCL // 325
D=M // 326
@SP // 327
A=M // 328
M=D // 329
@SP // 330
M=M+1 // 331
@ARG // 332
D=M // 333
@SP // 334
A=M // 335
M=D // 336
@SP // 337
M=M+1 // 338
@THIS // 339
D=M // 340
@SP // 341
A=M // 342
M=D // 343
@SP // 344
M=M+1 // 345
@THAT // 346
D=M // 347
@SP // 348
A=M // 349
M=D // 350
@SP // 351
M=M+1 // 352
@SP // 353
D=M // 354
@LCL // 355
M=D // 356
@6 // 357
D=D-A // 358
@ARG // 359
M=D // 360
@Main.fibonacci // 361
0;JMP // 362
(Main.fibonacciRET3)
// add
@SP // 363
M=M-1 // 364
A=M // 365
D=M // 366
@SP // 367
M=M-1 // 368
@SP // 369
A=M // 370
M=M+D // 371
@SP // 372
M=M+1 // 373
// return
@LCL // 374
D=M // 375
@R13 // 376
M=D // 377
@R13 // 378
D=M // 379
@5 // 380
D=D-A // 381
A=D // 382
D=M // 383
@R14 // 384
M=D // 385
@SP // 386
M=M-1 // 387
A=M // 388
D=M // 389
@ARG // 390
A=M // 391
M=D // 392
@ARG // 393
D=M // 394
@SP // 395
M=D+1 // 396
@R13 // 397
D=M // 398
@1 // 399
D=D-A // 400
A=D // 401
D=M // 402
@THAT // 403
M=D // 404
@R13 // 405
D=M // 406
@2 // 407
D=D-A // 408
A=D // 409
D=M // 410
@THIS // 411
M=D // 412
@R13 // 413
D=M // 414
@3 // 415
D=D-A // 416
A=D // 417
D=M // 418
@ARG // 419
M=D // 420
@R13 // 421
D=M // 422
@4 // 423
D=D-A // 424
A=D // 425
D=M // 426
@LCL // 427
M=D // 428
@R14 // 429
A=M // 430
0;JMP // 431
