from itertools import starmap
from operator import mul


def list_to_bits(l: list) -> int:
    return int(''.join(map(str, l)), 2) << 1

def v_xormultiplicate_m(v: list, m: list) -> list:
    return [sum(starmap(mul, zip(v, col)))%2 for col in zip(*m)]


def encoder(filein,fileout):
    blocksize=4

    G = [
    [0, 1, 1, 1, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 1, 0, 0],
    [1, 1, 0, 1, 0, 0, 1, 0],
    [1, 1, 1, 0, 0, 0, 0, 1]
    ]
#порождающая матрица
    while True:
        s=filein.read(blocksize)
        k = [i-48 for i in s]
        coded = v_xormultiplicate_m(k, G)
        if not s:
            break
        string_to_send = ''.join(str(c) for c in coded)
        fileout.write(string_to_send.encode())
    fileout.close()
