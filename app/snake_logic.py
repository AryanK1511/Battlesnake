import random
import typing
from .utils import attack_smaller_and_attack_larger, search_for_food_and_move, prevent_backward_movement, prevent_out_of_bounds_movement, prevent_collisions

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

    # ===== ATTACK SMALLER SNAKES AND AVOID LARGER ONES =====
    is_move_safe = attack_smaller_and_attack_larger(game_state, is_move_safe)
    
    # ===== FOOD SEEKING LOGIC =====
    is_move_safe, best_moves_for_food = search_for_food_and_move(game_state, is_move_safe, best_moves_for_food)

    # ===== STOPS SNAKE FROM MOVING BACKWARDS =====
    is_move_safe = prevent_backward_movement(game_state, is_move_safe)

    # ===== STOPS SNAKE FROM GOING OUT OF BOUNDS =====
    is_move_safe = prevent_out_of_bounds_movement(game_state, is_move_safe)
    

    # ===== STOPS SNAKE FROM COLLIDING WITH OTHER SNAKES AND ITSELF =====
    is_move_safe = prevent_collisions(game_state, is_move_safe)

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

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}