from algorithms import a_star_algorithm, floodfill_algorithm

# Returns all the valid moves remaining
def validate_next_move(game_state, is_move_safe):
    is_move_safe = prevent_out_of_bounds_movement(game_state, is_move_safe)
    is_move_safe = prevent_collisions(game_state, is_move_safe)
    return is_move_safe

# Returns all the safe moves remaining as a list
def get_safe_moves(game_state, is_move_safe):
    safe_moves = [move for move, isSafe in is_move_safe.items() if isSafe]
    return safe_moves

# ===== FOOD SEEKING AND SELF-LOOP PREVENTION LOGIC =====
def search_for_food_and_move(game_state, is_move_safe, best_moves_for_food):
    my_head = game_state["you"]["body"][0]  
    food = game_state['board']['food']

    # Check if there's food available on the board
    if food:
        # Finding the invalid moves using floodfill
        # This is done so that we do not get ourselves into situations where we are trapped
        invalid_moves = floodfill_algorithm.find_invalid_moves_using_floodfill(game_state, 30)
        # If there are invalid moves, we follow floodfill
        if len(invalid_moves) > 0:
            if invalid_moves[0][0] < my_head['x']:
                is_move_safe["left"] = False
            elif invalid_moves[0][0] > my_head['x']:
                is_move_safe["right"] = False
            elif invalid_moves[0][1] < my_head['y']:
                is_move_safe["down"] = False
            elif invalid_moves[0][1] > my_head['y']:
                is_move_safe["up"] = False

        # After floodfill filters out the options, find the closest food using A* search so that we can go in that directioon
        closest_food = min(food, key=lambda f: abs(f['x'] - my_head['x']) + abs(f['y'] - my_head['y']))
        path_to_food = a_star_algorithm.a_star_search(game_state, tuple(my_head.values()), tuple(closest_food.values()))
        print("Path to food using A*: ", path_to_food)

        # Move towards the closest food
        if path_to_food and len(path_to_food) > 1:
            next_move = path_to_food[1]
            # Flood fill and check if the length is more than 15
            if next_move[0] < my_head['x']:
                best_moves_for_food.append("left")
            elif next_move[0] > my_head['x']:
                best_moves_for_food.append("right")
            elif next_move[1] < my_head['y']:
                best_moves_for_food.append("down")
            elif next_move[1] > my_head['y']:
                best_moves_for_food.append("up")

    return is_move_safe, best_moves_for_food

# ===== STOPS SNAKE FROM GOING OUT OF BOUNDS =====
def prevent_out_of_bounds_movement(game_state, is_move_safe):
    my_head = game_state["you"]["body"][0]  
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    # The snake does not go outside from left or right
    if my_head["x"] <= 0:
        is_move_safe["left"] = False
    if my_head["x"] >= board_width - 1:
        is_move_safe["right"] = False
    # The snake does not go outside from top or bottom
    if my_head["y"] <= 0:
        is_move_safe["down"] = False
    if my_head["y"] >= board_height - 1:
        is_move_safe["up"] = False

    return is_move_safe

# ===== STOPS SNAKE FROM COLLIDING WITH OTHER SNAKES AND ITSELF =====
def prevent_collisions(game_state, is_move_safe):
    print(game_state)
    my_head = game_state["you"]["body"][0]
    my_tail = game_state["you"]["body"][game_state["you"]["length"]-1]
    for snake in game_state["board"]["snakes"]:
        for body_part in snake["body"]:
            # To prevent horizontal collsions
            if body_part["x"] == my_head["x"] - 1 and body_part["y"] == my_head["y"]:
                if body_part != my_tail: is_move_safe["left"] = False # Don't update is_move_safe if it's our tail, as we can move to the cell where our tail is safely (it'll move forward)
            if body_part["x"] == my_head["x"] + 1 and body_part["y"] == my_head["y"]:
                if body_part != my_tail: is_move_safe["right"] = False
            # To prevent vertical collisions
            if body_part["y"] == my_head["y"] + 1 and body_part["x"] == my_head["x"]:
                if body_part != my_tail: is_move_safe["up"] = False
            if body_part["y"] == my_head["y"] - 1 and body_part["x"] == my_head["x"]:
                if body_part != my_tail: is_move_safe["down"] = False

    return is_move_safe

# ===== STOPS SNAKE ENTERING A POTENTIAL HEAD-ON COLLISION IF IT IS SMALLER =====
def prevent_head_on_collision_if_smaller(game_state, is_move_safe):
    possible_moves_for_our_snake = {"left": (game_state["you"]["body"][0]["x"] - 1, game_state["you"]["body"][0]["y"]), "right": (game_state["you"]["body"][0]["x"] + 1, game_state["you"]["body"][0]["y"]), "up": (game_state["you"]["body"][0]["x"], game_state["you"]["body"][0]["y"] + 1), "down": (game_state["you"]["body"][0]["x"], game_state["you"]["body"][0]["y"] - 1)}
    # if len(get_safe_moves(game_state, is_move_safe)) > 1:
    questionable_moves = {}
    for possible_move in possible_moves_for_our_snake:
        for snake in game_state["board"]["snakes"]:
            if snake != game_state["you"]:
                possible_moves_for_other_snake = [(snake["head"]["x"] - 1, snake["head"]["y"]), (snake["head"]["x"] + 1, snake["head"]["y"]), (snake["head"]["x"], snake["head"]["y"] - 1), (snake["head"]["x"], snake["head"]["y"] + 1)]
                if possible_moves_for_our_snake[possible_move] in possible_moves_for_other_snake and snake["length"] >= game_state["you"]["length"]:
                    print(is_move_safe[possible_move])
                    questionable_moves[possible_move] = snake["head"]
                    #is_move_safe[possible_move] = False

    for move in questionable_moves:
        head = questionable_moves[move]
        closest_food = min(food, key=lambda f: abs(f['x'] - head['x']) + abs(f['y'] - head['y']))
        path_to_food = a_star_algorithm.a_star_search(game_state, tuple(head.values()), tuple(closest_food.values()))
        
        if path_to_food and len(path_to_food) > 1:
            next_move = path_to_food[1]
            
            if next_move[0] < head['x']:
                head["x"] -= 1
            elif next_move[0] > head['x']:
                head["x"] += 1
            elif next_move[1] < head['y']:
                head["y"] -= 1
            elif next_move[1] > head['y']:
                head["y"] += 1
        
        if tuple(head["x"], head["y"]) == questionable_moves[move]:
            is_move_safe[move] = False
    
    return is_move_safe
    

# ===== TRAPS SNAKES SO THAT THEY SELF DESTRUCT =====
def trap_other_snakes(game_state, is_move_safe):
    return is_move_safe

# gs = {'game': {'id': '2283976e-a25d-4d1c-982d-52ddad11e7e5', 'ruleset': {'name': 'standard', 'version': 'v1.2.3', 'settings': {'foodSpawnChance': 15, 'minimumFood': 1, 'hazardDamagePerTurn': 0, 'hazardMap': '', 'hazardMapAuthor': '', 'royale': {'shrinkEveryNTurns': 0}, 'squad': {'allowBodyCollisions': False, 'sharedElimination': False, 'sharedHealth': False, 'sharedLength': False}}}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 8, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_67K8yJC9fHr4GxffgSgVWPGD', 'name': "The Coward's Hiraeth Rookie", 'latency': '13', 'health': 94, 'body': [{'x': 7, 'y': 5}, {'x': 8, 'y': 5}, {'x': 9, 'y': 5}, {'x': 10, 'y': 5}], 'head': {'x': 7, 'y': 5}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#ffd39b', 'head': 'tiger-king', 'tail': 'tiger-tail'}}, {'id': 'gs_7MdkX4myrTFk9TSrfJK6WmqK', 'name': 'Academic Weapon', 'latency': '171', 'health': 97, 'body': [{'x': 3, 'y': 5}, {'x': 3, 'y': 6}, {'x': 3, 'y': 7}, {'x': 3, 'y': 8}, {'x': 2, 'y': 8}], 'head': {'x': 3, 'y': 5}, 'length': 5, 'shout': '', 'squad': '', 'customizations': {'color': '#fdac53', 'head': 'smart-caterpillar', 'tail': 'coffee'}}, {'id': 'gs_VFFvpqJDTg3K9cJmHQkR7vJ4', 'name': "The Coward's Hiraeth Rookie", 'latency': '7', 'health': 94, 'body': [{'x': 4, 'y': 4}, {'x': 3, 'y': 4}, {'x': 2, 'y': 4}, {'x': 1, 'y': 4}], 'head': {'x': 4, 'y': 4}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#ffd39b', 'head': 'tiger-king', 'tail': 'tiger-tail'}}, {'id': 'gs_hx6GKchmVfXT8SWj9B8R8d3C', 'name': "The Coward's Hiraeth Rookie", 'latency': '18', 'health': 94, 'body': [{'x': 6, 'y': 6}, {'x': 6, 'y': 7}, {'x': 6, 'y': 8}, {'x': 6, 'y': 9}], 'head': {'x': 6, 'y': 6}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#ffd39b', 'head': 'tiger-king', 'tail': 'tiger-tail'}}], 'food': [{'x': 5, 'y': 5}], 'hazards': []}, 'you': {'id': 'gs_7MdkX4myrTFk9TSrfJK6WmqK', 'name': 'Academic Weapon', 'latency': '171', 'health': 97, 'body': [{'x': 3, 'y': 5}, {'x': 3, 'y': 6}, {'x': 3, 'y': 7}, {'x': 3, 'y': 8}, {'x': 2, 'y': 8}], 'head': {'x': 3, 'y': 5}, 'length': 5, 'shout': '', 'squad': '', 'customizations': {'color': '#fdac53', 'head': 'smart-caterpillar', 'tail': 'coffee'}}}

# print(prevent_head_on_collision_if_smaller(gs, {"up": False, "down": False, "left": True, "right": True}))

# gs = {'game': {'id': '44700371-cf33-43c0-bbb0-4ecaad8f3f06', 'ruleset': {'name': 'standard', 'version': 'v1.2.3', 'settings': {'foodSpawnChance': 15, 'minimumFood': 1, 'hazardDamagePerTurn': 0, 'hazardMap': '', 'hazardMapAuthor': '', 'royale': {'shrinkEveryNTurns': 0}, 'squad': {'allowBodyCollisions': False, 'sharedElimination': False, 'sharedHealth': False, 'sharedLength': False}}}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 10, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_dyXpwPXbYpfxJ8VCXcmxDpkb', 'name': 'Academic Weapon', 'latency': '167', 'health': 100, 'body': [{'x': 5, 'y': 5}, {'x': 5, 'y': 6}, {'x': 5, 'y': 7}, {'x': 6, 'y': 7}, {'x': 6, 'y': 7}], 'head': {'x': 5, 'y': 5}, 'length': 5, 'shout': '', 'squad': '', 'customizations': {'color': '#fdac53', 'head': 'smart-caterpillar', 'tail': 'coffee'}}, {'id': 'gs_MHfYYqSWxJTScj4pyrMYmGbd', 'name': 'CopyrightInfringement', 'latency': '103', 'health': 92, 'body': [{'x': 5, 'y': 3}, {'x': 5, 'y': 4}, {'x': 4, 'y': 4}, {'x': 3, 'y': 4}], 'head': {'x': 5, 'y': 3}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#888888', 'head': 'default', 'tail': 'default'}}, {'id': 'gs_793BDGKcvrG6bh3bQj84VqFD', 'name': 'Copyright Infringement', 'latency': '6', 'health': 92, 'body': [{'x': 3, 'y': 5}, {'x': 4, 'y': 5}, {'x': 4, 'y': 6}, {'x': 3, 'y': 6}], 'head': {'x': 3, 'y': 5}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#000000', 'head': 'rbc-bowler', 'tail': 'skinny'}}], 'food': [{'x': 1, 'y': 6}], 'hazards': []}, 'you': {'id': 'gs_dyXpwPXbYpfxJ8VCXcmxDpkb', 'name': 'Academic Weapon', 'latency': '167', 'health': 100, 'body': [{'x': 5, 'y': 5}, {'x': 5, 'y': 6}, {'x': 5, 'y': 7}, {'x': 6, 'y': 7}, {'x': 6, 'y': 7}], 'head': {'x': 5, 'y': 5}, 'length': 5, 'shout': '', 'squad': '', 'customizations': {'color': '#fdac53', 'head': 'smart-caterpillar', 'tail': 'coffee'}}}

# print(trap_other_snakes(gs, {"up": True, "down": False, "left": False, "right": True}))
# print({'left': (4, 3)}.keys() in ["left", "right"])
# print({'left': (4, 3)}.key())