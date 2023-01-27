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


terms = [
    [1, 2, 2, 1],
    [2, 1, 1, 2],
    [3, 4, 4, 3],
    [4, 3, 3, 4],
    [1, 2, 4, 3],
    [2, 1, 3, 4],
    [3, 4, 2, 1],
    [4, 3, 1, 2],
]
operators_total = {}
for i, j, k, l in terms:
    # Ordered as c1,c2,a1,a2
    a1 = []
    for operator in construct_operator(k):
        a1.append(operator)
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

    operators_unique = {}
    for op in op_new3:
        if "".join(op.pauli) not in operators_unique:
            operators_unique["".join(op.pauli)] = op.factor
        else:
            operators_unique["".join(op.pauli)] += op.factor

    print(f"c{i} c{j} a{k} a{l} =", operators_unique)
