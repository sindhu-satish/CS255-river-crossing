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
    # On either bank, if missionaries > 0, they cannot be outnumbered by cannibals
    if M_left > 0 and C_left > M_left:
        return False
    if M_right > 0 and C_right > M_right:
        return False

    return True

def get_next_states(state, M_total, C_total, boat_capacity):
    """
    Given the current state, generate all possible next states based on the boat capacity.
    state = (M_left, C_left, M_right, C_right, boat_position)
    """
    M_left, C_left, M_right, C_right, boat_pos = state
    
    moves = []
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

def dfs(M_total, C_total, start_state, goal_state, boat_capacity):
    """
    Perform a DFS search to find a path from start_state to goal_state.
    Returns:
        (path, number_of_states_traversed)
    """
    stack = [start_state]
    visited = set([start_state])
    parent = {start_state: None}
    num_traversed = 0

    while stack:
        current_state = stack.pop()
        num_traversed += 1 

        if current_state == goal_state:
            # Reconstruct the path
            path = []
            while current_state is not None:
                path.append(current_state)
                current_state = parent[current_state]
            path.reverse()
            return path, num_traversed
        
        for nxt in get_next_states(current_state, M_total, C_total, boat_capacity):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = current_state
                stack.append(nxt)

    return None, num_traversed

def solve_missionaries_cannibals(M_total=3, C_total=3, boat_capacity=2, 
                                M_left=None, C_left=None, M_right=None, C_right=None, boat_position='left'):
    """
    Solve the missionaries and cannibals problem using DFS.
    
    Returns:
      {
        "output": dictionary representing the path if solution is found, else None,
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
    
    solution_path, num_traversed = dfs(M_total, C_total, start_state, goal_state, boat_capacity)
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
    M_total = 3
    C_total = M_total
    boat_capacity = 2
    result = solve_missionaries_cannibals(M_total=M_total, C_total=C_total, boat_capacity=boat_capacity)
    if result["output"] is not None:
        for step, val in result["output"].items():
            print(step, val)
        print("Number of states traversed in the state space:", result["number_of_states"])
    else:
        print("No solution found.")
        print("Number of states traversed:", result["number_of_states"])
