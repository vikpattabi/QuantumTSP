from quantum_funcs import *
from tsp_funcs import *
from pyquil.quil import Program, address_qubits
from pyquil.api import QVMConnection
import numpy as np
from pyquil.quilatom import QubitPlaceholder
from pyquil.gates import H, MEASURE
from pyquil.noise import add_decoherence_noise
import time

qvm = QVMConnection()

n_eigen_qbs = 8
n_qft_qbs = 6
n_trials=10

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

def run_solver(path, eigenstate, noise=False):
    pq = construct_full_solver(path, eigenstate)
    gates = Program()
    # Define necessary gates
    declaration, CUJ = def_CUj()
    gates += declaration
    declaration, CRK = def_controlled_rk()
    gates += declaration

    pq = gates + address_qubits(pq)

    if noise:
        print("Adding built-in decoherence noise not possible due to gate set.")
        # pq = add_decoherence_noise(pq)
    # print(pq)
    res = qvm.run(pq, trials=n_trials)
    outputs = []
    for output in res:
        exp_res = ''.join([str(i) for i in output])
        outputs.append(exp_res)

    return most_common(outputs)

def most_common(arr):
    return max(set(arr), key=arr.count)

def gen_eigenstates(n):
    
    return None

def main():
  print("Running QuantumTSP Solver: \n")
  start = time.time()
  res = run_solver('./data/graph_0.txt', '10001000')
  length = time.time() - start
  print("Time (s): %f" % length)

if __name__== "__main__":
  main()
