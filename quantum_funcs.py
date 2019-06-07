from pyquil.quil import Program, DefGate
import numpy as np
from pyquil.quilatom import QubitPlaceholder
from pyquil.gates import H, X
from pyquil.parameters import Parameter, quil_exp
from tsp_funcs import pipeline_unitaries

def setup_qpe(qubits):
    pq = Program()
    for qubit in qubits:
        pq += H(qubit)
    return pq

def def_CUj():
    pq = Program()
    a = Parameter('a') # a is naturally in the form of e^(ia) as it comes from the B matrix
    b = Parameter('b')
    c = Parameter('c')
    d = Parameter('d')
    cu = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, a, 0, 0, 0],
        [0, 0, 0, 0, 0, b, 0, 0],
        [0, 0, 0, 0, 0, 0, c, 0],
        [0, 0, 0, 0, 0, 0, 0, d]
    ])
    cuj =  DefGate('CUJ', cu, [a, b, c, d])
    constructor = cuj.get_constructor()
    pq += cuj
    return pq, constructor
# Constructs U, the tensor product of each U_j in the j controlled unitaries
def construct_U(placeholders, CUj, unitaries):
    pq = Program()

    # control qubit is the first one in placeholders:
    control = placeholders[0]
    for i in range(len(unitaries)):
        curr = unitaries[i]
        # Current a, b, c, d values are the diagonal of the current unitary
        first = placeholders[1 + 2*i]
        second = placeholders[2 + 2*i]
        [a, b, c, d] = np.diagonal(curr)
        pq += CUj(a, b, c, d)(control, first, second)
    return pq

# Constructs U^n for some n representing the number of qubits used in phase estimation
def construct_U_to_power(placeholders, CUj, unitaries, power):
    pq = Program()
    if(power < 0):
        raise Exception('Cannot raise U to negative power.')

    for i in range(power):
        pq += construct_U(placeholders, CUj, unitaries)
    return pq

def def_controlled_rk():
    pq = Program()
    k = Parameter('k')
    crk = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, quil_exp((2*np.pi*1j)/2**k)]
    ])
    crk =  DefGate('CRK', crk, [k])
    constructor = crk.get_constructor()
    pq += crk
    return pq, constructor

# Length of placeholders is the number of qubits we are approximating (should be 6)
def inverse_qft(placeholders, CRK):
    n = len(placeholders)
    pq = Program()
    for i in range(n):
        pq += H(placeholders[i])
        for j in range(2, n - i + 1):
            pq += CRK(j)(placeholders[i+j-1], placeholders[i])
    return pq

# Eigenstate inputted as a binary string
def setup_eigenstate(placeholders, state):
    pq = Program()
    for i, char in enumerate(state):
        if char == '1':
            pq += X(placeholders[i])
    return pq

# qbs=[]
# for i in range(6):
#     qbs.append(QubitPlaceholder())
# print(qbs)
# eigenstate = '100101'
# pq = setup_eigenstate(qbs, eigenstate)
# print(pq)
#
# pq, CRK = def_controlled_rk()
# placeholders = [QubitPlaceholder() for i in range(6)]
# pq = inverse_qft(placeholders, CRK)
# print(pq)
