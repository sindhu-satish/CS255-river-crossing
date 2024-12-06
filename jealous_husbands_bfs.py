from collections import deque

def is_valid_side(people):
    """
    Check if the given side (set of (Gender, ID)) satisfies the jealous husbands constraint.
    Constraint:
    For each woman W_i, if H_i is not present on this side, then there must be no men (H_j) on this side.
    """
    # Separate men and women by their IDs
    men = {p for p in people if p[0] == 'H'}
    women = {p for p in people if p[0] == 'W'}
    
    for w in women:
        # For each woman W_i
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

def generate_moves(state, N):
    """
    Given the current state, generate all possible next states by moving 1 or 2 individuals
    from one bank to the other.
    """
    left, right, boat_pos = state
    if boat_pos == 'L':
        # Choose 1 or 2 people from left to move to right
        candidates = list(left)
        for i in range(len(candidates)):
            # Move 1 person
            moved = [candidates[i]]
            new_left = set(left) - set(moved)
            new_right = set(right) | set(moved)
            if is_valid_state(new_left, new_right):
                yield (frozenset(new_left), frozenset(new_right), 'R')
                
            # Move 2 people
            for j in range(i+1, len(candidates)):
                moved = [candidates[i], candidates[j]]
                new_left = set(left) - set(moved)
                new_right = set(right) | set(moved)
                if is_valid_state(new_left, new_right):
                    yield (frozenset(new_left), frozenset(new_right), 'R')
    else:
        # Boat on right, move people from right to left
        candidates = list(right)
        for i in range(len(candidates)):
            # Move 1 person
            moved = [candidates[i]]
            new_right = set(right) - set(moved)
            new_left = set(left) | set(moved)
            if is_valid_state(new_left, new_right):
                yield (frozenset(new_left), frozenset(new_right), 'L')
            
            # Move 2 people
            for j in range(i+1, len(candidates)):
                moved = [candidates[i], candidates[j]]
                new_right = set(right) - set(moved)
                new_left = set(left) | set(moved)
                if is_valid_state(new_left, new_right):
                    yield (frozenset(new_left), frozenset(new_right), 'L')

def solve_jealous_husbands(N=3):
    """
    Solve the jealous husbands problem using BFS.
    Initially, all N couples (H1,W1,...,HN,WN) are on the left bank.
    Goal: Move everyone to the right bank.
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
            # We'll just print who is on left/right and boat position at each step
            output = {}
            for i, (l, r, bp) in enumerate(path):
                output[str(i)] = {
                    'left_bank': sorted(list(l)),
                    'right_bank': sorted(list(r)),
                    'boat_position': bp
                }
            return output
        
        for nxt in generate_moves(state, N):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = state
                queue.append(nxt)
    
    return None

if __name__ == "__main__":
    # Example with N=3 couples
    result = solve_jealous_husbands(N=3)
    res_list = []
    if result:
        for step, val in result.items():
            res_list.append(val)
        print(res_list)
    else:
        print("No solution found.")
