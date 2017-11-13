#!/bin/python
from binary_rewrite import rewrite32_little_endian
from tiny_disasm import Ins

opcodelen=7
funlen=3
def binfix(num,width):
    return bin(num)[2:].zfill(width)
while 1:
    print("Print your riscv ins,input 0 to quit:")
    string=input()
    b = int(string,16)
    if b==0:
        print("Quiting")
        break
    a= Ins(b)
    print("opcode:" + binfix(a.opcode,opcodelen))
    print("rd: " + "%d" % a.rd)
    print("rs: " + "%d" % a.rs1)
    print("fun3:" + binfix(a.funct3,funlen))


#target = "/home/cas/tmp/hello.riscv"

