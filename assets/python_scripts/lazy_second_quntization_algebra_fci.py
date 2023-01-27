import numpy as np
import slowquant.SlowQuant as sq


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
h_int = Transform1eSPIN(hcore_mo)

ERI = A.integral.electron_repulsion_tensor
ERI_mo = np.einsum(
    "ai,bj,ck,dl,abcd->ijkl",
    A.hartree_fock.mo_coeff,
    A.hartree_fock.mo_coeff,
    A.hartree_fock.mo_coeff,
    A.hartree_fock.mo_coeff,
    ERI,
)
g_int = Transform2eSPIN(ERI_mo)


class a:
    def __init__(self, idx):
        self.idx = idx
        self.dagger = False


class c:
    def __init__(self, idx):
        self.idx = idx
        self.dagger = True


def apply_operators(operators):
    state = [0, 0, 0, 0]
    sign = 1
    # [::-1] to get the right most operator first,
    # such that it works as we expect when applying to the ket.
    for operator in operators[::-1]:
        if operator.dagger:
            if state[operator.idx - 1] == 1:
                return 0
            if np.sum(state[: operator.idx - 1]) % 2 != 0:
                sign *= -1
            state[operator.idx - 1] = 1
        else:
            if state[operator.idx - 1] == 0:
                return 0
            if np.sum(state[: operator.idx - 1]) % 2 != 0:
                sign *= -1
            state[operator.idx - 1] = 0
    return sign


pm = {1: "+", -1: "-"}
H_ci = np.zeros((4, 4))
determinants = [[1, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 0], [0, 0, 1, 1]]
for bra_i, bra in enumerate(determinants):
    for ket_j, ket in enumerate(determinants):
        bra_occ = []
        for i, occ in enumerate(bra):
            if occ == 1:
                bra_occ.append(i + 1)
        ket_occ = []
        for i, occ in enumerate(ket):
            if occ == 1:
                ket_occ.append(i + 1)

        operator_pool = []
        for p in range(4):
            for q in range(4):
                operator_pool.append(
                    [
                        a(bra_occ[1]),
                        a(bra_occ[0]),
                        c(p + 1),
                        a(q + 1),
                        c(ket_occ[0]),
                        c(ket_occ[1]),
                    ]
                )

        for operators in operator_pool:
            sign = apply_operators(operators)
            if sign != 0:
                idx1, idx2 = operators[2].idx, operators[3].idx
                H_ci[bra_i, ket_j] += sign * h_int[idx1 - 1, idx2 - 1]

        operator_pool = []
        for p in range(4):
            for q in range(4):
                for r in range(4):
                    for s in range(4):
                        operator_pool.append(
                            [
                                a(bra_occ[1]),
                                a(bra_occ[0]),
                                c(p + 1),
                                c(q + 1),
                                a(s + 1),
                                a(r + 1),
                                c(ket_occ[0]),
                                c(ket_occ[1]),
                            ]
                        )

        for operators in operator_pool:
            sign = apply_operators(operators)
            if sign != 0:
                # Index swifting 4->3, 3->4 because of how the molecular Hamiltonian is defined.
                idx1, idx2, idx4, idx3 = (
                    operators[2].idx,
                    operators[3].idx,
                    operators[4].idx,
                    operators[5].idx,
                )
                H_ci[bra_i, ket_j] += (
                    sign * 0.5 * g_int[idx1 - 1, idx2 - 1, idx3 - 1, idx4 - 1]
                )

with np.printoptions(precision=3, suppress=True):
    print(H_ci)

energy, _ = np.linalg.eigh(H_ci)
print(f"Full CI electronic energy={energy[0]}")
