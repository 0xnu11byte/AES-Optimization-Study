# Prototype script for Algorithm 1: Searching Compact S-Box
# Assumes a smaller search space for demonstration purposes

from typing import List, Tuple

def gf_mul(a, b, poly):
    """Multiply two elements in GF(2^8) with a given primitive polynomial."""
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

def gf_inv(a, poly):
    """Find multiplicative inverse in GF(2^8) using Extended Euclidean Algorithm."""
    if a == 0:
        return 0
    lm, hm = 1, 0
    low, high = a, poly
    while low > 1:
        ratio = high // low
        nm = hm ^ gf_mul(ratio, lm, poly)
        new = high ^ gf_mul(ratio, low, poly)
        hm, lm = lm, nm
        high, low = low, new
    return lm

def affine_transform(byte, c=0x63):
    """Apply AES-like affine transformation."""
    result = 0
    for i in range(8):
        bit = (byte >> i) & 1
        total = bit ^ ((byte >> ((i + 4) % 8)) & 1) ^ ((byte >> ((i + 5) % 8)) & 1) ^ ((byte >> ((i + 6) % 8)) & 1) ^ ((byte >> ((i + 7) % 8)) & 1) ^ ((c >> i) & 1)
        result |= (total << i)
    return result

def generate_sbox(poly: int, M: int, c: int) -> List[int]:
    """Generate a single S-box using given poly, multiplier M and constant c."""
    sbox = []
    for x in range(256):
        inv = gf_inv(x, poly)
        transformed = gf_mul(inv, M, poly)
        sbox.append(affine_transform(transformed, c))
    return sbox

def get_ddt(sbox: List[int]) -> int:
    """Get differential uniformity (max of DDT, excluding 0)."""
    ddt = [[0]*256 for _ in range(256)]
    for x in range(256):
        for dx in range(256):
            dy = sbox[x] ^ sbox[x ^ dx]
            ddt[dx][dy] += 1
    return max(ddt[i][j] for i in range(1, 256) for j in range(256))

def get_lat(sbox: List[int]) -> int:
    """Get linear uniformity (max absolute LAT, excluding (0,0))."""
    lat = [[0]*256 for _ in range(256)]
    for a in range(256):
        for b in range(256):
            total = 0
            for x in range(256):
                total += (-1) ** (bin(a & x).count("1") ^ bin(b & sbox[x]).count("1"))
            lat[a][b] = total
    return max(abs(lat[a][b]) for a in range(256) for b in range(256) if not (a == 0 and b == 0))

def evaluate_sbox(sbox: List[int]) -> Tuple[int, int]:
    """Evaluate S-box based on security properties."""
    return get_ddt(sbox), get_lat(sbox)

# 30 irreducible primitive polynomials in GF(2^8)
polyList = [
    0x11b, 0x11d, 0x12b, 0x12d, 0x139, 0x13f, 0x14d, 0x15f, 0x163, 0x165,
    0x169, 0x171, 0x177, 0x17b, 0x187, 0x18b, 0x18d, 0x19f, 0x1a3, 0x1a9,
    0x1b1, 0x1bd, 0x1c3, 0x1cf, 0x1d7, 0x1dd, 0x1e7, 0x1f3, 0x1f5, 0x1f9
]

# For demo, limit M and c to small range
best_score = (100, 100)  # large initial values
best_sbox = []
best_params = ()

for poly in polyList[:1]:  # Only first 2 polynomials for speed
    for M in range(1, 1):  # Try 7 values
        for c in range(1, 2):
            sbox = generate_sbox(poly, M, c)
            du, lu = evaluate_sbox(sbox)
            if (du, lu) < best_score:
                best_score = (du, lu)
                best_sbox = sbox
                best_params = (poly, M, c)

(best_score, best_params, best_sbox[:16])  # Show sample of results

# Output the best found S-box and its parameters
print("Best S-box parameters (poly, M, c):", best_params)
print("Best S-box (first 16 bytes):", best_sbox[:16])
print("Best score (DDT, LAT):", best_score)