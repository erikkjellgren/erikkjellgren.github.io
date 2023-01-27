import numpy as np
import slowquant.SlowQuant as sq

# Hamiltonian_type can be:
#   HartreeFock
#   CID
#   Full

hamiltonian_type = "CID"

if hamiltonian_type == "Full":
    terms_1e = []
    for i in range(1, 5):
        for j in range(1, 5):
            terms_1e.append([i, j])
    terms_2e = []
    for i in range(1, 5):
        for j in range(1, 5):
            for k in range(1, 5):
                for l in range(1, 5):
                    terms_2e.append([i, j, k, l])
elif hamiltonian_type == "CID":
    terms_1e = [[1, 1], [2, 2], [3, 3], [4, 4]]
    terms_2e = [
        [1, 2, 2, 1],
        [2, 1, 1, 2],
        [3, 4, 4, 3],
        [4, 3, 3, 4],
        [1, 2, 4, 3],
        [2, 1, 3, 4],
        [3, 4, 2, 1],
        [4, 3, 1, 2],
    ]
elif hamiltonian_type == "HartreeFock":
    terms_1e = [[1, 1], [2, 2]]
    terms_2e = [[1, 2, 2, 1], [2, 1, 1, 2]]

relations = {
    "II": [1, "I"],
    "IX": [1, "X"],
    "IY": [1, "Y"],
    "IZ": [1, "Z"],
    "XI": [1, "X"],
    "YI": [1, "Y"],
    "ZI": [1, "Z"],
    "XX": [1, "I"],
    "XY": [1.0j, "Z"],
    "XZ": [-1.0j, "Y"],
    "YX": [-1.0j, "Z"],
    "YY": [1, "I"],
    "YZ": [1.0j, "X"],
    "ZX": [1.0j, "Y"],
    "ZY": [-1.0j, "X"],
    "ZZ": [1, "I"],
}

X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
I = np.array([[1, 0], [0, 1]])


def krons(A):
    """Does the P x P x P ..."""
    total = np.kron(A[0], A[1])
    for operator in A[2:]:
        total = np.kron(total, operator)
    return total


class pauli_operators:
    def __init__(self, factor, pauli):
        self.factor = factor
        self.pauli = pauli


def construct_operator(idx, dagger=False):
    """Transform fermionic operator into pauli operators.

    a = (X + iY)/2

    a^dagger = c = (X - iY)/2
    """
    operator1 = ["I", "I", "I", "I"]
    operator2 = ["I", "I", "I", "I"]
    operator1[idx - 1] = "X"
    operator2[idx - 1] = "Y"
    factor1 = 1 / 2
    factor2 = 1.0j / 2
    if dagger:
        factor2 *= -1
    return pauli_operators(factor1, operator1), pauli_operators(factor2, operator2)


def pauli_string_product(A, B):
    """Product of two pauli strings.

    (A1 x A2 x ... x An)(B1 x B2 x ... x Bn) = (A1 B1)x(A2 B2)x...x(An Bn)
    """
    factor = A.factor * B.factor
    out = []
    for a, b in zip(A.pauli, B.pauli):
        fac, operator = relations[f"{a}{b}"]
        factor *= fac
        out.append(operator)
    return pauli_operators(factor, out)


def Transform1eSPIN(int1e):
    int1e_spin = np.zeros((len(int1e) * 2, len(int1e) * 2))
    for p in range(1, len(int1e) * 2 + 1):
        for q in range(1, len(int1e) * 2 + 1):
            if p % 2 == q % 2:
                int1e_spin[p - 1, q - 1] = int1e[(p + 1) // 2 - 1, (q + 1) // 2 - 1]
    return int1e_spin


def Transform2eSPIN(int2e):
    """Takes two-electron integrals to spin-basis.
    Beware of the index transformation:

    (pr|qs) -> <pq|rs>
    """
    int2e_spin = np.zeros(
        (len(int2e) * 2, len(int2e) * 2, len(int2e) * 2, len(int2e) * 2)
    )
    for p in range(1, len(int2e) * 2 + 1):
        for r in range(1, len(int2e) * 2 + 1):
            if p % 2 == r % 2:
                for q in range(1, len(int2e) * 2 + 1):
                    for s in range(1, len(int2e) * 2 + 1):
                        if q % 2 == s % 2:
                            int2e_spin[p - 1, q - 1, r - 1, s - 1] = int2e[
                                (p + 1) // 2 - 1,
                                (r + 1) // 2 - 1,
                                (q + 1) // 2 - 1,
                                (s + 1) // 2 - 1,
                            ]
    return int2e_spin


A = sq.SlowQuant()
A.set_molecule("""H 0 0 0; H 1.401 0 0""", distance_unit="bohr")
A.set_basis_set("sto-3g")
A.init_hartree_fock()
A.hartree_fock.run_restricted_hartree_fock()

hcore = A.integral.kinetic_energy_matrix + A.integral.nuclear_attraction_matrix
hcore_mo = np.einsum(
    "pi,qj,pq->ij", A.hartree_fock.mo_coeff, A.hartree_fock.mo_coeff, hcore
)
h = Transform1eSPIN(hcore_mo)

ERI = A.integral.electron_repulsion_tensor
ERI_mo = np.einsum(
    "ai,bj,ck,dl,abcd->ijkl",
    A.hartree_fock.mo_coeff,
    A.hartree_fock.mo_coeff,
    A.hartree_fock.mo_coeff,
    A.hartree_fock.mo_coeff,
    ERI,
)
g = Transform2eSPIN(ERI_mo)


operators_total = {}
for i, j in terms_1e:
    # Ordered as c1, a1
    a1 = []
    for operator in construct_operator(j):
        a1.append(operator)
        # Only apply the factor to the first term (other wise it would be factor**2)
        a1[-1].factor *= h[i - 1, j - 1]

    c1 = []
    for operator in construct_operator(i, True):
        c1.append(operator)

    op_new = []
    for op1 in c1:
        for op2 in a1:
            op_new.append(pauli_string_product(op1, op2))

    for op in op_new:
        if "".join(op.pauli) not in operators_total:
            operators_total["".join(op.pauli)] = op.factor
        else:
            operators_total["".join(op.pauli)] += op.factor

for i, j, k, l in terms_2e:
    # Ordered as c1,c2,a1,a2
    a1 = []
    for operator in construct_operator(k):
        a1.append(operator)
        # Only apply the factor to the first term (other wise it would be factor**4)
        a1[-1].factor *= g[i - 1, j - 1, l - 1, k - 1] / 2
    a2 = []
    for operator in construct_operator(l):
        a2.append(operator)

    c1 = []
    for operator in construct_operator(i, True):
        c1.append(operator)
    c2 = []
    for operator in construct_operator(j, True):
        c2.append(operator)

    op_new = []
    for op1 in c1:
        for op2 in c2:
            op_new.append(pauli_string_product(op1, op2))
    op_new2 = []
    for op in op_new:
        for op3 in a1:
            op_new2.append(pauli_string_product(op, op3))
    op_new3 = []
    for op in op_new2:
        for op4 in a2:
            op_new3.append(pauli_string_product(op, op4))

    for op in op_new3:
        if "".join(op.pauli) not in operators_total:
            operators_total["".join(op.pauli)] = op.factor
        else:
            operators_total["".join(op.pauli)] += op.factor

# Prune for numerical noise
pauli_strings = {}
for pauli_string, factor in operators_total.items():
    if np.abs(factor) > 10**-5:
        if np.abs(np.imag(factor)) < 10**-5:
            pauli_strings[pauli_string] = np.real(factor)
        else:
            pauli_strings[pauli_string] = factor

print("\n")
print("### PAULI STRINGS ###")
print(pauli_strings)
print("\n")

H_JW = np.zeros((16, 16))
for pauli_string, factor in pauli_strings.items():
    operator_list = []
    for operator in pauli_string:
        if operator == "I":
            operator_list.append(I)
        elif operator == "X":
            operator_list.append(X)
        elif operator == "Y":
            operator_list.append(Y)
        elif operator == "Z":
            operator_list.append(Z)
    H_JW += factor * np.real(krons(operator_list))

print("### JW HAMILTONIAN ###")
print(H_JW)
print("\n")

print("### Eigenvalue and Eigenvectors ###")
print(np.linalg.eigh(H_JW))
