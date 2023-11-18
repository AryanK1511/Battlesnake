d = {'game': {'id': '76fe47b8-5c48-44fc-95ab-fa98acafcb90', 'ruleset': {'name': 'standard', 'version': 'v1.2.3', 'settings': {'foodSpawnChance': 15, 'minimumFood': 1, 'hazardDamagePerTurn': 0, 'hazardMap': '', 'hazardMapAuthor': '', 'royale': {'shrinkEveryNTurns': 0}, 'squad': {'allowBodyCollisions': False, 'sharedElimination': False, 'sharedHealth': False, 'sharedLength': False}}}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 42, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_7mM66bpPtWwDRmwxwMW8pxTQ', 'name': "Aryan's Academic Weapon", 'latency': '8', 'health': 58, 'body': [{'x': 10, 'y': 0}, {'x': 10, 'y': 1}, {'x': 10, 'y': 2}], 'head': {'x': 10, 'y': 0}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#fdac53', 'head': 'smart-caterpillar', 'tail': 'coffee'}}, {'id': 'gs_SyqXqtxBBqbpd6KwdFbxXqm7', 'name': 'Scared Bot', 'latency': '1', 'health': 98, 'body': [{'x': 10, 'y': 10}, {'x': 9, 'y': 10}, {'x': 8, 'y': 10}, {'x': 8, 'y': 9}, {'x': 9, 'y': 9}], 'head': {'x': 10, 'y': 10}, 'length': 5, 'shout': '', 'squad': '', 'customizations': {'color': '#000000', 'head': 'bendr', 'tail': 'curled'}}, {'id': 'gs_mDFRWjrwpDHwSPDbkTvcM3wS', 'name': 'Loopy Bot', 'latency': '1', 'health': 60, 'body': [{'x': 0, 'y': 8}, {'x': 0, 'y': 9}, {'x': 1, 'y': 9}, {'x': 1, 'y': 8}], 'head': {'x': 0, 'y': 8}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#800080', 'head': 'caffeine', 'tail': 'iguana'}}], 'food': [{'x': 0, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 4}, {'x': 0, 'y': 0}, {'x': 4, 'y': 6}], 'hazards': []}, 'you': {'id': 'gs_7mM66bpPtWwDRmwxwMW8pxTQ', 'name': "Aryan's Academic Weapon", 'latency': '8', 'health': 58, 'body': [{'x': 10, 'y': 0}, {'x': 10, 'y': 1}, {'x': 10, 'y': 2}], 'head': {'x': 10, 'y': 0}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#fdac53', 'head': 'smart-caterpillar', 'tail': 'coffee'}}}

print(d["board"]["food"])

def heuristic(f):
    return abs(f['x'] - my_head['x']) + abs(f['y'] - my_head['y'])

# Example usage:
food = [{'x': 3, 'y': 5}, {'x': 1, 'y': 2}, {'x': 6, 'y': 8}]
my_head = {'x': 4, 'y': 3}

heuristic_values = [heuristic(f) for f in food]
print(heuristic_values)