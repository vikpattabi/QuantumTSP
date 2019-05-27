from pyquil import Program
from pyquil.paulis import PauliSum
from pyquil.api import WavefunctionSimulator
from pyquil.gates import RX, RZ, CNOT
from scipy.optimize import minimize
import numpy as np

qvm = QVMConnection()

def solve_vqe(hamiltonian: PauliSum) -> float:
    # Construct a variational quantum eigensolver solution to find the lowest
    # eigenvalue of the given hamiltonian
    num_layers = 10
    fun = lambda params: sim.expectation(ansatz(params, num_layers), hamiltonian)

    res = minimize(fun, np.random.normal(size=num_layers*10))
    return sim.expectation(ansatz(res.x, num_layers), hamiltonian)

def layer(params):
    pq = Program()
    for i in range(5):
        pq += RX(params[i], i)
        pq += RZ(params[i+5], i)
    for i in range(4):
        pq += CNOT(i, i+1)
    return pq

def ansatz(params, num_layers):
    pq = Program()
    for i in range(num_layers):
        pq += layer(params[10*i:10*i+10])
    ro = pq.declare('ro', 'BIT', 5)
    return pq
