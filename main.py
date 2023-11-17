import random
import typing

# Called at battlesnake creation
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "AryanK1511", 
        "color": "#FDAC53",  
        "head": "smart-caterpillar",  
        "tail": "coffee"
    }

# Called when game begins
def start(game_state: typing.Dict):
    print("GAME START")

# Called when game finishes
def end(game_state: typing.Dict):
    print("GAME OVER\n")

# Called on every turn
def move(game_state: typing.Dict) -> typing.Dict:
    print(game_state)
    # Returning a dictionary at the end which tells the Battlesnake what direction to move
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    best_moves_for_food = []
    my_head = game_state["you"]["body"][0]  

    # ===== FOOD SEEKING LOGIC =====
    # Check if there's food available on the board
    food = game_state['board']['food']
    if food:
        # Find the closest food
        closest_food = min(food, key=lambda f: abs(f['x'] - my_head['x']) + abs(f['y'] - my_head['y']))

        # Move towards the closest food
        if closest_food['x'] < my_head['x']:
            is_move_safe["left"] = True
            best_moves_for_food.append("left")
        elif closest_food['x'] > my_head['x']:
            is_move_safe["right"] = True
            best_moves_for_food.append("right")
        elif closest_food['y'] < my_head['y']:
            is_move_safe["down"] = True
            best_moves_for_food.append("down")
        elif closest_food['y'] > my_head['y']:
            is_move_safe["up"] = True
            best_moves_for_food.append("up")

    # ===== STOPS SNAKE FROM MOVING BACKWARDS =====
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

    # ===== STOPS SNAKE FROM GOING OUT OF BOUNDS =====
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
        
    # ===== STOPS SNAKE FROM COLLIDING WITH OTHER SNAKES AND ITSELF =====
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
    
    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    if len(best_moves_for_food) > 0 and best_moves_for_food[0] in safe_moves:
        next_move = best_moves_for_food[0]
    else:
        next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})