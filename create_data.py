import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

MAX_EDGE_WEIGHT = np.pi/2

def write_data():
    for file in range(4):
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

        name = './data/graph_' + str(file) + '.txt'
        print('Writing to file: ' + name)
        nx.write_weighted_edgelist(G, name)

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

write_graph_from_paper()
