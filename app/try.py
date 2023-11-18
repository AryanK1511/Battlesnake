is_move_safe = {"up": True, "down": False, "left": True, "right": False}

safe_moves = [move for move, isSafe in is_move_safe.items() if isSafe]

print("Before: " + str(safe_moves))

game_state = {'game': {'id': '05dbd856-436e-441f-92d9-920849d96a26', 'ruleset': {'name': 'standard', 'version': 'v1.2.3', 'settings': {'foodSpawnChance': 15, 'minimumFood': 1, 'hazardDamagePerTurn': 0, 'hazardMap': '', 'hazardMapAuthor': '', 'royale': {'shrinkEveryNTurns': 0}, 'squad': {'allowBodyCollisions': False, 'sharedElimination': False, 'sharedHealth': False, 'sharedLength': False}}}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 38, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_78mvGqtyR7CGwWtRRC9qB7kP', 'name': 'That one asian kid in class', 'latency': '162', 'health': 85, 'body': [{'x': 3, 'y': 5}, {'x': 4, 'y': 5}, {'x': 5, 'y': 5}, {'x': 5, 'y': 4}, {'x': 4, 'y': 4}, {'x': 3, 'y': 4}, {'x': 3, 'y': 3}], 'head': {'x': 3, 'y': 5}, 'length': 7, 'shout': '', 'squad': '', 'customizations': {'color': '#fdac53', 'head': 'smart-caterpillar', 'tail': 'coffee'}}, {'id': 'gs_Fd9RhyTtY3QGyGQqdv8mfrFJ', 'name': 'bascilous-python', 'latency': '133', 'health': 87, 'body': [{'x': 1, 'y': 5}, {'x': 0, 'y': 5}, {'x': 0, 'y': 4}, {'x': 1, 'y': 4}, {'x': 1, 'y': 3}], 'head': {'x': 1, 'y': 5}, 'length': 5, 'shout': '', 'squad': '', 'customizations': {'color': '#ffffff', 'head': 'evil', 'tail': 'round-bum'}}], 'food': [{'x': 0, 'y': 8}, {'x': 0, 'y': 2}], 'hazards': []}, 'you': {'id': 'gs_78mvGqtyR7CGwWtRRC9qB7kP', 'name': 'That one asian kid in class', 'latency': '162', 'health': 85, 'body': [{'x': 3, 'y': 5}, {'x': 4, 'y': 5}, {'x': 5, 'y': 5}, {'x': 5, 'y': 4}, {'x': 4, 'y': 4}, {'x': 3, 'y': 4}, {'x': 3, 'y': 3}], 'head': {'x': 3, 'y': 5}, 'length': 7, 'shout': '', 'squad': '', 'customizations': {'color': '#fdac53', 'head': 'smart-caterpillar', 'tail': 'coffee'}}}

my_head = game_state["you"]["body"][0]  
possible_moves_for_my_snake = []
for safe_move in safe_moves:
    if safe_move == "up":
        possible_moves_for_my_snake.append([my_head["x"], my_head["y"] + 1])
    elif safe_move == "down":
        possible_moves_for_my_snake.append([my_head["x"], my_head["y"] - 1])
    elif safe_move == "left":
        possible_moves_for_my_snake.append([my_head["x"] - 1, my_head["y"]])
    elif safe_move == "right":
        possible_moves_for_my_snake.append([my_head["x"] + 1, my_head["y"]])
print(possible_moves_for_my_snake)
for snake in game_state["board"]["snakes"][1:]:
    # if snake["length"] >= game_state["you"]["length"]:
    head_positions = [[snake["head"]["x"] + 1, snake["head"]["y"]], [snake["head"]["x"] - 1, snake["head"]["y"]], [snake["head"]["x"], snake["head"]["y"] + 1], [snake["head"]["x"], snake["head"]["y"] - 1]]
    for head_position in head_positions:
        if head_position in possible_moves_for_my_snake:
            # Determine the direction of the collision and update is_move_safe accordingly
            if head_position[0] < my_head["x"] and len(safe_moves) > 1:
                is_move_safe["left"] = False
            if head_position[0] > my_head["x"] and len(safe_moves) > 1:
                is_move_safe["right"] = False
            if head_position[1] < my_head["y"] and len(safe_moves) > 1:
                is_move_safe["up"] = False
            if head_position[1] > my_head["y"] and len(safe_moves) > 1:
                is_move_safe["down"] = False
        safe_moves = [move for move, isSafe in is_move_safe.items() if isSafe]

print("After: " + str(safe_moves))