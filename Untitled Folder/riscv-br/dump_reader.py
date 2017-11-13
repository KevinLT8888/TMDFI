#!/bin/python
from tiny_disasm import Ins

class Ins_data():
    def __init__(self, add, ins, disasm, section):
        self.add = add
        self.ins = Ins(ins)
        self.disasm = disasm
        self.section = section

class Dump():
    def __init__(self, path):
        with open(path, 'r') as f:
            current_section = ''
            self.ins_lst = []
            for line in f:
                if line.strip(): #not empty
                    if line.startswith('Disassembly of'):
                        current_section=line.split()[-1][:-1]
                    elif line.endswith('riscv\n'):
                        pass
                    elif line.endswith(':\n'):
                        pass
                    else:       # real instructions
                        add, ins, disasm =  line.split(None,2)
                        self.ins_lst.append(Ins_data(int(add[:-1],16),int(ins,16),disasm.strip(),current_section))



