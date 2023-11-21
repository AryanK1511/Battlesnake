# my_head = game_state["you"]["body"][0]  
    # for snake in game_state["board"]["snakes"]:
    #     for body_part in snake["body"]:
    #         # To prevent horizontal collsions
    #         if (body_part["x"] == my_head["x"] - 1 and body_part["y"] == my_head["y"]):
    #             return False
    #         if (body_part["x"] == my_head["x"] + 1 and body_part["y"] == my_head["y"]):
    #             return False
    #         if (body_part["y"] == my_head["y"] + 1 and body_part["x"] == my_head["x"]):
    #             return False
    #         if (body_part["y"] == my_head["y"] - 1 and body_part["x"] == my_head["x"]):
    #             return False