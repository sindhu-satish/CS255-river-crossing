def is_valid_state(M_left, C_left, M_right, C_right, M_total, C_total):
    """
    Check if the current distribution of missionaries and cannibals is valid.
    Rules:
    - On either bank, cannibals should never outnumber missionaries if there are missionaries present.
    """
    # Check left bank
    if M_left < 0 or C_left < 0 or M_right < 0 or C_right < 0:
        return False
    if M_left > M_total or C_left > C_total or M_right > M_total or C_right > C_total:
        return False
    
    if M_left > 0 and C_left > M_left:
        return False
    if M_right > 0 and C_right > M_right:
        return False
    
    return True

def get_next_states(state, M_total, C_total):
    """
    Given the current state, generate all possible next states.
    
    state = (M_left, C_left, M_right, C_right, boat_position)
    boat_position can be 'left' or 'right'.
    """
    M_left, C_left, M_right, C_right, boat_pos = state
    moves = []
    
    # All possible boat loadings (up to two people):
    # (M, C) can be (1,0), (2,0), (0,1), (0,2), (1,1)
    possible_moves = [(1,0), (2,0), (0,1), (0,2), (1,1)]
    
    if boat_pos == 'left':
        for M_move, C_move in possible_moves:
            new_M_left = M_left - M_move
            new_C_left = C_left - C_move
            new_M_right = M_right + M_move
            new_C_right = C_right + C_move
            
            if is_valid_state(new_M_left, new_C_left, new_M_right, new_C_right, M_total, C_total):
                moves.append((new_M_left, new_C_left, new_M_right, new_C_right, 'right'))
    else:  # boat_pos == 'right'
        for M_move, C_move in possible_moves:
            new_M_left = M_left + M_move
            new_C_left = C_left + C_move
            new_M_right = M_right - M_move
            new_C_right = C_right - C_move
            
            if is_valid_state(new_M_left, new_C_left, new_M_right, new_C_right, M_total, C_total):
                moves.append((new_M_left, new_C_left, new_M_right, new_C_right, 'left'))
    
    return moves

def dfs(start_state, goal_state, M_total, C_total, visited=None, path=None):
    """
    Perform a DFS search to find a path from start_state to goal_state.
    """
    if visited is None:
        visited = set()
    if path is None:
        path = []
    
    path.append(start_state)
    visited.add(start_state)
    
    # Check if goal reached
    if start_state == goal_state:
        return path
    
    # Get next possible states
    for nxt in get_next_states(start_state, M_total, C_total):
        if nxt not in visited:
            result = dfs(nxt, goal_state, M_total, C_total, visited, path)
            if result is not None:
                return result
    
    path.pop()
    return None

def solve_missionaries_cannibals(M_total=3, C_total=3, M_left=None, C_left=None, M_right=None, C_right=None, boat_position='left'):
    """
    Solve the missionaries and cannibals problem using DFS.
    
    Inputs:
    - M_total: total number of missionaries
    - C_total: total number of cannibals
    - M_left, C_left, M_right, C_right: initial distribution on each bank.
      If None, defaults to all on left bank and none on right.
    - boat_position: 'left' or 'right'
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
    
    solution_path = dfs(start_state, goal_state, M_total, C_total)
    if solution_path is None:
        print("No solution found.")
        return
    
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
    return output

if __name__ == "__main__":
    # Example usage:
    # Here you can prompt the user or just run the classic scenario.
    # For example:
    # M_total = int(input("Enter total missionaries: "))
    # C_total = int(input("Enter total cannibals: "))
    # ... and so on if needed.
    
    # Using the classic problem:
    result = solve_missionaries_cannibals(M_total=3, C_total=3)
    if result:
        print(result)
