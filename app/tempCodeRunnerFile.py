is_move_safe = {"up": True, "down": True, "left": True, "right": True}

safe_moves = [move for move, isSafe in is_move_safe.items() if isSafe]
print(safe_moves)