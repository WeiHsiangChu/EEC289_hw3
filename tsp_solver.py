import numpy as np
import time

cycle_counts = 0

def load_tsp_txt(filepath):
    with open(filepath, "r") as f:
        
        first_line = f.readline()
        first_line = first_line.strip()
        n = int(first_line) # 1000 nodes

        _ = f.readline() #ignore title

        distance = np.full((n, n), np.inf) # n * n distance matrix

        for line in f:
            parts = line.split()
            i, j, d = parts

            i = int(i) - 1
            j = int(j) - 1
            d = float(d)

            distance[i, j] = d
            distance[j, i] = d

        np.fill_diagonal(distance, 0.0)

        return distance


def path_length(path, distance):
    total = 0.0

    for i in range(len(path) - 1):
        a = path[i]
        b = path[i + 1]
        total += distance[a,b]

    total += distance[path[-1], path[0]] # add distance from the last node to the start node

    return total


def nn(distance, start):
    global cycle_counts
    n = distance.shape[0]
    unvisited = set(range(n))
    path = [start]
    unvisited.remove(start)
    current = start

    while unvisited:
        next_node = min(unvisited, key=lambda j: distance[current, j])
        path.append(next_node)
        unvisited.remove(next_node)
        current = next_node

    cycle_counts += 1
    return path


def two_opt(path, distance, start_time, time_limit):
    global cycle_counts
    n = len(path) # number of nodes in the path

    improved = True
    while improved:
        if time.time() - start_time >= time_limit:
            return path
        improved = False

        for i in range(1, n - 2): # first edge
            if time.time() - start_time >= time_limit:
                return path
            a = path[i - 1]
            b = path[i]
  
            for j in range(i + 1, n - 1): # second edge
                if time.time() - start_time >= time_limit:
                    return path
                c = path[j]
                d = path[j + 1]

                cycle_counts += 1 # each (i, j) corresponds to evaluating one possible new cycle
                old_cost = distance[a, b] + distance[c, d]
                new_cost = distance[a, c] + distance[b, d]

                if new_cost < old_cost:
                    path[i:j + 1] = reversed(path[i:j + 1]) # reverse i to j to reconstruct the cycle

                    improved = True
                    break # once we found one improvement for fixed i and swap it, the path has changed, any further j chceks are invalid
            if improved:
                break # the path was changed, so we start from the beginning

    return path 


def best_path_in_one_min(distance, time_limit=60):
    global cycle_counts
    cycle_counts = 0

    n = distance.shape[0]
    start_candidates = list(range(n))
    np.random.seed(42)
    np.random.shuffle(start_candidates)

    best_cost = np.inf
    best_path = None

    start_time = time.time()

    for start in start_candidates:
        if time.time() - start_time >= time_limit:
            break

        nn_path = nn(distance, start=start)

        two_opt_path = two_opt(nn_path, distance, start_time, time_limit)

        cost = path_length(two_opt_path, distance)

        if cost < best_cost:
            best_cost = cost
            best_path = two_opt_path.copy()

    return best_path, best_cost, cycle_counts


def save_solution(path, sid):
    filename = f"solution_{sid}.txt"

    with open(filename, "w") as f:
        cycle = [node + 1 for node in path]
        cycle.append(cycle[0])
        line = ", ".join(str(x) for x in cycle)
        f.write(line + "\n\n")

input_graph = "YOUR_GRAPH_FILE.txt" # the path to the graph's text file
SID = "YOUR_STUDENT_ID" # student id

distance = load_tsp_txt(input_graph)
best_path, best_cost, cycle_counts = best_path_in_one_min(distance, time_limit=60)
print("best cost: ", f"{best_cost: .2f}")
print("cycle evaluation counts: ", f"{cycle_counts: .1e}")
save_solution(best_path, SID)
