import heapq

# Manhattan distance heuristic (Distance formula)
def heuristic_cost_estimate(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

# A* Algorithm implementation
def a_star_search(game_state, start, goal):
    rows, cols = game_state["board"]["height"], game_state["board"]["width"]
    open_set = [(0, start)]  # Priority queue for nodes to be evaluated: (f_score, node)
    came_from = {}  # Dictionary to store the parent node of each node
    g_score = {start: 0}  # Cost from start to current node
    f_score = {start: heuristic_cost_estimate(start, goal)}  # Estimated total cost from start to goal through current node

    while open_set:
        # Pop the node with the lowest f_score from the priority queue
        current_f_score, current_node = heapq.heappop(open_set)

        if current_node == goal:
            # Reconstruct the path if goal is reached
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            return path[::-1]  # Return the reversed path from start to goal

        # Generate neighbors (adjacent cells) of the current node
        for neighbor in [(current_node[0] + 1, current_node[1]), (current_node[0] - 1, current_node[1]), (current_node[0], current_node[1] + 1), (current_node[0], current_node[1] - 1)]:
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                tentative_g_score = g_score[current_node] + 1  # Assuming each step has a cost of 1

                # Check if the neighbor is a better path
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Update the values for this neighbor
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic_cost_estimate(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))  # Add the neighbor to the priority queue

    return None  # If the loop completes without reaching the goal, there is no path
