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

d1 = {'game': {'id': 'fdfe9726-8c46-433c-bfec-28d139052d8f', 'ruleset': {'name': 'standard', 'version': 'v1.2.3', 'settings': {'foodSpawnChance': 15, 'minimumFood': 1, 'hazardDamagePerTurn': 0, 'hazardMap': '', 'hazardMapAuthor': '', 'royale': {'shrinkEveryNTurns': 0}, 'squad': {'allowBodyCollisions': False, 'sharedElimination': False, 'sharedHealth': False, 'sharedLength': False}}}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 288, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_x3JRdhBCbSJqgmfJQjFbRp7b', 'name': 'Academic Weapon', 'latency': '163', 'health': 100, 'body': [{'x': 10, 'y': 2}, {'x': 9, 'y': 2}, {'x': 8, 'y': 2}, {'x': 7, 'y': 2}, {'x': 7, 'y': 1}, {'x': 6, 'y': 1}, {'x': 5, 'y': 1}, {'x': 4, 'y': 1}, {'x': 3, 'y': 1}, {'x': 3, 'y': 2}, {'x': 2, 'y': 2}, {'x': 1, 'y': 2}, {'x': 1, 'y': 1}, {'x': 1, 'y': 0}, {'x': 0, 'y': 0}, {'x': 0, 'y': 1}, {'x': 0, 'y': 2}, {'x': 0, 'y': 3}, {'x': 0, 'y': 4}, {'x': 1, 'y': 4}, {'x': 1, 'y': 3}, {'x': 2, 'y': 3}, {'x': 3, 'y': 3}, {'x': 4, 'y': 3}, {'x': 5, 'y': 3}, {'x': 6, 'y': 3}, {'x': 7, 'y': 3}, {'x': 7, 'y': 4}, {'x': 7, 'y': 5}, {'x': 7, 'y': 6}, {'x': 8, 'y': 6}, {'x': 8, 'y': 7}, {'x': 9, 'y': 7}, {'x': 9, 'y': 8}, {'x': 8, 'y': 8}, {'x': 8, 'y': 9}, {'x': 8, 'y': 10}, {'x': 8, 'y': 10}], 'head': {'x': 10, 'y': 2}, 'length': 38, 'shout': '', 'squad': '', 'customizations': {'color': '#fdac53', 'head': 'smart-caterpillar', 'tail': 'coffee'}}], 'food': [{'x': 1, 'y': 7}, {'x': 4, 'y': 7}], 'hazards': []}, 'you': {'id': 'gs_x3JRdhBCbSJqgmfJQjFbRp7b', 'name': 'Academic Weapon', 'latency': '163', 'health': 100, 'body': [{'x': 10, 'y': 2}, {'x': 9, 'y': 2}, {'x': 8, 'y': 2}, {'x': 7, 'y': 2}, {'x': 7, 'y': 1}, {'x': 6, 'y': 1}, {'x': 5, 'y': 1}, {'x': 4, 'y': 1}, {'x': 3, 'y': 1}, {'x': 3, 'y': 2}, {'x': 2, 'y': 2}, {'x': 1, 'y': 2}, {'x': 1, 'y': 1}, {'x': 1, 'y': 0}, {'x': 0, 'y': 0}, {'x': 0, 'y': 1}, {'x': 0, 'y': 2}, {'x': 0, 'y': 3}, {'x': 0, 'y': 4}, {'x': 1, 'y': 4}, {'x': 1, 'y': 3}, {'x': 2, 'y': 3}, {'x': 3, 'y': 3}, {'x': 4, 'y': 3}, {'x': 5, 'y': 3}, {'x': 6, 'y': 3}, {'x': 7, 'y': 3}, {'x': 7, 'y': 4}, {'x': 7, 'y': 5}, {'x': 7, 'y': 6}, {'x': 8, 'y': 6}, {'x': 8, 'y': 7}, {'x': 9, 'y': 7}, {'x': 9, 'y': 8}, {'x': 8, 'y': 8}, {'x': 8, 'y': 9}, {'x': 8, 'y': 10}, {'x': 8, 'y': 10}], 'head': {'x': 10, 'y': 2}, 'length': 38, 'shout': '', 'squad': '', 'customizations': {'color': '#fdac53', 'head': 'smart-caterpillar', 'tail': 'coffee'}}}

moves = find_invalid_moves_using_floodfill(d1, 30)
print(moves)