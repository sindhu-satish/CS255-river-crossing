import math
import heapq

def is_valid_side(people):
    """
    Check the jealous husbands constraint for one side.
    If a woman W_i is present without H_i, then no other men can be present.
    """
    men = {p for p in people if p[0] == 'H'}
    women = {p for p in people if p[0] == 'W'}
    
    for w in women:
        i = w[1]
        h = ('H', i)
        if h not in people:
            # Her husband isn't here, so no other men allowed
            if len(men) > 0:
                return False
    return True

def is_valid_state(left, right):
    """
    A state is valid if both sides satisfy the jealous husbands constraint.
    """
    return is_valid_side(left) and is_valid_side(right)

def generate_moves(state, N):
    """
    Generate next possible states by moving 1 or 2 people.
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

def heuristic(state, N):
    """
    Heuristic function:
    h = ceil((number_of_people_on_left) / 2)
    """
    left, right, boat_pos = state
    people_on_left = len(left)
    return math.ceil(people_on_left / 2.0)

def astar_search(N, start, goal):
    """
    A* search for the Jealous Husbands problem.
    """
    g_cost = {start: 0}
    parent = {start: None}
    
    start_h = heuristic(start, N)
    # Priority queue of (f, g, state)
    # f = g + h
    open_set = []
    heapq.heappush(open_set, (start_h, 0, start))
    visited = set()
    
    while open_set:
        f, g, current = heapq.heappop(open_set)
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == goal:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path
        
        for nxt in generate_moves(current, N):
            tentative_g = g + 1
            if nxt not in g_cost or tentative_g < g_cost[nxt]:
                g_cost[nxt] = tentative_g
                parent[nxt] = current
                h = heuristic(nxt, N)
                f = tentative_g + h
                heapq.heappush(open_set, (f, tentative_g, nxt))
    return None

def solve_jealous_husbands(N=3):
    """
    Solve the Jealous Husbands problem using A* search.
    """
    # Initial state: all on left
    left = frozenset([('H', i) for i in range(1, N+1)] + [('W', i) for i in range(1, N+1)])
    right = frozenset()
    start = (left, right, 'L')
    goal = (frozenset(), frozenset([('H', i) for i in range(1, N+1)] + [('W', i) for i in range(1, N+1)]), 'R')
    
    path = astar_search(N, start, goal)
    if path is None:
        return None
    
    # Convert path to required output format
    output = {}
    for i, (l, r, bp) in enumerate(path):
        output[str(i)] = {
            'left_bank': sorted(list(l)),
            'right_bank': sorted(list(r)),
            'boat_position': bp
        }
    return output

if __name__ == "__main__":
    # Example with N=3 couples
    result = solve_jealous_husbands(N=3)
    if result:
        for step, val in result.items():
            print(step, val)
    else:
        print("No solution found.")
