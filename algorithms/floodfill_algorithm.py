# The 'visited' cells will be updated in the grid
# print(grid)
grid = {'game': {'id': '1b65d9ab-efba-40d7-9cfe-61050f81494c', 'ruleset': {'name': 'standard', 'version': 'v1.2.3', 'settings': {'foodSpawnChance': 15, 'minimumFood': 1, 'hazardDamagePerTurn': 0, 'hazardMap': '', 'hazardMapAuthor': '', 'royale': {'shrinkEveryNTurns': 0}, 'squad': {'allowBodyCollisions': False, 'sharedElimination': False, 'sharedHealth': False, 'sharedLength': False}}}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 60, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_48pTX7y3mpSjhKqWVb37BTWd', 'name': 'That one asian kid in class', 'latency': '173', 'health': 97, 'body': [{'x': 8, 'y': 8}, {'x': 8, 'y': 9}, {'x': 7, 'y': 9}, {'x': 6, 'y': 9}, {'x': 5, 'y': 9}, {'x': 5, 'y': 8}, {'x': 5, 'y': 7}, {'x': 6, 'y': 7}, {'x': 7, 'y': 7}, {'x': 8, 'y': 7}, {'x': 9, 'y': 7}, {'x': 9, 'y': 6}, {'x': 9, 'y': 5}, {'x': 9, 'y': 4}], 'head': {'x': 8, 'y': 8}, 'length': 14, 'shout': '', 'squad': '', 'customizations': {'color': '#fdac53', 'head': 'smart-caterpillar', 'tail': 'coffee'}}], 'food': [{'x': 0, 'y': 6}, {'x': 2, 'y': 10}, {'x': 0, 'y': 2}], 'hazards': []}, 'you': {'id': 'gs_48pTX7y3mpSjhKqWVb37BTWd', 'name': 'That one asian kid in class', 'latency': '173', 'health': 97, 'body': [{'x': 8, 'y': 8}, {'x': 8, 'y': 9}, {'x': 7, 'y': 9}, {'x': 6, 'y': 9}, {'x': 5, 'y': 9}, {'x': 5, 'y': 8}, {'x': 5, 'y': 7}, {'x': 6, 'y': 7}, {'x': 7, 'y': 7}, {'x': 8, 'y': 7}, {'x': 9, 'y': 7}, {'x': 9, 'y': 6}, {'x': 9, 'y': 5}, {'x': 9, 'y': 4}], 'head': {'x': 8, 'y': 8}, 'length': 14, 'shout': '', 'squad': '', 'customizations': {'color': '#fdac53', 'head': 'smart-caterpillar', 'tail': 'coffee'}}}


def calculate_flood_fill_score(start, game_state):
    visited = set()
    stack = [start]

    while stack:
        x, y = stack.pop()
        if (x, y) not in visited:
            visited.add((x, y))

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_x, next_y = x + dx, y + dy
                if is_valid_move(game_state, next_x, next_y):
                    stack.append((next_x, next_y))
    return len(visited)

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

def find_invalid_moves_using_floodfill(game_state, threshold):
    invalid_moves = []
    head_x, head_y = tuple(grid["you"]["head"].values())

    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_x, next_y = head_x + dx, head_y + dy
        if is_valid_move(game_state, next_x, next_y):
            floodfill_score = calculate_flood_fill_score((next_x, next_y), game_state)
            if floodfill_score < threshold:
                invalid_moves.append((next_x, next_y))
    print("IM:", invalid_moves)
    return invalid_moves

# Example data
vm = find_invalid_moves_using_floodfill(grid, 15)
