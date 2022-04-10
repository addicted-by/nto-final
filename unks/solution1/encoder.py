#!/usr/bin/python3
def encoder(filein,fileout):
    blocksize=7
    while True:
        s=filein.read(blocksize)
        if not s:
            break
        fileout.write(s)
