from pyquil.quil import Program, DefGate
import numpy as np
from pyquil.quilatom import QubitPlaceholder
from pyquil.gates import H
from pyquil.parameters import Parameter, quil_exp


def def_CUj():
    a = Parameter('a') # a is naturally in the form of e^(ia) as it comes from the B matrix
    b = Parameter('b')
    c = Parameter('c')
    d = Parameter('d')
    cu = np.eye(8)
    cu[4, 4] = a
    cu[5, 5] = b
    cu[6, 6] = c
    cu[7, 7] = d
    gate_def = DefGate('CUJ', cu, [a, b, c, d])
    return gate_def.get_constructor()

# Constructs U, the tensor product of each U_j in the j controlled unitaries
def construct_U(placeholders, CUj, unitaries):
    pq = Program()

    # control qubit is the first one in placeholders:
    control = placeholders[0]

    for i in range(len(unitaries)):
        curr = unitaries[i]
        # Current a, b, c, d values are the diagonal of the current unitary
        diag = np.diagonal(curr)
        first = placeholders[1 + 2*i]
        second = [2 + 2*i]
        pq += CUj(curr)(control, first, second)
    return pq

# Constructs U^n for some n representing the number of qubits used in phase estimation
def construct_U_to_power(placeholders, CUj, unitaries, power):
    pq = Program()
    if(power < 0):
        raise Exception('Cannot raise U to negative power.')

    pq = construct_U(placeholders, CUj, unitaries)
    for i in range(1, power):
        pq += pq
    return pq

def def_controlled_rk():
    k = Parameter('k')
    crk = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, quil_exp((-2*np.pi*1j)/2**k)]
    ])
    gate_definition = DefGate('CRK', crk, [k])
    return gate_definition.get_constructor()

# Length of placeholders is the number of qubits we are approximating (should be 6)
def inverse_qft(placeholders, CRK):
    n = len(placeholders)
    pq = Program()
    for i in range(n):
        pq += H(placeholders[i])
        for j in range(2, n - i + 1):
            pq += CRK(j)(placeholders[i+j-1], placeholders[i])
    return pq

# CRK = def_controlled_rk()
# pq = inverse_qft(6, CRK)
# print(pq)

#
# Previous attempt at defining U gates, drawing directly from IBM QASM u1 native gate definitions
#
# def controlled_UJ(u_j, CU1, U1, CCX): # Pass in gate declarations
#     [a, b, c, d] = np.flatten(u_j)
#     q1 = QubitPlaceholder()
#     q2 = QubitPlaceholder()
#     q3 = QubitPlaceholder()
#     # Per QASM documentation, u1 := Rz
#     # Define quantum circuit representing controlled_U gate
#     pq = Program()
#     pq += CU1(c/a)(q1, q2)
#     pq += U1(a)(q1)
#     pq += CU1(b/a)(q1, q3)
#     pq += CCX(q1, q2, q3)
#     x = np.sqrt((d*c)/(a*b))
#     pq += U1(x)(q3)
#     pq += CCX(q1, q2, q3)
#     return pq

# def def_cu1():
#     x = Parameter('x')
#     cu1 = np.array([
#         [1, 0, 0, 0],
#         [0, 1, 0, 0],
#         [0, 0, 1, 0],
#         [0, 0, 0, x]
#     ])
#     gate_definition = DefGate('CU1', cu1, [x])
#     return gate_definition.get_constructor()
#
# def def_u1():
#     x = Parameter('x')
#     u1 = np.array([
#         [1, 0],
#         [0, x]
#     ])
#     gate_definition = DefGate('U1', u1, [x])
#     return gate_definition.get_constructor()
#
# def def_ccx():
#     ccx = np.eye(8)
#     ccx[6, 6] = 0
#     ccx[7, 7] = 0
#     ccx[6, 7] = 1
#     ccx[7, 6] = 1
#     gate_definition = DefGate('CCX', ccx)
#     return gate_definition.get_constructor()
