#!/bin/python
import os

path_to_spike_dasm= "/home/cas/fpga-zynq/rocket-chip/riscv-tools/bin/spike-dasm"

def spike_disasm(ins):
    if isinstance(ins,str):
        ins = int(ins,16)
    output =  os.popen(('echo "DASM(%8X)" | ' % ins) + path_to_spike_dasm)
    return output.read().strip()
