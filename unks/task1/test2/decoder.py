#!/usr/bin/python3
def decoder(filein, fileout, filelog):
    blocksize = 9
    s = filein.read(blocksize)
    if not s:
        return
    while True:
        fileout.write(s)
        s = filein.read(blocksize)
        if not s:
            break
