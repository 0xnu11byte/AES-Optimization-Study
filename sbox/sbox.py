import array

def gf_mul(a, b):
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        hi_bit = a & 0x80
        a = (a << 1) & 0xFF
        if hi_bit:
            a ^= 0x1B
        b >>= 1
    return result

def gf_inverse(byte):
    """Find multiplicative inverse using brute force (valid for small field like GF(2^8))"""
    if byte == 0:
        return 0
    for i in range(1, 256):
        if gf_mul(byte, i) == 1:
            return i
    return 0

def affine_transform(byte):
    c = 0x63
    result = 0
    for i in range(8):
        bit = (
            ((byte >> i) & 1) ^
            ((byte >> ((i + 4) % 8)) & 1) ^
            ((byte >> ((i + 5) % 8)) & 1) ^
            ((byte >> ((i + 6) % 8)) & 1) ^
            ((byte >> ((i + 7) % 8)) & 1) ^
            ((c >> i) & 1)
        )
        result |= (bit << i)
    return result

def generate_sbox():
    sbox = []
    for i in range(256):
        inv = gf_inverse(i)
        sbox.append(affine_transform(inv))
    return sbox

# Generate and print
sbox = generate_sbox()
for i in range(0, 256, 16):
    print(" ".join(f"{x:02X}" for x in sbox[i:i+16]))

# Save as raw binary
with open("sbox.bin", "wb") as f:
    array.array('B', sbox).tofile(f)  # 'B' is unsigned byte