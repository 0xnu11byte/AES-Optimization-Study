# Import libraries
import numpy as np
import array
# np.set_printoptions(threshold=np.inf)

def load_sbox_bin(filename):
    with open(filename, "rb") as f:
        data = array.array('B')
        data.fromfile(f, 256)
        assert len(data) == 256, "S-Box must be 256 bytes"
        return list(data)

SBOX = load_sbox_bin("sbox.bin")

# Inverse S-box
SBOX_INV = [0] * 256
for i in range(256):
    SBOX_INV[SBOX[i]] = i

# ----------- DIFFERENCE DISTRIBUTION TABLE (DDT) -----------
def compute_ddt(sbox):
    ddt = np.zeros((256, 256), dtype=int)
    for dx in range(256):
        for x in range(256):
            x2 = x ^ dx
            dy = sbox[x] ^ sbox[x2]
            ddt[dx][dy] += 1
    return ddt

# ----------- LINEAR APPROXIMATION TABLE (LAT) --------------
def parity(n):
    return bin(n).count("1") % 2

def compute_lat(sbox):
    lat = np.zeros((256, 256), dtype=int)
    for a in range(256):
        for b in range(256):
            count = 0
            for x in range(256):
                if parity(a & x) == parity(b & sbox[x]):
                    count += 1
            lat[a][b] = count - 128  # bias: center around 0
    return lat

# ----------- BOOMERANG CONNECTIVITY TABLE (BCT) ------------
def compute_bct(sbox, sbox_inv):
    bct = np.zeros((256, 256), dtype=int)
    for alpha in range(256):
        for beta in range(256):
            count = 0
            for x in range(256):
                y1 = sbox[x]
                y2 = sbox[x ^ alpha]
                x1_prime = sbox_inv[y1 ^ beta]
                x2_prime = sbox_inv[y2 ^ beta]
                if x1_prime ^ x2_prime == alpha:
                    count += 1
            bct[alpha][beta] = count
    return bct

# -------------------- MAIN SCRIPT --------------------
ddt = compute_ddt(SBOX)
lat = compute_lat(SBOX)
bct = compute_bct(SBOX, SBOX_INV)

# Print security parameters
print("Differential Uniformity (max of DDT, excluding first row):", np.max(ddt[1:]))
print("Linear Uniformity (max absolute LAT, excluding (0,0)):", np.max(np.abs(lat[1:, 1:])))
print("Boomerang Uniformity (max of BCT, excluding row 0 & col 0):", np.max(bct[1:, 1:]))

# Optional: print full tables
# print("DDT:\n", ddt)
# print("LAT:\n", lat)
# print("BCT:\n", bct)
