from quantum_funcs import *
from tsp_funcs import *
from pyquil.quil import Program, address_qubits
from pyquil.api import QVMConnection, get_qc, QVMCompiler
import numpy as np
from pyquil.quilatom import QubitPlaceholder
from pyquil.gates import H, MEASURE, RZ
# from pyquil.noise import add_decoherence_noise
import networkx as nx
import matplotlib.pyplot as plt
import time
import sys

qvm = QVMConnection()
qc = get_qc("16q-qvm")
compiler = QVMCompiler('tcp://localhost:5555', qc.device, timeout=60)

n_eigen_qbs = 8
n_qft_qbs = 6
n_trials=1

EIGENSTATES = [
    '1230',
    '1203',
    '1302',
    '1320',
    '1023',
    '1032'
]

help_msg = '\nUsage instructions for the Quantum TSP solver: \n' \
            '-------------------------------------------------------\n'\
            '-Call \'python solver.py\' to execute the solver on the sample graph from displayed in the paper.\n'\
            '-Use the following flags to change program behavior.\n'\
            '       - \'--print_quil\' to display the aggregated quil program in the console.\n'\
            '       - \'--fully_quantum\' to run a fully quantum version of the algorithm, which requires more classical memory but less qvm calls.\n'\
            '       - \'--graph=[filename]\' to run the solver on a specified file formatted as a networkx weighted edgelist.\n'\


def construct_full_solver(filename, eigenstate, eigen_qbs, qft_qbs, ro, iter_num=None):
    units=pipeline_unitaries(filename)

    # Sum up program
    pq = Program()

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

    # For determining where to measure qbs depending on iterated or fully quantum implementation
    for i in range(n_qft_qbs):
        if(iter_num):
            pq += MEASURE(qft_qbs[i], ro[iter_num*n_qft_qbs + i])
        else:
            pq += MEASURE(qft_qbs[i], ro[i])

    return pq

def run_solver_quantum(path, eigenstates, to_print):
    gates = Program()
    declaration, CUJ = def_CUj()
    gates += declaration
    declaration, CRK = def_controlled_rk()
    gates += declaration

    pq = Program()

    # Declare placeholders
    eigen_qbs = [QubitPlaceholder() for i in range(n_eigen_qbs)] # Confirm
    qft_qbs = [QubitPlaceholder() for i in range(n_qft_qbs)]

    ro = pq.declare('ro', 'BIT', n_qft_qbs*len(EIGENSTATES))
    for i, e in enumerate(eigenstates):
        pq += construct_full_solver(path, e, eigen_qbs, qft_qbs, ro, iter_num = i)
        pq.reset()
    pq = gates + address_qubits(pq)

    if to_print:
        print('Printing QUIL code for sample eigenstate:')
        print('-------------------------')
        print(pq)

    res = qvm.run(pq, trials=n_trials)
    res = np.array_split(res[0], len(EIGENSTATES))

    output = {}
    for i, elem in enumerate(res):
        output[gen_eigenstate(EIGENSTATES[i])] = ''.join([str(c) for c in elem])
    return output

def run_solver(path, eigenstate, to_print, noise=False):
    # Declare placeholders
    eigen_qbs = [QubitPlaceholder() for i in range(n_eigen_qbs)] # Confirm
    qft_qbs = [QubitPlaceholder() for i in range(n_qft_qbs)]

    pq = Program()
    ro = pq.declare('ro', 'BIT', n_qft_qbs)
    pq += construct_full_solver(path, eigenstate, eigen_qbs, qft_qbs, ro)
    gates = Program()
    # Define necessary gates
    declaration, CUJ = def_CUj()
    gates += declaration
    declaration, CRK = def_controlled_rk()
    gates += declaration

    pq = gates + address_qubits(pq)

    if to_print:
        print('Printing QUIL code for sample eigenstate:')
        print('-------------------------')
        print(pq)

    # ep = None
    if noise:
        print('Unable to add noise due to timeout in compilation.')
        # to_compile = Program() + RZ(np.pi, 0)
        # print(to_compile)
        # print('Compiling program into natural gate set.')
        # ep = qc.compile(pq)
        # print('Finished compiling.')
        # print(ep.program)
        # pq = add_decoherence_noise(pq)
        # res = compiler.quil_to_native_quil(to_compile)
        # print(res)
    # pq = pq if (ep == None) else ep.program
    res = qvm.run(pq, trials=n_trials)
    outputs = []
    for output in res:
        exp_res = ''.join([str(i) for i in output])
        outputs.append(exp_res)
    # print(res)

    return most_common(outputs)

def most_common(arr):
    return max(set(arr), key=arr.count)

# Converts eigenstates to binary representation (for setting up qubits)
def gen_eigenstates():
    states = []
    for e in EIGENSTATES:
        bin_str = gen_eigenstate(e)
        states.append(bin_str)
    return states

def gen_eigenstate(e):
    bin_str = ''
    for num in e:
        bin_str += bin(int(num))[2:].zfill(2)
    return bin_str

def run_solver_for_all_eigenstates(path, fq = False, to_print=False):
    res = {}
    eigens = gen_eigenstates()
    if fq:
        res = run_solver_quantum(path, eigens, to_print)
    else:
        for e in eigens:
            print("Solving for " + e)
            res[e] = run_solver(path, e, to_print, noise=False)
            to_print = False
    print("Done!")
    return res

def eigen_to_node_name(bit_str):
    output = ''
    for i in range(0, len(bit_str), 2):
        curr = bit_str[i: i+2]
        output += str(int(curr, 2))
    return output

def construct_soln_table(in_map):
    keys = in_map.keys()
    tups = [(key, in_map[key]) for key in keys]
    sorted_arr = sorted(tups, key=lambda tup: int(tup[1], 2))
    winner = sorted_arr[0][0]
    print('')
    print('Eigenstate | Ordering | Result | Result as int')
    for item in sorted_arr:
        print('%s   | %s     | %s | %d' % (item[0], eigen_to_node_name(item[0]), item[1], int(item[1], 2)))
    print('')
    return winner

def highlight_best_route(route, file):
    path = eigen_to_node_name(route)
    G = nx.read_weighted_edgelist(file)
    pos = nx.spring_layout(G)
    nx.draw(G, pos=pos)
    nx.draw_networkx_edge_labels(G, pos=pos, with_labels=True)
    edgelist = [(path[i], path[(i+1) % 4]) for i in range(len(path))]
    nx.draw_networkx_edges(G, pos=pos, edgelist = edgelist, width=8, edge_color='r')
    plt.show()

def get_args():
    n_args = len(sys.argv) - 1
    if (sys.argv[1] == '--help' and n_args == 1):
        print(help_msg)
        return False

    args = set(sys.argv[1:])
    path = 'data/graph_from_paper.txt'
    fq = True if '--fully_quantum' in args else False
    to_print = True if '--print_quil' in args else False
    for s in args:
        if '--graph=' in s:
            path = s.replace('--graph=', '')
    return path, fq, to_print

def main():
  args = get_args()
  if not args:
      return
  path, fq, to_print = args
  start = time.time()
  print("Running QuantumTSP Solver: \n")
  res = run_solver_for_all_eigenstates(path, fq=fq, to_print=to_print)
  length = time.time() - start
  winner = construct_soln_table(res)
  print("Time (s): %f" % length)
  highlight_best_route(winner, path)

if __name__== "__main__":
  main()
