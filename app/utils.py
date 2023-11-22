from algorithms import a_star_algorithm, floodfill_algorithm

# ===== FOOD SEEKING AND SELF-LOOP PREVENTION LOGIC =====
def search_for_food_and_move(game_state, is_move_safe, best_moves_for_food):
    my_head = game_state["you"]["body"][0]  
    food = game_state['board']['food']

    # Check if there's food available on the board
    if food and len([move for move, isSafe in is_move_safe.items() if isSafe]) > 1:
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
    my_tail = game_state["you"]["body"][-1]
    for snake in game_state["board"]["snakes"]:
        for body_part in snake["body"]:
            # To prevent horizontal collsions
            if body_part["x"] == my_head["x"] - 1 and body_part["y"] == my_head["y"]:
                if body_part != my_tail: is_move_safe["left"] = False
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

    # Handling the base case where we could possibly collide with another snake in an H2H situation
    questionable_moves = {}
    is_move_safe_copy = is_move_safe.copy()
    for possible_move in possible_moves_for_our_snake:
        for snake in game_state["board"]["snakes"]:
            if snake != game_state["you"]:
                possible_moves_for_other_snake = [(snake["head"]["x"] - 1, snake["head"]["y"]), (snake["head"]["x"] + 1, snake["head"]["y"]), (snake["head"]["x"], snake["head"]["y"] - 1), (snake["head"]["x"], snake["head"]["y"] + 1)]
                if possible_moves_for_our_snake[possible_move] in possible_moves_for_other_snake and snake["length"] >= game_state["you"]["length"]:
                    print(is_move_safe[possible_move])
                    questionable_moves[possible_move] = snake["head"]
                    is_move_safe_copy[possible_move] = False

    for entry in is_move_safe_copy:
        if is_move_safe_copy[entry] == True:
            return is_move_safe_copy

    # This case is when we have no safe options and we need to predict the move of the other snake to make a decision
    for move in questionable_moves:
        head = questionable_moves[move].copy()
        closest_food = min(game_state["board"]["food"], key=lambda f: abs(f['x'] - head['x']) + abs(f['y'] - head['y']))
        path_to_food = a_star_algorithm.a_star_search(game_state, tuple(head.values()), tuple(closest_food.values()))
        
        if path_to_food and len(path_to_food) > 1:
            next_move = path_to_food[1]
            
            if next_move[0] < head['x']:
                head["x"] -= 1 # (4, 5)
            elif next_move[0] > head['x']:
                head["x"] += 1
            elif next_move[1] < head['y']:
                head["y"] -= 1
            elif next_move[1] > head['y']:
                head["y"] += 1
        
        if tuple([head["x"], head["y"]]) == possible_moves_for_our_snake[move]:
            is_move_safe[move] = False
    
    return is_move_safe