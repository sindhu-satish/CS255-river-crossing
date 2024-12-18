import heapq
import math

def is_valid_state(M_left, C_left, M_right, C_right, M_total, C_total):
    # Check invalid counts
    if M_left < 0 or C_left < 0 or M_right < 0 or C_right < 0:
        return False
    if M_left > M_total or C_left > C_total or M_right > M_total or C_right > C_total:
        return False
    
    # Check missionary constraint
    if M_left > 0 and C_left > M_left:
        return False
    if M_right > 0 and C_right > M_right:
        return False
    
    return True

def get_possible_moves(boat_capacity):
    moves = []
    for i in range(boat_capacity + 1):   # i missionaries
        for j in range(boat_capacity + 1):  # j cannibals
            if i + j <= boat_capacity and i + j > 0:
                moves.append((i, j))
    return moves

def get_next_states(state, M_total, C_total, boat_capacity):
    """
    Generate all valid next states from the given state.
    state = (M_left, C_left, M_right, C_right, boat_pos)
    boat_pos in {'left', 'right'}
    """
    M_left, C_left, M_right, C_right, boat_pos = state
    possible_moves = get_possible_moves(boat_capacity)
    next_states = []
    
    if boat_pos == 'left':
        for M_move, C_move in possible_moves:
            new_M_left = M_left - M_move
            new_C_left = C_left - C_move
            new_M_right = M_right + M_move
            new_C_right = C_right + C_move
            if is_valid_state(new_M_left, new_C_left, new_M_right, new_C_right, M_total, C_total):
                next_states.append((new_M_left, new_C_left, new_M_right, new_C_right, 'right'))
    else:  # boat is on the right
        for M_move, C_move in possible_moves:
            new_M_left = M_left + M_move
            new_C_left = C_left + C_move
            new_M_right = M_right - M_move
            new_C_right = C_right - C_move
            if is_valid_state(new_M_left, new_C_left, new_M_right, new_C_right, M_total, C_total):
                next_states.append((new_M_left, new_C_left, new_M_right, new_C_right, 'left'))
    
    return next_states

def heuristic(state, M_total, C_total):
    """
    Heuristic: a simple estimate of trips remaining.
    h = ceil((M_left + C_left)/2)
    """
    M_left, C_left, M_right, C_right, boat_pos = state
    people_left = M_left + C_left
    return math.ceil(people_left / 2.0)

def astar_search(M_total, C_total, start_state, goal_state, boat_capacity):
    """
    A* search to find the shortest path from start_state to goal_state.
    Returns:
      path: The sequence of states from start to goal.
      num_traversed: Number of states traversed (popped from the priority queue).
    """
    open_heap = []
    g_cost = {start_state: 0}
    parent = {start_state: None}
    
    start_h = heuristic(start_state, M_total, C_total)
    heapq.heappush(open_heap, (start_h, 0, start_state))
    visited = set()
    num_traversed = 0  

    while open_heap:
        f, g, current = heapq.heappop(open_heap)
        num_traversed += 1  

        if current in visited:
            continue
        visited.add(current)
        
        # Check if goal reached
        if current == goal_state:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, num_traversed
        
        # Explore neighbors
        for nxt in get_next_states(current, M_total, C_total, boat_capacity):
            tentative_g = g + 1
            if nxt not in g_cost or tentative_g < g_cost[nxt]:
                g_cost[nxt] = tentative_g
                parent[nxt] = current
                h = heuristic(nxt, M_total, C_total)
                f = tentative_g + h
                heapq.heappush(open_heap, (f, tentative_g, nxt))

    return None, num_traversed

def solve_missionaries_cannibals(M_total=3, C_total=3, boat_capacity=2, 
                                M_left=None, C_left=None, M_right=None, C_right=None, boat_position='left'):
    """
    Solve the missionaries and cannibals problem using A* search.
    
    Returns:
      {
        "output": solution_path_as_dict or None,
        "number_of_states": number_of_states_traversed,
        "N": M_total
      }
    """
    if M_left is None:
        M_left = M_total
    if C_left is None:
        C_left = C_total
    if M_right is None:
        M_right = 0
    if C_right is None:
        C_right = 0
    
    start_state = (M_left, C_left, M_right, C_right, boat_position)
    goal_state = (0, 0, M_total, C_total, 'right')
    
    solution_path, num_traversed = astar_search(M_total, C_total, start_state, goal_state, boat_capacity)
    if solution_path is None:
        print("No solution found.")
        return {"output": None, "number_of_states": num_traversed, "N": M_total}
    
    output = {}
    for i, (Ml, Cl, Mr, Cr, bp) in enumerate(solution_path):
        output[str(i)] = {
            'M_left': Ml,
            'C_left': Cl,
            'M_right': Mr,
            'C_right': Cr,
            'boat_position': bp
        }
    return {"output": output, "number_of_states": num_traversed, "N": M_total}

if __name__ == "__main__":
    M_total = 6
    C_total = 6
    boat_capacity = C_total - 1
    
    result = solve_missionaries_cannibals(M_total=M_total, C_total=C_total, boat_capacity=boat_capacity)
    if result["output"]:
        print("Solution path:")
        for step, val in result["output"].items():
            print(step, val)
        print("Number of states traversed in the state space:", result["number_of_states"])
    else:
        print("No solution found.")
        print("Number of states traversed:", result["number_of_states"])
