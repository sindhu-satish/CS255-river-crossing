from collections import deque
import itertools

def is_valid_side(people):
    """
    Check if the given side (set of (Gender, ID)) satisfies the jealous husbands constraint.
    Constraint:
    For each woman W_i, if H_i is not present on this side, then there must be no men (H_j) on this side.
    """
    men = {p for p in people if p[0] == 'H'}
    women = {p for p in people if p[0] == 'W'}
    
    for w in women:
        i = w[1]
        h = ('H', i)
        if h not in people:
            # Her husband is not here
            # Check if any other man is present
            if len(men) > 0:
                return False
    return True

def is_valid_state(left, right):
    """
    State is valid if both left and right banks satisfy the constraints.
    """
    return is_valid_side(left) and is_valid_side(right)

def generate_moves(state, N, boat_capacity):
    """
    Given the current state, generate all possible next states by moving
    from 1 up to boat_capacity individuals from one bank to the other.
    """
    left, right, boat_pos = state
    if boat_pos == 'L':
        # Move people from left to right
        candidates = list(left)
        for size in range(1, boat_capacity + 1):
            for moved in itertools.combinations(candidates, size):
                new_left = set(left) - set(moved)
                new_right = set(right) | set(moved)
                if is_valid_state(new_left, new_right):
                    yield (frozenset(new_left), frozenset(new_right), 'R')
    else:
        # Move people from right to left
        candidates = list(right)
        for size in range(1, boat_capacity + 1):
            for moved in itertools.combinations(candidates, size):
                new_right = set(right) - set(moved)
                new_left = set(left) | set(moved)
                if is_valid_state(new_left, new_right):
                    yield (frozenset(new_left), frozenset(new_right), 'L')

def solve_jealous_husbands(N=3, boat_capacity=2):
    """
    Solve the jealous husbands problem using BFS.
    Initially, all N couples (H1,W1,...,HN,WN) are on the left bank.
    Goal: Move everyone to the right bank.
    
    Returns:
       (output, num_visited)
       output: A dictionary of steps if a solution is found, else None.
       num_visited: The number of states visited in the state space.
    """
    # Create initial sets
    left = frozenset([('H', i) for i in range(1, N+1)] + [('W', i) for i in range(1, N+1)])
    right = frozenset()
    start = (left, right, 'L')
    goal = (frozenset(), frozenset([('H', i) for i in range(1, N+1)] + [('W', i) for i in range(1, N+1)]), 'R')
    
    # BFS
    queue = deque([start])
    visited = set([start])
    parent = {start: None}
    
    while queue:
        state = queue.popleft()
        if state == goal:
            # Reconstruct path
            path = []
            cur = state
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            
            # Convert path to readable output
            output = {}
            for i, (l, r, bp) in enumerate(path):
                output[str(i)] = {
                    'left_bank': sorted(list(l)),
                    'right_bank': sorted(list(r)),
                    'boat_position': bp
                }
            return {"output": output, "number_of_states": len(visited)}
        
        for nxt in generate_moves(state, N, boat_capacity):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = state
                queue.append(nxt)
    
    return {"output": None, "number_of_states": len(visited)}

if __name__ == "__main__":
    N = 4
    boat_capacity = N - 1
    result, num_visited = solve_jealous_husbands(N, boat_capacity)
    res_list = []
    if result:
        for step, val in result.items():
            res_list.append(val)
        print(res_list)
        print("Number of visited states:", num_visited)
    else:
        print("No solution found.")
        print("Number of visited states:", num_visited)
