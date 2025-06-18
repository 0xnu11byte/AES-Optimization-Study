import numpy as np
import galois

# Step 1: Define GF(2^8) with irreducible polynomial 0x1F5 (x^8 + x^7 + x^6 + x^5 + x^4 + x^2 + 1)
primitive_poly = galois.Poly.Int(0x1F5)
GF256 = galois.GF(2**8, irreducible_poly=primitive_poly)

# Step 2: Choose triplet values (y, z, w)
y = GF256(0x13)
z = GF256(0x7a)
w = GF256(0x5d)


# Step 3: Construct the basis as per structured powers
basis = [
    (w**2) * (z**4) * (y**16),   # χ0
    (w**1) * (z**4) * (y**16),   # χ1
    (w**2) * (z**1) * (y**16),   # χ2
    (w**1) * (z**1) * (y**16),   # χ3
    (w**2) * (z**4) * (y**1),    # χ4
    (w**1) * (z**4) * (y**1),    # χ5
    (w**2) * (z**1) * (y**1),    # χ6
    (w**1) * (z**1) * (y**1),    # χ7
]

# Step 4: Build Isomorphism Matrix X (Each column = bit representation of χi)
X = np.array([[int(basis[col]) >> row & 1 for col in range(8)] for row in range(7, -1, -1)], dtype=int)

print("\nχ values:")
for i, chi in enumerate(basis):
    print(f"χ{i} = 0x{int(chi):02x}")


# Step 5: Print X matrix and χ values
print("Isomorphism Matrix X:")
print(X)

# Step 6: Inverse of X in GF(2)
try:
    X_inv = np.linalg.inv(X) % 2
    print("\nInverse of X (X⁻¹):")
    print(X_inv.astype(int))
except np.linalg.LinAlgError:
    print("\nMatrix X is not invertible in GF(2)")
