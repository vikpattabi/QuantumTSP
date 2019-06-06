import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import sys

MAX_EDGE_WEIGHT = np.pi/2


help_msg = '\nUsage instructions for the data.py Quantum TSP solver: \n' \
            '-------------------------------------------------------\n'\
            '-Call \'python data.py --view_graph [filename]\' to view a networkx visualization of a given graph.\n'\
            '-Call \'python data.py --write_graph [filename]\' to write a random graph for testing. Edge weights will be'\
            'picked so as to normalize the maximum path length to be less than 2*pi.'


def write_data(path):
    G = nx.Graph()
    for i in range(4):
        G.add_node(i)


    for i in range(1, 4):
        G.add_edges_from([(0, i, {'weight': np.random.uniform(0, MAX_EDGE_WEIGHT)})])

    for i in range(2, 4):
        G.add_edges_from([(1, i, {'weight': np.random.uniform(0, MAX_EDGE_WEIGHT)})])

    for i in range(3, 4):
        G.add_edges_from([(2, i, {'weight': np.random.uniform(0, MAX_EDGE_WEIGHT)})])

    nx.draw(G, pos=nx.spring_layout(G))
    nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G))
    plt.show()

    print('Writing to file: ' + path)
    nx.write_weighted_edgelist(G, path)

def view_graph(path):
    G = nx.read_weighted_edgelist(path)
    pos = nx.spring_layout(G)
    nx.draw(G, pos=pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos=pos)
    plt.show()

def write_graph_from_paper():
    A = np.array([
        [0, np.pi/2, np.pi/8, np.pi/4],
        [np.pi/2, 0, np.pi/4, np.pi/4],
        [np.pi/8, np.pi/4, 0, np.pi/8],
        [np.pi/4, np.pi/4, np.pi/8, 0]
    ])
    G = nx.from_numpy_matrix(A)

    name = './data/graph_from_paper.txt'
    print('Writing to file: ' + name)
    nx.write_weighted_edgelist(G, name)

def get_args():
    n_args = len(sys.argv) - 1
    if n_args < 1:
        raise Exception('Enter a fn to name to call.')
    if n_args == 1 and sys.argv[1] == '--help':
        print(help_msg)
        return False
    if sys.argv[1] == '--write_graph':
        if n_args != 2:
            raise Exception('Program takes input [fn name] [path, optional]')
        path = sys.argv[2]
        return (True, path)
    elif sys.argv[1] == '--view_graph':
        if n_args != 2:
            raise Exception('Program takes input [fn name] [path, optional]')
        path = sys.argv[2]
        return (False, path)
    return sys.argv[1]

def main():
  path = get_args()
  if not path:
      return
  if len(path) == 2:
      if path[0]:
          write_data(path[1])
      else:
          view_graph(path[1])

if __name__== "__main__":
  main()
