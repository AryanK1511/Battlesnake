from algorithms import a_star_algorithm, floodfill_algorithm

# ===== FOOD SEEKING LOGIC =====
def search_for_food_and_move(game_state, is_move_safe, best_moves_for_food):
    my_head = game_state["you"]["body"][0]  
    food = game_state['board']['food']

    # Check if there's food available on the board
    if food:
        # Finding the invalid moves using floodfill
        # This is done so that we do not get ourselves into situations where we are trapped
        moves = floodfill_algorithm.find_invalid_moves_using_floodfill(game_state, 30)
        # If there are invalid moves, we follow floodfill
        if len(moves) > 0:
            for move in moves:
                if move[0] < my_head['x']:
                    is_move_safe["right"] = True
                    is_move_safe["left"] = False
                    is_move_safe["up"] = True
                    is_move_safe["down"] = True
                elif move[0] > my_head['x']:
                    is_move_safe["right"] = False
                    is_move_safe["left"] = True
                    is_move_safe["up"] = True
                    is_move_safe["down"] = True
                elif move[1] < my_head['y']:
                    is_move_safe["right"] = True
                    is_move_safe["left"] = True
                    is_move_safe["up"] = True
                    is_move_safe["down"] = False
                elif move[1] > my_head['y']:
                    is_move_safe["right"] = True
                    is_move_safe["left"] = True
                    is_move_safe["up"] = False
                    is_move_safe["down"] = True
        # If there are no invalid moves, we use A* algorithm
        else:
            # Find the closest food
            closest_food = min(food, key=lambda f: abs(f['x'] - my_head['x']) + abs(f['y'] - my_head['y']))
            path_to_food = a_star_algorithm.a_star_search(game_state, tuple(my_head.values()), tuple(closest_food.values()))
            print(path_to_food)
            # Move towards the closest food
            if path_to_food and len(path_to_food) > 1:
                next_move = path_to_food[1]
                # Flood fill and check if the length is more than 15
                if next_move[0] < my_head['x']:
                    is_move_safe["left"] = True
                    best_moves_for_food.append("left")
                elif next_move[0] > my_head['x']:
                    is_move_safe["right"] = True
                    best_moves_for_food.append("right")
                elif next_move[1] < my_head['y']:
                    is_move_safe["down"] = True
                    best_moves_for_food.append("down")
                elif next_move[1] > my_head['y']:
                    is_move_safe["up"] = True
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
    for snake in game_state["board"]["snakes"]:
        for body_part in snake["body"]:
            # To prevent horizontal collsions
            if body_part["x"] == my_head["x"] - 1 and body_part["y"] == my_head["y"]:
                is_move_safe["left"] = False
            if body_part["x"] == my_head["x"] + 1 and body_part["y"] == my_head["y"]:
                is_move_safe["right"] = False
            # To prevent vertical collisions
            if body_part["y"] == my_head["y"] + 1 and body_part["x"] == my_head["x"]:
                is_move_safe["up"] = False
            if body_part["y"] == my_head["y"] - 1 and body_part["x"] == my_head["x"]:
                is_move_safe["down"] = False

    return is_move_safe

# ===== STOPS SNAKE ENTERING A POTENTIAL HEAD ON IF IT IS SMALLER =====
def prevent_head_on_collisions_if_smaller(game_state, is_move_safe):
    my_head = game_state["you"]["body"][0]  
    possible_moves_for_my_snake = []
    safe_moves = [move for move, isSafe in is_move_safe.items() if isSafe]
    for safe_move in safe_moves:
        if safe_move == "up":
            possible_moves_for_my_snake.append([my_head["x"], my_head["y"] + 1])
        elif safe_move == "down":
            possible_moves_for_my_snake.append([my_head["x"], my_head["y"] - 1])
        elif safe_move == "left":
            possible_moves_for_my_snake.append([my_head["x"] - 1, my_head["y"]])
        elif safe_move == "right":
            possible_moves_for_my_snake.append([my_head["x"] + 1, my_head["y"]])

    for snake in game_state["board"]["snakes"][1:]:
        if snake["length"] >= game_state["you"]["length"]:
            head_positions = [[snake["head"]["x"] + 1, snake["head"]["y"]], [snake["head"]["x"] - 1, snake["head"]["y"]], [snake["head"]["x"], snake["head"]["y"] + 1], [snake["head"]["x"], snake["head"]["y"] - 1]]
            for head_position in head_positions:
                if head_position in possible_moves_for_my_snake:
                    # Determine the direction of the collision and update is_move_safe accordingly
                    if head_position[0] < my_head["x"] and len(safe_moves) > 1 and (head_position[1] == my_head["y"] or head_position[1] == my_head["y"] - 1 or head_position[1] == my_head["y"] + 1):
                        is_move_safe["left"] = False
                    if head_position[0] > my_head["x"] and len(safe_moves) > 1 and (head_position[1] == my_head["y"] or head_position[1] == my_head["y"] - 1 or head_position[1] == my_head["y"] + 1):
                        is_move_safe["right"] = False
                    if head_position[1] > my_head["y"] and len(safe_moves) > 1 and (head_position[0] == my_head["x"] or head_position[0] == my_head["x"] - 1 or head_position[0] == my_head["x"] + 1):
                        is_move_safe["up"] = False
                    if head_position[1] < my_head["y"] and len(safe_moves) > 1 and (head_position[0] == my_head["x"] or head_position[0] == my_head["x"] - 1 or head_position[0] == my_head["x"] + 1):
                        is_move_safe["down"] = False
                safe_moves = [move for move, isSafe in is_move_safe.items() if isSafe]

    return is_move_safe