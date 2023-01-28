import numpy as np

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


thetas = {}
terms = []
for a1 in range(3, 5):
    for i1 in range(1, 3):
        terms.append([a1, i1])

for a1, i1 in terms:
    # Ordered as c1, a1
    a1_op = []
    a1_op_adj = []
    # Only apply external factors to one term here, a1
    for operator in construct_operator(i1):
        a1_op.append(operator)
    for operator in construct_operator(i1, True):
        a1_op_adj.append(operator)
        a1_op_adj[-1].factor *= -1

    c1_op = []
    c1_op_adj = []
    for operator in construct_operator(a1, True):
        c1_op.append(operator)
    for operator in construct_operator(a1):
        c1_op_adj.append(operator)

    op_new = []
    for op1 in c1_op:
        for op2 in a1_op:
            op_new.append(pauli_string_product(op1, op2))
    for op1 in c1_op_adj:
        for op2 in a1_op_adj:
            op_new.append(pauli_string_product(op1, op2))

    for op in op_new:
        if f"theta_{a1}{i1}" not in thetas:
            thetas[f"theta_{a1}{i1}"] = {"".join(op.pauli): op.factor}
        else:
            if "".join(op.pauli) not in thetas[f"theta_{a1}{i1}"]:
                thetas[f"theta_{a1}{i1}"]["".join(op.pauli)] = op.factor
            else:
                thetas[f"theta_{a1}{i1}"]["".join(op.pauli)] += op.factor
terms = []
for a2 in range(3, 5):
    for i2 in range(1, 3):
        for a1 in range(3, 5):
            for i1 in range(1, 3):
                terms.append([a2, i2, a1, i1])


for a2, i2, a1, i1 in terms:
    # Ordered as c2,a2,c1,a1
    a1_op = []
    a1_op_adj = []
    # Only apply external factors to one term here, a1
    for operator in construct_operator(i1):
        a1_op.append(operator)
        a1_op[-1].factor *= 1 / 4
    for operator in construct_operator(i1, True):
        a1_op_adj.append(operator)
        a1_op_adj[-1].factor *= -1 / 4
    a2_op = []
    a2_op_adj = []
    for operator in construct_operator(i2):
        a2_op.append(operator)
    for operator in construct_operator(i2, True):
        a2_op_adj.append(operator)

    c1_op = []
    c1_op_adj = []
    for operator in construct_operator(a1, True):
        c1_op.append(operator)
    for operator in construct_operator(a1):
        c1_op_adj.append(operator)
    c2_op = []
    c2_op_adj = []
    for operator in construct_operator(a2, True):
        c2_op.append(operator)
    for operator in construct_operator(a2):
        c2_op_adj.append(operator)

    op_new = []
    for op1 in c2_op:
        for op2 in a2_op:
            op_new.append(pauli_string_product(op1, op2))
    op_new2 = []
    for op in op_new:
        for op3 in c1_op:
            op_new2.append(pauli_string_product(op, op3))
    op_new3 = []
    for op in op_new2:
        for op4 in a1_op:
            op_new3.append(pauli_string_product(op, op4))
    op_new = []
    for op1 in c2_op_adj:
        for op2 in a2_op_adj:
            op_new.append(pauli_string_product(op1, op2))
    op_new2 = []
    for op in op_new:
        for op3 in c1_op_adj:
            op_new2.append(pauli_string_product(op, op3))
    for op in op_new2:
        for op4 in a1_op_adj:
            op_new3.append(pauli_string_product(op, op4))

    for op in op_new3:
        if f"theta_{a1}{a2}{i1}{i2}" not in thetas:
            thetas[f"theta_{a1}{a2}{i1}{i2}"] = {"".join(op.pauli): op.factor}
        else:
            if "".join(op.pauli) not in thetas[f"theta_{a1}{a2}{i1}{i2}"]:
                thetas[f"theta_{a1}{a2}{i1}{i2}"]["".join(op.pauli)] = op.factor
            else:
                thetas[f"theta_{a1}{a2}{i1}{i2}"]["".join(op.pauli)] += op.factor

# Prune for numerical noise
anzats_strings = {}
for theta, pauli_strings in thetas.items():
    pauli_new = {}
    for pauli_string, factor in pauli_strings.items():
        if np.abs(factor) > 10**-5:
            if np.abs(np.imag(factor)) < 10**-5:
                pauli_new[pauli_string] = np.real(factor)
            else:
                pauli_new[pauli_string] = factor
    if len(pauli_new) != 0:
        anzats_strings[theta] = pauli_new

for theta, pauli_strings in anzats_strings.items():
    print(theta)
print("")

for theta, pauli_strings in anzats_strings.items():
    print(f"T += {theta}*(", end="")
    for pauli_string, factor in pauli_strings.items():
        if np.imag(factor) > 0:
            print(f"+{factor}*", end="")
        else:
            print(f"{factor}*", end="")
        print("krons([", end="")
        for i, pauli in enumerate(pauli_string):
            if i == len(pauli_string) - 1:
                print(f"{pauli}", end="")
            else:
                print(f"{pauli}, ", end="")
        print("])", end="")
    print(")")
