import numpy as np
import networkx as nx

def read_in_graph(path):
    G = nx.read_weighted_edgelist(path)
    return nx.to_numpy_matrix(G)

def construct_B_matrix(adj_matrix):
    B = np.exp(1j * adj_matrix)
    return B

def construct_unitaries(B):
    N = B.shape[0]
    U_mats = []
    for j in range(0, N):
        U_mat = np.zeros((N, N), dtype=complex)
        for k in range(0, N):
            U_mat[k][k] = B[k, j] # Why is this not 1/sqrt(N) * B[k, j]
        U_mats.append(U_mat)
    return U_mats

def is_unitary(m):
    return np.allclose(np.eye(len(m)), m.dot(m.T.conj()))

def check_Us(units):
    print('Checking if all matrices are unitary...')
    for item in units:
        print(is_unitary(item))

# TODO: normalize the edge weights such that the maximum path length
# cannot exceed 2*pi
def normalize_path_lengths(adj_matrix):
    pass


# adj = read_in_graph('./data/graph_0.txt')
# B = construct_B_matrix(adj)
# units = construct_unitaries(B)
# check_Us(units)
