#!/usr/bin/python3


# from itertools import starmap
# from operator import mul

# def v_xormultiplicate_m(v: list, m: list) -> list:
#     return [sum(starmap(mul, zip(v, col)))%2 for col in zip(*m)]




def encoder(filein,fileout):
    blocksize=4

    G = [[1,0,1,1,0,0,0],
      [0,1,0,1,1,0,0], 
      [0,0,1,0,1,1,0], 
      [0,0,0,1,0,1,1]] 
#порождающая матрица

    while True:
        s=filein.read(blocksize)
        
        if not s:
            break
        fileout.write(s)
