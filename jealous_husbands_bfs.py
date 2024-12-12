from collections import deque
import itertools

def is_valid_side(people):
    """
    Check if the given side (set of (Gender, ID)) satisfies the jealous husbands constraint.
    For each woman W_i, if H_i is not present on this side, then no other man can be present.
    """
    men = {p for p in people if p[0] == 'H'}
    women = {p for p in people if p[0] == 'W'}
    
    for w in women:
        i = w[1]
        h = ('H', i)
        if h not in people:
            # Her husband is not here, so no other men allowed
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

def solve_jealous_husbands(N=3, boat_capacity=2, left=None, right=None, boat_pos='L'):
    """
    Solve the jealous husbands problem using BFS with a possibly arbitrary initial state.
    
    Parameters:
        N (int): number of couples
        boat_capacity (int): capacity of the boat
        left (array of arrays): e.g. [["H",1], ["W",1], ["H",2], ["W",2]]
        right (array of arrays): e.g. [["H",3], ["W",3], ["H",4], ["W",4]]
        boat_pos (str): 'L' or 'R' indicating where the boat starts
        
    Returns:
       A dictionary: {"output": <path_dict>, "number_of_states": <int>}
       If no solution is found, "output" is None.
    """
    # Convert input arrays to frozensets of tuples if given
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
        print("Number of visited states:", result["number_of_states"])
    else:
        print("No solution found.")
        print("Number of visited states:", result["number_of_states"])
