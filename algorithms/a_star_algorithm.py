import heapq

# Manhattan distance heuristic (Distance formula)
def heuristic_cost_estimate(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def a_star_search(game_state, start, goal):
    rows, cols = game_state["board"]["height"], game_state["board"]["width"]
    open_set = [(0, start)]  # Priority queue for nodes to be evaluated: (f_score, node)
    came_from = {}  # Dictionary to store the parent node of each node
    g_score = {start: 0}  # Cost from start to current node
    f_score = {start: heuristic_cost_estimate(start, goal)}  # Estimated total cost from start to goal through current node

    while open_set:
        current_f_score, current_node = heapq.heappop(open_set)
        if current_node == goal:
            # Reconstruct the path if goal is reached
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            return path[::-1]

        # (current_node[0] + 1, current_node[1]) -> (x + 1, y) => Right
        # (current_node[0] - 1, current_node[1]) -> (x - 1, y) => Left
        # (current_node[0], current_node[1] + 1) -> (x, y + 1) => Up
        # (current_node[0], current_node[1] - 1) -> (x, y - 1) => Down
        for neighbor in [(current_node[0] + 1, current_node[1]), (current_node[0] - 1, current_node[1]), (current_node[0], current_node[1] + 1), (current_node[0], current_node[1] - 1)]:
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                tentative_g_score = g_score[current_node] + 1  # Assuming each step has a cost of 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Update the values for this neighbor
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic_cost_estimate(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # If the loop completes without reaching the goal, there is no path

# Example usage:
# matrix = {'game': {'id': '76fe47b8-5c48-44fc-95ab-fa98acafcb90', 'ruleset': {'name': 'standard', 'version': 'v1.2.3', 'settings': {'foodSpawnChance': 15, 'minimumFood': 1, 'hazardDamagePerTurn': 0, 'hazardMap': '', 'hazardMapAuthor': '', 'royale': {'shrinkEveryNTurns': 0}, 'squad': {'allowBodyCollisions': False, 'sharedElimination': False, 'sharedHealth': False, 'sharedLength': False}}}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 42, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_7mM66bpPtWwDRmwxwMW8pxTQ', 'name': "Aryan's Academic Weapon", 'latency': '8', 'health': 58, 'body': [{'x': 10, 'y': 0}, {'x': 10, 'y': 1}, {'x': 10, 'y': 2}], 'head': {'x': 10, 'y': 0}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#fdac53', 'head': 'smart-caterpillar', 'tail': 'coffee'}}, {'id': 'gs_SyqXqtxBBqbpd6KwdFbxXqm7', 'name': 'Scared Bot', 'latency': '1', 'health': 98, 'body': [{'x': 10, 'y': 10}, {'x': 9, 'y': 10}, {'x': 8, 'y': 10}, {'x': 8, 'y': 9}, {'x': 9, 'y': 9}], 'head': {'x': 10, 'y': 10}, 'length': 5, 'shout': '', 'squad': '', 'customizations': {'color': '#000000', 'head': 'bendr', 'tail': 'curled'}}, {'id': 'gs_mDFRWjrwpDHwSPDbkTvcM3wS', 'name': 'Loopy Bot', 'latency': '1', 'health': 60, 'body': [{'x': 0, 'y': 8}, {'x': 0, 'y': 9}, {'x': 1, 'y': 9}, {'x': 1, 'y': 8}], 'head': {'x': 0, 'y': 8}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#800080', 'head': 'caffeine', 'tail': 'iguana'}}], 'food': [{'x': 0, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 4}, {'x': 0, 'y': 0}, {'x': 4, 'y': 6}], 'hazards': []}, 'you': {'id': 'gs_7mM66bpPtWwDRmwxwMW8pxTQ', 'name': "Aryan's Academic Weapon", 'latency': '8', 'health': 58, 'body': [{'x': 10, 'y': 0}, {'x': 10, 'y': 1}, {'x': 10, 'y': 2}], 'head': {'x': 10, 'y': 0}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#fdac53', 'head': 'smart-caterpillar', 'tail': 'coffee'}}}

# start = (2, 2)
# goal = (2, 0)

# path = a_star_search(matrix, start, goal)
# print(path)