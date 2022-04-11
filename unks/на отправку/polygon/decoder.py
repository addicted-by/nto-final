#!/usr/bin/python3
from itertools import starmap
from operator import mul


def list_to_bits(l: list) -> int:
    return int(''.join(map(str, l)), 2) << 1

def v_xormultiplicate_m(v: list, m: list) -> list:
    return [sum(starmap(mul, zip(v, col)))%2 for col in zip(*m)]
    
def decoder(filein, fileout, filelog):
    blocksize=8
    s = filein.read(blocksize)
    H = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 0]
    ]
    if not s:
        return
    while True:
        filelog.write('\n---ENCODED---\n'.encode())       
        filelog.write(s)
        coded = [int(c)-48 for c in s]
        syndrome = v_xormultiplicate_m(coded, H)
        si = None
        if syndrome != [0,0,0,0]:
            try:
                si = H.index(s)
            except ValueError:
                si = None
        if si != None:
            coded[si] = int(not coded[si])
        log_string = ''.join(str(c) for c in coded)
        string_to_send = ''.join(str(c) for c in coded[4:])
        filelog.write('\n---FULL-DECODED---\n'.encode())
        filelog.write(log_string.encode())
        filelog.write('\n---DECODED---\n'.encode())
        filelog.write(string_to_send.encode())
        fileout.write(string_to_send.encode())
        s = filein.read(blocksize)
        if not s:
            break