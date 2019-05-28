from pyquil.quil import Program
from pyquil.api import QVMConnection
import numpy as np
from pyquil.quilatom import QubitPlaceholder

def controlled_U(u_j, CU1, U1, CCX): # Pass in gate declarations
    [a, b, c, d] = np.flatten(u_j)
    q1 = QubitPlaceholder()
    q2 = QubitPlaceholder()
    q3 = QubitPlaceholder()
    # Per QASM documentation, u1 := Rz
    # Define quantum circuit representing controlled_U gate
    pq = Program()
    pq += CU1(c/a)(q1, q2)
    pq += U1(a)(q1)
    pq += CU1(b/a)(q1, q3)
    pq += CCX(q1, q2, q3)
    x = np.sqrt((d*c)/(a*b))
    pq += U1(x)(q3)
    pq += CCX(q1, q2, q3)


def def_cu1():
    x = Parameter('x')
    cu1 = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, x]
    ])
    gate_definition = DefGate('CU1', cu1, [x])
    return gate_definition.get_constructor()

def def_u1():
    x = Parameter('x')
    u1 = np.array([
        [1, 0],
        [0, x]
    ])
    gate_definition = DefGate('U1', u1, [x])
    return gate_definition.get_constructor()

def def_ccx():
    ccx = np.eye(8)
    ccx[6, 6] = 0
    ccx[7, 7] = 0
    ccx[6, 7] = 1
    ccx[7, 6] = 1
    gate_definition = DefGate('CCX', ccx)
    return gate_definition.get_constructor()
