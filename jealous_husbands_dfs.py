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


def solve_jealous_husbands(N=3, boat_capacity=2):
    """
    Solve the Jealous Husbands problem using DFS.
    
    Returns:
        (output, num_nodes_generated)
        output: Dictionary of steps if a solution is found, else None.
        num_nodes_generated: number of nodes generated in the state space.
    """
    # Initial configuration: all couples on the left bank
    left = frozenset([('H', i) for i in range(1, N+1)] + [('W', i) for i in range(1, N+1)])
    right = frozenset()
    start = (left, right, 'L')
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
    N = 5
    boat_capacity = N-1
    result, num_generated = solve_jealous_husbands(N, boat_capacity)
    if result:
        for step, val in result.items():
            print(step, val)
        print("Number of nodes generated in the state space:", num_generated)
    else:
        print("No solution found.")
        print("Number of nodes generated:", num_generated)
