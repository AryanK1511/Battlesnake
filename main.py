import random
import typing

def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "AryanK1511",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")

# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    print(game_state)

    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }

    # Prevent battlesnake from going backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    # Update the following lines
    if my_head["x"] <= 0:  # Head is at the left boundary, don't move left
        is_move_safe["left"] = False
    elif my_head["x"] >= board_width - 1:  # Head is at the right boundary, don't move right
        is_move_safe["right"] = False
    elif my_head["y"] <= 0:  # Head is at the top boundary, don't move up
        is_move_safe["down"] = False
    elif my_head["y"] >= board_height - 1:  # Head is at the bottom boundary, don't move down
        is_move_safe["up"] = False


    # Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']

    # for segment in my_body[1:]:  # Start from the second segment to avoid the head
    #     if my_head["x"] == segment["x"] and my_head["y"] == segment["y"]:
    #         # The head will collide with the body, mark the corresponding move as unsafe
    #         is_move_safe["up"] = False
    #         is_move_safe["down"] = False
    #         is_move_safe["left"] = False
    #         is_move_safe["right"] = False
    #         break


    # Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']

    # Update the following lines
    # for snake in opponents:
    #     for segment in snake['body']:
    #         if my_head["x"] == segment["x"] and my_head["y"] == segment["y"]:
    #             # The head will collide with the other snake's body, mark the corresponding move as unsafe
    #             is_move_safe["up"] = False
    #             is_move_safe["down"] = False
    #             is_move_safe["left"] = False
    #             is_move_safe["right"] = False
    #             break


    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })