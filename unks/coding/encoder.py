#!/usr/bin/python3

from support import * 

def encoder(filein,fileout):
    blocksize=8
    check_bits = [i for i in range(1, blocksize + 1) if not i & (i - 1)]
    while True:
        s=filein.read(blocksize)
        if not s:
            break
        result = set_check_bits(chars_to_bin(s), check_bits)
        fileout.write(result)