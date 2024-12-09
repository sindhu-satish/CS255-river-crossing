from collections import deque

def is_valid_state(M_left, C_left, M_right, C_right, M_total, C_total):
    """
    Check if the current distribution of missionaries and cannibals is valid.
    """
    # Check for invalid counts
    if M_left < 0 or C_left < 0 or M_right < 0 or C_right < 0:
        return False
    if M_left > M_total or C_left > C_total or M_right > M_total or C_right > C_total:
        return False
    
    # Check constraints: 
    # 1) On either bank, if missionaries > 0, they cannot be outnumbered by cannibals
    if M_left > 0 and C_left > M_left:
        return False
    if M_right > 0 and C_right > M_right:
        return False

    return True

def get_next_states(state, M_total, C_total, boat_capacity):
    """
    Given the current state, generate all possible next states based on the boat capacity.
    state = (M_left, C_left, M_right, C_right, boat_position)
    boat_position can be 'left' or 'right'.
    """
    M_left, C_left, M_right, C_right, boat_pos = state
    
    moves = []
    # Generate possible moves: 
    # For each number of missionaries M_move and cannibals C_move, 
    # 1 <= M_move + C_move <= boat_capacity
    # and at least one of them must be > 0.
    for M_move in range(0, boat_capacity+1):
        for C_move in range(0, boat_capacity+1):
            if 1 <= M_move + C_move <= boat_capacity:
                if boat_pos == 'left':
                    new_M_left = M_left - M_move
                    new_C_left = C_left - C_move
                    new_M_right = M_right + M_move
                    new_C_right = C_right + C_move
                    
                    if is_valid_state(new_M_left, new_C_left, new_M_right, new_C_right, M_total, C_total):
                        moves.append((new_M_left, new_C_left, new_M_right, new_C_right, 'right'))
                else:  # boat_pos == 'right'
                    new_M_left = M_left + M_move
                    new_C_left = C_left + C_move
                    new_M_right = M_right - M_move
                    new_C_right = C_right - C_move
                    
                    if is_valid_state(new_M_left, new_C_left, new_M_right, new_C_right, M_total, C_total):
                        moves.append((new_M_left, new_C_left, new_M_right, new_C_right, 'left'))
    
    return moves

def bfs(M_total, C_total, start_state, goal_state, boat_capacity):
    """
    Perform a BFS search to find a path from start_state to goal_state.
    Returns:
        path (if found) and number of nodes generated.
    """
    queue = deque([start_state])
    visited = set([start_state])
    parent = {start_state: None}  # to reconstruct path
    num_generated = 1  # Count the start state as generated

    while queue:
        current_state = queue.popleft()
        
        if current_state == goal_state:
            # Reconstruct the path
            path = []
            while current_state is not None:
                path.append(current_state)
                current_state = parent[current_state]
            path.reverse()
            return path, num_generated
        
        for nxt in get_next_states(current_state, M_total, C_total, boat_capacity):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = current_state
                queue.append(nxt)
                num_generated += 1

    return None, num_generated

def solve_missionaries_cannibals(M_total=3, C_total=3, boat_capacity=2, 
                                M_left=None, C_left=None, M_right=None, C_right=None, boat_position='left'):
    """
    Solve the missionaries and cannibals problem using BFS.
    
    Inputs:
    - M_total: total number of missionaries
    - C_total: total number of cannibals
    - boat_capacity: capacity of the boat
    - M_left, C_left, M_right, C_right: initial distribution. Defaults to all on left.
    - boat_position: 'left' or 'right'
    
    Returns:
      (output, num_generated)
      output: dictionary representing the path if solution is found, else None.
      num_generated: number of states generated in the search.
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
    
    solution_path, num_generated = bfs(M_total, C_total, start_state, goal_state, boat_capacity)
    if solution_path is None:
        print("No solution found.")
        return {"output": output, "number_of_states": num_generated}
    
    # Convert solution path to required output format
    output = {}
    for i, (Ml, Cl, Mr, Cr, bp) in enumerate(solution_path):
        output[str(i)] = {
            'M_left': Ml,
            'C_left': Cl,
            'M_right': Mr,
            'C_right': Cr,
            'boat_position': bp
        }
    return {"output": output, "number_of_states": num_generated}

if __name__ == "__main__":
    M_total = 6
    C_total = M_total
    boat_capacity = M_total - 1
    result, num_generated = solve_missionaries_cannibals(M_total=M_total, C_total=C_total, boat_capacity=boat_capacity)
    if result:
        for step, val in result.items():
            print(step, val)
        print("Number of nodes generated in the state space:", num_generated)
    else:
        print("No solution found.")
        print("Number of nodes generated:", num_generated)
