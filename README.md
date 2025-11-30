# EEC289 HW3 — Heuristic Solution for 1000-Node Traveling Salesman Problem

This repository contains a heuristic solution for the 1000-node Traveling Salesman Problem (TSP) using **Nearest Neighbor (NN) initialization combined with 2-opt local search**, under a **strict 60-second time limit**, as required by the EEC289 Homework 3 assignment.

Two complete graphs are solved:
- **Graph A (Euclidean Distance)**
- **Graph B (Random Distance from Uniform[0,100])**

---

## Algorithm Overview

The algorithm follows this pipeline:

1. **Nearest Neighbor (NN) Initialization**
   - Start from a selected node.
   - Repeatedly visit the closest unvisited node.
   - Generates an initial Hamiltonian cycle quickly.

2. **2-opt Local Search Optimization**
   - Iteratively removes two edges and reconnects them if the new configuration shortens the tour.
   - Continues until no further improvement is found (local optimum).

3. **Multiple Random Restarts Under 60 Seconds**
   - Starting nodes are shuffled randomly.
   - NN + 2-opt is applied for each start.
   - The best solution found within **60 seconds** is returned.

4. **Cycle Evaluation Count**
   - Every NN construction and every 2-opt edge-pair evaluation is counted as one evaluated cycle.

---

## Data Files

The repository uses the following input files (provided by the course):

- `TSP_1000_euclidianDistance.txt`
- `TSP_1000_randomDistance.txt`

Each file contains:
- First line: number of nodes (1000)
- Second line: title (ignored)
- Remaining lines: `(node_i, node_j, distance)`

---

## How to Run the Code

1. **Clone the repository**
2. **Ensure the iniput files are in the same directory**
3. Run the solver:
    `python tsp_solver.py`

## Notice
This solver is designed for general 1000-node TSP instances. While two example graphs are provided in this repository (Euclidean and Random), the code will work correctly for any valid input graph with the same format.
