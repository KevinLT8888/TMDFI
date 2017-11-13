#!/bin/python

# This little module disasm some of riscv instructions, and point out the rd, rs1, rs2

import functools
from spike_disasm import spike_disasm

class Ins(int):
    def __init__(self, ins):
        if isinstance(ins,str):
            self = int(ins, 16)
        elif isinstance(ins,int):
            self = ins
        else:
            raise Exception
        if self>0xFFFFFFFF:
            raise Exception

    @property
    def spike_disasm(self):
        return spike_disasm(self)

    @property
    def rd(self):
        return (self & 0x00000FE0) >> 7

    @property
    def rs1(self):
        return (self & 0xF8000) >> 15

    @property
    def opcode(self):
        return self & 0x7F

    def set_opcode(self, value):
        new_ins =Ins((self & 0xFFFFFF80) + value)
        return new_ins

    @property
    def funct3(self):
        return (self & 0x7000) >> 12

    def set_funct3(self, value):
        new_ins = Ins((self & 0xFFFF8FFF) | (value << 12))
        return new_ins

#a=Ins(0x000280e7)
#print a.funct3
##a=a.set_opcode(0b1111111)
#print a.spike_disasm
#print hex(a)