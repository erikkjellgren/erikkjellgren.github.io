import numpy as np
import scipy.linalg
import slowquant.SlowQuant as sq
from scipy.optimize import minimize

X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
I = np.array([[1, 0], [0, 1]])


def krons(A):
    total = np.kron(A[0], A[1])
    for operator in A[2:]:
        total = np.kron(total, operator)
    return total


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


def pauli_string_prouct(A, B):
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
# All terms
terms = []
for i in range(1, 5):
    for j in range(1, 5):
        terms.append([i, j])


for i, j in terms:
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
            op_new.append(pauli_string_prouct(op1, op2))

    for op in op_new:
        if "".join(op.pauli) not in operators_total:
            operators_total["".join(op.pauli)] = op.factor
        else:
            operators_total["".join(op.pauli)] += op.factor
# All terms
terms = []
for i in range(1, 5):
    for j in range(1, 5):
        for k in range(1, 5):
            for l in range(1, 5):
                terms.append([i, j, k, l])

for i, j, k, l in terms:
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
            op_new.append(pauli_string_prouct(op1, op2))
    op_new2 = []
    for op in op_new:
        for op3 in a1:
            op_new2.append(pauli_string_prouct(op, op3))
    op_new3 = []
    for op in op_new2:
        for op4 in a2:
            op_new3.append(pauli_string_prouct(op, op4))

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


def uccsd_anzats_trotter(theta):
    theta_31 = theta[0]
    theta_32 = theta[1]
    theta_41 = theta[2]
    theta_42 = theta[3]
    theta_4321 = theta[4]
    theta_4312 = theta[5]
    theta_3421 = theta[6]
    theta_3412 = theta[7]

    expT = scipy.linalg.expm(theta_31 * (0.5j) * krons([Y, I, X, I]))
    expT = np.matmul(expT, scipy.linalg.expm(theta_31 * (-0.5j) * krons([X, I, Y, I])))
    expT = np.matmul(expT, scipy.linalg.expm(theta_32 * (0.5j) * krons([I, Y, X, I])))
    expT = np.matmul(expT, scipy.linalg.expm(theta_32 * (-0.5j) * krons([I, X, Y, I])))
    expT = np.matmul(expT, scipy.linalg.expm(theta_41 * (0.5j) * krons([Y, I, I, X])))
    expT = np.matmul(expT, scipy.linalg.expm(theta_41 * (-0.5j) * krons([X, I, I, Y])))
    expT = np.matmul(expT, scipy.linalg.expm(theta_42 * (0.5j) * krons([I, Y, I, X])))
    expT = np.matmul(expT, scipy.linalg.expm(theta_42 * (-0.5j) * krons([I, X, I, Y])))
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4321 * (0.03125j) * krons([X, Y, X, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4321 * (-0.03125j) * krons([X, X, X, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4321 * (0.03125j) * krons([Y, X, X, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4321 * (0.03125j) * krons([Y, Y, X, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4321 * (-0.03125j) * krons([X, X, Y, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4321 * (-0.03125j) * krons([X, Y, Y, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4321 * (0.03125j) * krons([Y, Y, Y, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4321 * (-0.03125j) * krons([Y, X, Y, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4312 * (0.03125j) * krons([Y, X, X, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4312 * (-0.03125j) * krons([X, X, X, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4312 * (0.03125j) * krons([X, Y, X, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4312 * (0.03125j) * krons([Y, Y, X, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4312 * (-0.03125j) * krons([X, X, Y, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4312 * (-0.03125j) * krons([Y, X, Y, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4312 * (0.03125j) * krons([Y, Y, Y, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_4312 * (-0.03125j) * krons([X, Y, Y, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3421 * (0.03125j) * krons([X, Y, X, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3421 * (-0.03125j) * krons([X, X, Y, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3421 * (0.03125j) * krons([Y, X, X, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3421 * (0.03125j) * krons([Y, Y, Y, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3421 * (-0.03125j) * krons([X, X, X, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3421 * (-0.03125j) * krons([X, Y, Y, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3421 * (0.03125j) * krons([Y, Y, X, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3421 * (-0.03125j) * krons([Y, X, Y, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3412 * (0.03125j) * krons([Y, X, X, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3412 * (-0.03125j) * krons([X, X, Y, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3412 * (0.03125j) * krons([X, Y, X, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3412 * (0.03125j) * krons([Y, Y, Y, X]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3412 * (-0.03125j) * krons([X, X, X, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3412 * (-0.03125j) * krons([Y, X, Y, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3412 * (0.03125j) * krons([Y, Y, X, Y]))
    )
    expT = np.matmul(
        expT, scipy.linalg.expm(theta_3412 * (-0.03125j) * krons([X, Y, Y, Y]))
    )
    return expT


def total_energy(theta):
    E_tot = np.zeros((16, 16)) * 0.0j
    for paulis, factor in pauli_strings.items():
        pauli_string = []
        for pauli in paulis:
            if pauli == "I":
                pauli_string.append(I)
            elif pauli == "X":
                pauli_string.append(X)
            elif pauli == "Y":
                pauli_string.append(Y)
            elif pauli == "Z":
                pauli_string.append(Z)
        UCCSD = uccsd_anzats_trotter(theta)
        UCCSD_dagger = np.conj(uccsd_anzats_trotter(theta)).T
        E = factor * np.matmul(UCCSD_dagger, np.matmul(krons(pauli_string), UCCSD))
        E_tot += E
    print(np.min(np.real(E_tot)))
    return np.min(np.real(E_tot))


res = minimize(total_energy, np.zeros(8), tol=1e-5)
