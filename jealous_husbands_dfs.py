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

def generate_moves(state, N):
    """
    Given the current state, generate all possible next states by moving 1 or 2 individuals.
    state = (left_set, right_set, boat_position)
    """
    left, right, boat_pos = state
    if boat_pos == 'L':
        candidates = list(left)
        # Move 1 person
        for i in range(len(candidates)):
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
        # Boat on right side
        candidates = list(right)
        # Move 1 person
        for i in range(len(candidates)):
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


def dfs(state, goal, N, visited, parent):
    """
    Depth-first search for a solution.
    """
    if state == goal:
        return True
    
    visited.add(state)
    
    for nxt in generate_moves(state, N):
        if nxt not in visited:
            parent[nxt] = state
            if dfs(nxt, goal, N, visited, parent):
                return True
    return False


def solve_jealous_husbands(N=3):
    """
    Solve the Jealous Husbands problem using DFS.
    """
    # Initial configuration: all couples on the left bank
    left = frozenset([('H', i) for i in range(1, N+1)] + [('W', i) for i in range(1, N+1)])
    right = frozenset()
    start = (left, right, 'L')
    goal = (frozenset(), frozenset([('H', i) for i in range(1, N+1)] + [('W', i) for i in range(1, N+1)]), 'R')
    
    visited = set()
    parent = {start: None}
    
    if dfs(start, goal, N, visited, parent):
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
        return output
    else:
        return None

if __name__ == "__main__":
    # Example with N=3 couples
    result = solve_jealous_husbands(N=3)
    if result:
        for step, val in result.items():
            print(step, val)
    else:
        print("No solution found.")
