from app import snake_logic

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": snake_logic.info, "start": snake_logic.start, "move": snake_logic.move, "end": snake_logic.end})