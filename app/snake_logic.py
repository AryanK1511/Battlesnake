import random
import typing
from .utils import search_for_food_and_move, prevent_out_of_bounds_movement, prevent_collisions

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
    # print(game_state)
    # Returning a dictionary at the end which tells the Battlesnake what direction to move
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    best_moves_for_food = []

    # Movement manipulators
    is_move_safe, best_moves_for_food = search_for_food_and_move(game_state, is_move_safe, best_moves_for_food)
    print("1" + str(is_move_safe))
    is_move_safe = prevent_out_of_bounds_movement(game_state, is_move_safe)
    print("2" + str(is_move_safe))
    is_move_safe = prevent_collisions(game_state, is_move_safe)
    print("3" + str(is_move_safe))
    print("BMFF: " + str(best_moves_for_food))

    # ===== CHECK FOR AVAILABLE SAFE MOVES =====
    safe_moves = [move for move, isSafe in is_move_safe.items() if isSafe]

    # Choose a random move from the safe ones
    if len(best_moves_for_food) > 0 and best_moves_for_food[0] in safe_moves:
        next_move = best_moves_for_food[0]
    else:
        if len(safe_moves) > 0:
            next_move = random.choice(safe_moves)
        else:
            print("No safe moves")
            next_move = "down"

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}