# AES-128 Implementation with Dynamic Affine S-Box
# Author: Gaurav Pratap

import os 

# Rijndael irreducible polynomial for GF(2^8): x^8 + x^4 + x^3 + x + 1 = 0x11B
AES_MOD = 0x11B

# Affine transformation matrix for S-box
AFFINE_MATRIX = [
    0xF1,  # 11110001
    0xE3,  # 11100011
    0xC7,  # 11000111
    0x8F,  # 10001111
    0x1F,  # 00011111
    0x3E,  # 00111110
    0x7C,  # 01111100
    0xF8   # 11111000
]

# Round constants for key expansion
RCON = [0x01]
for i in range(1, 10):
    RCON.append((RCON[-1] << 1) ^ (0x11B if RCON[-1] & 0x80 else 0x00))

def xtime(a):
    return ((a << 1) ^ AES_MOD) if (a & 0x80) else (a << 1)

def gf_mul(a, b):
    """Galois field multiplication in GF(2^8)"""
    res = 0
    for i in range(8):
        if b & 1:
            res ^= a
        a = xtime(a)
        b >>= 1
    return res & 0xFF

def gf_inv(a):
    """Multiplicative inverse in GF(2^8)"""
    if a == 0:
        return 0
    for i in range(1, 256):
        if gf_mul(a, i) == 1:
            return i
    return 0

def affine_transform(byte):
    """Apply AES affine transformation to a byte"""
    result = 0
    for i in range(8):
        # Rotate and XOR bits according to AES affine transformation definition
        bit = (
            ((byte >> i) & 1) ^
            ((byte >> ((i + 4) % 8)) & 1) ^
            ((byte >> ((i + 5) % 8)) & 1) ^
            ((byte >> ((i + 6) % 8)) & 1) ^
            ((byte >> ((i + 7) % 8)) & 1) ^ 1
        )
        result |= (bit << i)
    return result

def generate_sbox():
    return [affine_transform(gf_inv(i)) for i in range(256)]

SBOX = generate_sbox()

def sub_bytes(state):
    return [SBOX[b] for b in state]

def shift_rows(state):
    return [
        state[0],  state[5],  state[10], state[15],
        state[4],  state[9],  state[14], state[3],
        state[8],  state[13], state[2],  state[7],
        state[12], state[1],  state[6],  state[11],
    ]

def mix_columns(state):
    def mix_single_column(col):
        return [
            gf_mul(col[0], 2) ^ gf_mul(col[1], 3) ^ col[2] ^ col[3],
            col[0] ^ gf_mul(col[1], 2) ^ gf_mul(col[2], 3) ^ col[3],
            col[0] ^ col[1] ^ gf_mul(col[2], 2) ^ gf_mul(col[3], 3),
            gf_mul(col[0], 3) ^ col[1] ^ col[2] ^ gf_mul(col[3], 2),
        ]
    new_state = []
    for i in range(4):
        col = [state[i + 4 * j] for j in range(4)]
        mixed = mix_single_column(col)
        for j in range(4):
            new_state.append(mixed[j])
    return new_state

def add_round_key(state, round_key):
    return [b ^ k for b, k in zip(state, round_key)]

def key_expansion(key):
    key_symbols = list(key)
    if len(key_symbols) != 16:
        raise ValueError("Key must be 16 bytes.")
    key_schedule = key_symbols[:]
    for i in range(4, 4 * (10 + 1)):
        temp = key_schedule[(i - 1)*4:i*4]
        if i % 4 == 0:
            temp = temp[1:] + temp[:1]  # RotWord
            temp = [SBOX[b] for b in temp]  # SubWord
            temp[0] ^= RCON[i//4 - 1]
        for j in range(4):
            temp[j] ^= key_schedule[(i - 4)*4 + j]
        key_schedule += temp
    return [key_schedule[16*i:16*(i+1)] for i in range(11)]

def pad_pkcs7(data):
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)

def unpad_pkcs7(data):
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError("Invalid padding")
    return data[:-pad_len]

def aes_encrypt(plaintext, key):
    if len(plaintext) != 16:
        raise ValueError("Plaintext must be 16 bytes.")
    round_keys = key_expansion(key)
    state = list(plaintext)
    state = add_round_key(state, round_keys[0])
    for round in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[round])
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[10])
    return state

def encrypt_ecb(plaintext_bytes, key_bytes):
    if len(key_bytes) != 16:
        raise ValueError("Key must be 16 bytes.")
    padded = pad_pkcs7(plaintext_bytes)
    blocks = [padded[i:i+16] for i in range(0, len(padded), 16)]
    cipher_blocks = []
    for block in blocks:
        ct = aes_encrypt(list(block), list(key_bytes))
        cipher_blocks.extend(ct)
    return bytes(cipher_blocks) 

if __name__ == "__main__":
    import binascii

    # Example usage
    key = b'YELLOW SUBMARINE'
    plaintext = "AES encryption from scratch with affine S-box is awesome!"

    ciphertext = encrypt_ecb(plaintext.encode('utf-8'), key)
    print("Ciphertext (hex):", ciphertext.hex())
    
    # Decrypting is not implemented in this snippet, but you can implement it similarly.