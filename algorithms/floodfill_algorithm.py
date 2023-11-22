# Function to calculate flood-fill score from a given starting point
def calculate_flood_fill_score(start, game_state):
    visited = set()
    stack = [start]

    while stack:
        x, y = stack.pop()
        if (x, y) not in visited:
            visited.add((x, y))

            # Explore adjacent cells (up, down, left, right)
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_x, next_y = x + dx, y + dy
                if is_valid_move(game_state, next_x, next_y):
                    stack.append((next_x, next_y))

    return len(visited)  # Return the size of the visited set, representing the connected region

# Function to check if a move is valid (within grid and not colliding with snake bodies)
def is_valid_move(game_state, x, y):
    # Extract relevant information from the game_state
    board = game_state["board"]
    width, height = board["width"], board["height"]
    snakes = board["snakes"]

    # Check if the move is within the game grid
    if x < 0 or x >= width or y < 0 or y >= height:
        return False

    # Check if the move is not colliding with a snake body
    for snake in snakes:
        for body_part in snake["body"]:
            if body_part["x"] == x and body_part["y"] == y:
                return False

    # If all checks pass, the move is valid
    return True

# Function to find invalid moves using flood-fill algorithm
def find_invalid_moves_using_floodfill(game_state, threshold):
    invalid_moves = []
    total_valid_moves = []
    head_x, head_y = tuple(game_state["you"]["head"].values())
    min_score = float('inf')
    worst_move = None

    # Check each possible move (up, down, left, right)
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_x, next_y = head_x + dx, head_y + dy
        if is_valid_move(game_state, next_x, next_y):
            total_valid_moves.append((next_x, next_y))
            # Calculate the flood-fill score for the connected region from the potential move
            floodfill_score = calculate_flood_fill_score((next_x, next_y), game_state)
            print("Floodfill Score:", floodfill_score)

            # Check if the flood-fill score is below the specified threshold
            if floodfill_score < threshold:
                invalid_moves.append((next_x, next_y))

                # Keep track of the move with the maximum flood-fill score
                if floodfill_score < min_score:
                    min_score = floodfill_score
                    worst_move = (next_x, next_y)

    # We only have one move left
    if invalid_moves == total_valid_moves and len(invalid_moves) == 1:
        invalid_moves = []
    
    if len(invalid_moves) > 0:
            invalid_moves = [worst_move]    

    print("Valid Moves:", total_valid_moves)
    print("Invalid Moves:", invalid_moves)
    return invalid_moves