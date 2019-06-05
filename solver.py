from quantum_funcs.py import *
from tsp_funcs.py import *
from pyquil.quil import Program, address_qubits
from pyquil.api import QVMConnection
import numpy as np
from pyquil.quilatom import QubitPlaceholder
from pyquil.gates import H

qvm = QVMConnection()

# Define necessary gates
CUJ = def_CUj()
CRK = def_controlled_rk()

def construct_program(filename):
    adj = read_in_graph(filename)
    B = construct_B_matrix(adj)
    units = construct_unitaries(B)

    pq = Program()


def main():
  print("Hello World!")

if __name__== "__main__":
  main()
