from itertools import combinations

def is_valid_side(people):
    """
    Check if the given side (set of (Gender, ID)) satisfies the jealous husbands constraint.
    For each woman W_i on this side, if her husband H_i is not present, then no other men should be present.
    """
    men = {p for p in people if p[0] == 'H'}
    women = {p for p in people if p[0] == 'W'}
    
    for w in women:
        i = w[1]
        h = ('H', i)
        if h not in people:
            # Her husband is not here, so this side must not have any other men
            if len(men) > 0:
                return False
    return True

def is_valid_state(left, right):
    """
    State is valid if both left and right sides satisfy the constraints.
    """
    return is_valid_side(left) and is_valid_side(right)

def generate_moves(state, N, boat_capacity):
    """
    Given the current state, generate all possible next states by moving
    from 1 up to boat_capacity individuals.
    state = (left_set, right_set, boat_position)
    """
    left, right, boat_pos = state
    if boat_pos == 'L':
        candidates = list(left)
        # Move from 1 up to boat_capacity individuals from left to right
        for size in range(1, boat_capacity + 1):
            for moved in combinations(candidates, size):
                new_left = set(left) - set(moved)
                new_right = set(right) | set(moved)
                if is_valid_state(new_left, new_right):
                    yield (frozenset(new_left), frozenset(new_right), 'R')
    else:
        candidates = list(right)
        # Move from 1 up to boat_capacity individuals from right to left
        for size in range(1, boat_capacity + 1):
            for moved in combinations(candidates, size):
                new_right = set(right) - set(moved)
                new_left = set(left) | set(moved)
                if is_valid_state(new_left, new_right):
                    yield (frozenset(new_left), frozenset(new_right), 'L')

def dfs(state, goal, N, boat_capacity, visited, parent, nodes_generated):
    """
    Depth-first search for a solution.
    
    nodes_generated is a list with one element (to mutate inside the function).
    We'll increment nodes_generated[0] every time we generate a new state.
    """
    if state == goal:
        return True
    
    visited.add(state)
    
    for nxt in generate_moves(state, N, boat_capacity):
        if nxt not in visited:
            parent[nxt] = state
            nodes_generated[0] += 1  # Counting this newly discovered node
            if dfs(nxt, goal, N, boat_capacity, visited, parent, nodes_generated):
                return True
    return False

def solve_jealous_husbands(N=3, boat_capacity=2, left=None, right=None, boat_pos='L'):
    """
    Solve the Jealous Husbands problem using DFS with the ability to set an arbitrary initial state.
    
    Parameters:
        N (int): number of couples
        boat_capacity (int): capacity of the boat
        left (array of arrays): e.g. [["H",1], ["W",1], ...]
        right (array of arrays): e.g. [["H",3], ["W",3], ...]
        boat_pos (str): 'L' or 'R' indicating where the boat starts
    
    Returns:
        A dictionary with "output" and "number_of_states".
        If no solution is found, "output" is None.
    """
    # Convert input arrays to frozensets of tuples if provided
    if left is None:
        left = frozenset([('H', i) for i in range(1, N+1)] + [('W', i) for i in range(1, N+1)])
    else:
        left = frozenset(tuple(p) for p in left)
    
    if right is None:
        right = frozenset()
    else:
        right = frozenset(tuple(p) for p in right)
    
    start = (left, right, boat_pos)
    goal = (frozenset(), frozenset([('H', i) for i in range(1, N+1)] + [('W', i) for i in range(1, N+1)]), 'R')
    
    visited = set()
    parent = {start: None}
    nodes_generated = [1]  # Start node counts as generated
    
    if dfs(start, goal, N, boat_capacity, visited, parent, nodes_generated):
        # Reconstruct path
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        
        # Format output
        output = {}
        for i, (l, r, bp) in enumerate(path):
            output[str(i)] = {
                'left_bank': sorted(list(l)),
                'right_bank': sorted(list(r)),
                'boat_position': bp
            }
        return {"output": output, "number_of_states": nodes_generated[0]}
    else:
        return {"output": None, "number_of_states": nodes_generated[0]}

if __name__ == "__main__":
    # Example usage:
    N = 4
    boat_capacity = 4
    left_bank = [["H",1], ["W",1], ["H",2], ["W",2]]
    right_bank = [["H",3], ["W",3], ["H",4], ["W",4]]
    boat_position = 'R'

    result = solve_jealous_husbands(N=N, boat_capacity=boat_capacity, left=left_bank, right=right_bank, boat_pos=boat_position)
    if result["output"] is not None:
        for step, val in result["output"].items():
            print(step, val)
        print("Number of states visited in the state space:", result["number_of_states"])
    else:
        print("No solution found.")
        print("Number of states visited in the state space:", result["number_of_states"])
