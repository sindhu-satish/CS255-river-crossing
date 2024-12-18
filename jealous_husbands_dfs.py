from itertools import combinations
import sys
sys.setrecursionlimit(10**6)


def is_valid_side(people):
    """
    Check if the given side satisfies the jealous husbands constraint.
    """
    men = {p for p in people if p[0] == 'H'}
    women = {p for p in people if p[0] == 'W'}

    for w in women:
        i = w[1]
        h = ('H', i)
        if h not in people:
            # If her husband is not here, no other men should be present
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
    Generate possible moves based on current state.
    """
    left, right, boat_pos = state
    if boat_pos == 'L':
        candidates = list(left)
        for size in range(1, boat_capacity + 1):
            for moved in combinations(candidates, size):
                new_left = set(left) - set(moved)
                new_right = set(right) | set(moved)
                if is_valid_state(new_left, new_right):
                    yield (frozenset(new_left), frozenset(new_right), 'R')
    else:
        candidates = list(right)
        for size in range(1, boat_capacity + 1):
            for moved in combinations(candidates, size):
                new_right = set(right) - set(moved)
                new_left = set(left) | set(moved)
                if is_valid_state(new_left, new_right):
                    yield (frozenset(new_left), frozenset(new_right), 'L')


def dfs_recursive(current, goal, N, boat_capacity, visited, parent, states_traversed):
    """
    Recursive DFS that counts the number of states TRAVERSED, not generated.
    Each time we process a state (current), we increment states_traversed.
    """
    # Mark this state as traversed
    states_traversed[0] += 1
    
    if current == goal:
        return True

    visited.add(current)

    moves = list(generate_moves(current, N, boat_capacity))
    # Prioritize moves by the number of people on the right bank
    moves.sort(key=lambda x: len(x[1]))

    for nxt in moves:
        if nxt not in visited:
            parent[nxt] = current
            if dfs_recursive(nxt, goal, N, boat_capacity, visited, parent, states_traversed):
                return True
    return False

def solve_jealous_husbands(N=3, boat_capacity=2, left=None, right=None, boat_pos='L'):
    """
    Solve the Jealous Husbands problem using a normal (recursive) DFS, 
    and return the number of states TRAVERSED.
    """
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
    states_traversed = [0]  

    if dfs_recursive(start, goal, N, boat_capacity, visited, parent, states_traversed):
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()

        output = {}
        for i, (l, r, bp) in enumerate(path):
            output[str(i)] = {
                'left_bank': sorted(list(l)),
                'right_bank': sorted(list(r)),
                'boat_position': bp
            }
        return {"output": output, "number_of_states": states_traversed[0], "N": N}
    else:
        return {"output": None, "number_of_states": states_traversed[0], "N": N}


if __name__ == "__main__":
    N = 3
    boat_capacity = 2
    result = solve_jealous_husbands(N=N, boat_capacity=boat_capacity)
    if result["output"] is not None:
        for step, val in result["output"].items():
            print(step, val)
        print("Number of states traversed in the state space:", result["number_of_states"])
    else:
        print("No solution found.")
        print("Number of states traversed in the state space:", result["number_of_states"])
