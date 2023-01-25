import numpy as np


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
determinants = [[1, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 0], [0, 0, 1, 1]]
for bra in determinants:
    for ket in determinants:
        print(
            f"<{''.join(str(x) for x in bra)}|H|{''.join(str(x) for x in ket)}> = ",
            end="",
        )

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
                print(f" {pm[sign]} h_{idx1}{idx2}", end="")

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
                print(f" {pm[sign]} 1/2 g_{idx1}{idx2}{idx3}{idx4}", end="")

        print("")
