import numpy as np
import multiprocessing as mp
from typing import List, Tuple

def gf_mul(a, b, poly):
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        carry = a & 0x80
        a <<= 1
        if carry:
            a ^= poly
        a &= 0xFF
        b >>= 1
    return result

def compute_inv_table(poly: int) -> List[int]:
    inv_table = [0] * 256
    for a in range(1, 256):
        t, newt, r, newr = 0, 1, poly, a
        while newr != 0:
            quotient = r // newr
            t, newt = newt, t ^ gf_mul(quotient, newt, poly)
            r, newr = newr, r ^ gf_mul(quotient, newr, poly)
        inv_table[a] = t
    return inv_table

def affine_transform(byte, c=0x63):
    result = 0
    for i in range(8):
        bit = (byte >> i) & 1
        total = bit ^ ((byte >> ((i + 4) % 8)) & 1) ^ ((byte >> ((i + 5) % 8)) & 1) ^ \
                ((byte >> ((i + 6) % 8)) & 1) ^ ((byte >> ((i + 7) % 8)) & 1) ^ ((c >> i) & 1)
        result |= (total << i)
    return result

def generate_sbox(poly: int, M: int, c: int, inv_table: List[int]) -> List[int]:
    return [affine_transform(gf_mul(inv_table[x], M, poly), c) if x != 0 else affine_transform(0, c) for x in range(256)]

def get_ddt(sbox: List[int]) -> int:
    ddt = np.zeros((256, 256), dtype=int)
    for x in range(256):
        for dx in range(256):
            dy = sbox[x] ^ sbox[x ^ dx]
            ddt[dx][dy] += 1
    return np.max(ddt[1:])

def get_lat(sbox: List[int]) -> int:
    lat = np.zeros((256, 256), dtype=int)
    for a in range(256):
        for b in range(256):
            lat[a, b] = sum((-1) ** (bin(a & x).count("1") ^ bin(b & sbox[x]).count("1")) for x in range(256))
    lat[0][0] = 0
    return np.max(np.abs(lat))

def evaluate_sbox(sbox: List[int]) -> Tuple[int, int]:
    return get_ddt(sbox), get_lat(sbox)

def process_params(args):
    poly, M, c, inv_table = args
    sbox = generate_sbox(poly, M, c, inv_table)
    du, lu = evaluate_sbox(sbox)
    return (du, lu), sbox, (poly, M, c)

def run_parallel_search():
    polyList = [
        0x11b, 0x11d, 0x12b, 0x12d, 0x139, 0x13f, 0x14d, 0x15f, 0x163, 0x165,
        0x169, 0x171, 0x177, 0x17b, 0x187, 0x18b, 0x18d, 0x19f, 0x1a3, 0x1a9,
        0x1b1, 0x1bd, 0x1c3, 0x1cf, 0x1d7, 0x1dd, 0x1e7, 0x1f3, 0x1f5, 0x1f9
    ]

    M_vals = list(range(1, 2))
    c_vals = list(range(1, 2))

    args_list = []
    inv_tables = {poly: compute_inv_table(poly) for poly in polyList}

    for poly in polyList[:1]:
        inv_table = inv_tables[poly]
        for M in M_vals:
            for c in c_vals:
                args_list.append((poly, M, c, inv_table))

    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.map(process_params, args_list)

    best = min(results, key=lambda x: x[0])
    return best

best_score, best_sbox, best_params = run_parallel_search()
best_score, best_params, best_sbox[:16]  # show sample output
