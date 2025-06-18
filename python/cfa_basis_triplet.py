import numpy as np
import galois
from itertools import product

# Define GF(2^8) with the irreducible polynomial 0x1f5 = x^8 + x^7 + x^6 + x^4 + x^2 + x + 1
primitive_poly = galois.Poly.Int(0x1f5)
GF256 = galois.GF(2**8, irreducible_poly=primitive_poly)

# Function to create isomorphism matrix X from (y, z, w)
def generate_basis_matrix(y, z, w):
    """
    Construct the transformation matrix X ∈ GF(2)^{8x8} 
    using a composite basis with basis elements (1, y, z, yz, w, yw, zw, yzw)
    """
    base_elements = [1, y, z, y*z, w, y*w, z*w, y*z*w]
    matrix = np.array([[int(b >> (7 - i)) & 1 for b in base_elements] for i in range(8)], dtype=int)
    return matrix

# Brute-force all (y, z, w) in GF(2^8)\{0}
nonzero_elements = [e for e in GF256.elements if e != 0]

valid_triplets = []

# Limit to 10 valid results for brevity
max_results = 3
count = 0

for y, z, w in product(nonzero_elements, repeat=3):
    try:
        X = generate_basis_matrix(y, z, w)
        if np.linalg.matrix_rank(X) == 8:
            valid_triplets.append((int(y), int(z), int(w)))
            count += 1
            if count >= max_results:
                break
    except Exception as e:
        continue

# Print a few valid triplets
print(f"Total valid triplets: {len(valid_triplets)}")
for i, (y, z, w) in enumerate(valid_triplets[:10]):
    print(f"{i+1}. y=0x{y:02x}, z=0x{z:02x}, w=0x{w:02x}")
