#!/usr/bin/python3
def encoder(filein,fileout):
    blocksize=9
    while True:
        s=filein.read(blocksize)
        if not s:
            break
        fileout.write(s)
