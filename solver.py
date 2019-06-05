from quantum_funcs import *
from tsp_funcs import *
from pyquil.quil import Program, address_qubits
from pyquil.api import QVMConnection
import numpy as np
from pyquil.quilatom import QubitPlaceholder
from pyquil.gates import H, MEASURE

qvm = QVMConnection()

n_eigen_qbs = 8
n_qft_qbs = 6

def construct_full_solver(filename, eigenstate):
    units=pipeline_unitaries(filename)

    # Declare placeholders
    eigen_qbs = [QubitPlaceholder() for i in range(n_eigen_qbs)] # Confirm
    qft_qbs = [QubitPlaceholder() for i in range(n_qft_qbs)]

    # Sum up program
    pq = Program()
    ro = pq.declare('ro', 'BIT', n_qft_qbs)

    # Define necessary gates
    declaration, CUJ = def_CUj()
    declaration, CRK = def_controlled_rk()

    pq += setup_eigenstate(eigen_qbs, eigenstate)
    pq += setup_qpe(qft_qbs)

    # TODO: formalize math on eigenstates
    for i, qb in enumerate(reversed(qft_qbs)):
        pq += construct_U_to_power([qb] + eigen_qbs, CUJ, units, 2**i)

    # Add QFT
    pq += inverse_qft(qft_qbs, CRK)
    for i in range(n_qft_qbs):
        pq += MEASURE(qft_qbs[i], ro[i])

    return pq

def run_solver(pq):
    gates = Program()
    # Define necessary gates
    declaration, CUJ = def_CUj()
    gates += declaration
    declaration, CRK = def_controlled_rk()
    gates += declaration

    pq = gates + address_qubits(pq)
    # print(pq)
    res = qvm.run(pq)
    #
    exp_res = ''.join([str(i) for i in res[0]])
    return exp_res


def main():
  print("Running QuantumTSP Solver: \n")
  pq = construct_full_solver('./data/graph_0.txt', '10001000')
  res = run_solver(pq)
  print(res)

if __name__== "__main__":
  main()
