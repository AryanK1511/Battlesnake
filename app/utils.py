from algorithms import a_star_algorithm

# ===== FOOD SEEKING LOGIC =====
def search_for_food_and_move(game_state, is_move_safe, best_moves_for_food):
    my_head = game_state["you"]["body"][0]  
    # Check if there's food available on the board
    food = game_state['board']['food']
    if food:
        # Find the closest food
        closest_food = min(food, key=lambda f: abs(f['x'] - my_head['x']) + abs(f['y'] - my_head['y']))
        path_to_food = a_star_algorithm.a_star_search(game_state, tuple(my_head.values()), tuple(closest_food.values()))
        print(path_to_food)

        # Move towards the closest food
        if path_to_food and len(path_to_food) > 1:
            next_move = path_to_food[1]
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

# ===== STOPS SNAKE FROM MOVING BACKWARDS =====
def prevent_backward_movement(game_state, is_move_safe):
    # Coordinates of your "head" and "neck"
    my_head = game_state["you"]["body"][0]  
    my_neck = game_state["you"]["body"][1]  
    # Neck is left of head, don't move left
    if my_neck["x"] < my_head["x"]:  
        is_move_safe["left"] = False
    # Neck is right of head, don't move right
    elif my_neck["x"] > my_head["x"]:  
        is_move_safe["right"] = False
    # Neck is below head, don't move down
    elif my_neck["y"] < my_head["y"]:  
        is_move_safe["down"] = False
    # Neck is above head, don't move up
    elif my_neck["y"] > my_head["y"]:  
        is_move_safe["up"] = False

    return is_move_safe

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