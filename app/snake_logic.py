import random
import typing
from .utils import search_for_food_and_move, prevent_out_of_bounds_movement, prevent_collisions, prevent_head_on_collision_if_smaller

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
    # Returning a dictionary at the end which tells the Battlesnake what direction to move
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    best_moves_using_a_star_or_floodfill = []

    # ========== Movement manipulators ========== 
    print("\n===========================================================================")
    is_move_safe = prevent_out_of_bounds_movement(game_state, is_move_safe)
    print("Safe moves after BOUNDARY PREVENTION CODE: " + str(is_move_safe))

    is_move_safe = prevent_collisions(game_state, is_move_safe)
    print("Safe moves after COLLISION PREVENTION CODE: " + str(is_move_safe))

    is_move_safe = prevent_head_on_collision_if_smaller(game_state, is_move_safe)
    print("Safe moves after HEAD-ON COLLISION PREVENTION CODE: " + str(is_move_safe))

    is_move_safe, best_moves_using_a_star_or_floodfill = search_for_food_and_move(game_state, is_move_safe, best_moves_using_a_star_or_floodfill)
    print("Safe moves after A* AND FLOODFILL" + str(is_move_safe))
    print("Best moves after A* AND FLOODFILL: " + str(best_moves_using_a_star_or_floodfill))
    print("===========================================================================")

    # ===== CHECK FOR AVAILABLE SAFE MOVES =====
    safe_moves = [move for move, isSafe in is_move_safe.items() if isSafe]

    # Choose a random move from the safe ones
    if len(best_moves_using_a_star_or_floodfill) > 0 and best_moves_using_a_star_or_floodfill[0] in safe_moves:
        next_move = best_moves_using_a_star_or_floodfill[0]
    else:
        if len(safe_moves) > 0:
            next_move = random.choice(safe_moves)
        else:
            print("No safe moves")
            next_move = "down"

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}