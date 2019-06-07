# QuantumTSP
Implementation of a Traveling Salesman solver using a Quantum Virtual Machine
<br/>
Final Project for Stanford's CS269Q: 'Quantum Computer Programming' 
<br/>
# Installation Notes
Required packages include Python 3.7, pyQuil, networkx, matplotlib, and numpy. Installing pyQuil and running a QVM instance as described in the CS269Q pyQuil guide should be sufficient for running this project. Furthermore, files must be run with an active QVM server.
<br/>
# How to use this Project
This project features a number of files designed to implement a Quantum Phase Estimation approach to solving the Traveling Salesman Problem. The core file is __solver.py__ which implements functions from __tsp_funcs.py__ and __quantum_funcs.py__. Another file, __data.py__, allows the user to visualize saves networks and randomly generate new (already normalized) networks on which to test.
<br/>
<br/>
__solver.py__
<br/>
<br/>
Calling __python solver.py__ executes the basic version of the TSP solver. Various flags can be added to change the solver behavior, and they can be viewed by calling __python solver.py --help__. Specifically, they are:
* __--print_quil__ displays the aggregated quil program to be run on the qvm 
* __--fully_quantum__ aggregates the eigenstate testing code fully into quil, as opposed to running 6 iterations of the eigenstate testing using a for-loop. There is a negligible speed-up, but printing the quil program yields a much larger result.
* __--graph=[filename]__ runs the solver on a specified graph relative to the current path. The referenced file should be a .txt containing the results of writing a graph via networkx.write_weighted_edgelist. If this is not called, the default graph is __data/graph_from_paper.txt__
* __--num_trials=[int]__ runs the solver for [int] times on the specified graph and prints the results of this accuracy testing. The default for this value is 1. 
<br/>
<br/>
Although not modifiable via an external flag, changing the 'verbose' parameter of construct_soln_table in this file's main function will turn on/off the solver's tabular printing of results after computing the phases.
<br/>
<br/>
**data.py**
<br/> 
<br/>
This program is useful for visualizing test graphs and generating new random test graphs. Running __python data.py --help__ will display information on how to use the flags for this file which should be intuitive. 

