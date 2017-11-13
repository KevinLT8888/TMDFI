#!/bin/python
import os,sys
from dump_reader import Dump
from binary_rewrite import rewrite32_little_endian

elf_name="/home/cas/tmp/empty"
if len(sys.argv)>1:
    elf_name=sys.argv[1]
dump_name=elf_name+"_dump"
os.system("/home/cas/fpga-zynq/rocket-chip/riscv-tools/bin/riscv64-unknown-elf-objdump -d %s > %s"% (elf_name, dump_name))
new_fname=elf_name+"_protected"

dump = Dump(dump_name)

# read ELF
content=None
with open(elf_name,'rb') as f:
    content=f.read()

# calculate file offset - VMA offset, file offset = ins.offset + bias
offset_bias = {}
output =  os.popen('/home/cas/fpga-zynq/rocket-chip/riscv-tools/bin/riscv64-unknown-elf-objdump -h %s' % elf_name)
index = 0
for line in output.readlines():
    if line.split() and line.split()[0].strip()==str(index):
        index += 1
        _, name, _ , vma, _, f_offset, _ = line.split(None,6)
        if name.strip()== '.text':
            offset_bias[name.strip()+'.unlikely']=int(f_offset,16)-int(vma,16)
        offset_bias[name.strip()]=int(f_offset,16)-int(vma,16)
        #print "Section: ", name, "\tvma:", vma, "\tfile offset", f_offset


# find instructions require rewrite
for i in dump.ins_lst:
    if i.ins.opcode==0b1101111 or (i.ins.opcode==0b1100111 and i.ins.funct3 == 0b000):
        if i.disasm.startswith("j"):
            if i.ins.rd == 1:  # call
                if i.ins.opcode==0b1101111: # jal
                    content=rewrite32_little_endian(content, i.add+offset_bias[i.section], i.ins.set_opcode(0b1101011))
                else:                        #jalr
                    content=rewrite32_little_endian(content, i.add+offset_bias[i.section], i.ins.set_funct3(0b111))
            elif i.ins.rd == 0: #jmp
                pass
            else:
                print (i.disasm)
        elif i.disasm.startswith("ret"):
            content=rewrite32_little_endian(content, i.add+offset_bias[i.section], i.ins.set_funct3(0b010))
        else:
            print (i.disasm)

with open(new_fname, 'wb') as f:
    f.write(content)



#with open(fname) as f:
#    with open(new_fname,'w') as nf:
#        for i in f.readline():
#            nf.write(protected(i))