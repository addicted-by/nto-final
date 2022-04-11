#!/usr/bin/python3
def decoder(filein, fileout, filelog):
    blocksize=7
    s = filein.read(blocksize)
    H = [[1,0,1],
      [1,1,1],
       [1,1,0],
       [0,1,1],
       [1,0,0],
       [0,1,0],
       [0,0,1]]
    if not s:
        return
    while True:
        
        fileout.write(s)
        s = filein.read(blocksize)
        if not s:
            break
