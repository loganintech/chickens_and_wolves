import sys
import math
import copy
import pprint

def load(path):

    with open(path, "r") as f:
        left = f.readline().strip().split(',')
        right = f.readline().strip().split(",")

        data = {
            "left": {
                "chickens": int(left[0]),
                "wolves": int(left[1]),
                "boat": left[2] == "1",
            },
            "right": {
                "chickens": int(right[0]),
                "wolves": int(right[1]),
                "boat": right[2] == "1",
            }
        }

        return data

"""
GRAPH SEARCH Pseudocode

def graph_search(problem, fringe_tree) returns solution or failure
    closed = HASHSET_OF_VISITED_PLACES
    fringe = insert(create_node(initial_state[problem]), fringe)
    while True:
        if fringe is empty return failure
        node = remove_front(fringe)
        if goal_test(problem, state[node]) then return solution(node)
        if state[node] is not in closed
            closed[node] = state[node]
            fringe = insert_all(expand(node, problem), fringe)
 """

def bfs(problem, goal):
    closed = {}
    fringe = [[problem]]
    counter = 0
    while True:
        if len(fringe) == 0:
            return math.inf, ["We failed, chief"]
        path = fringe.pop(0)
        state = path[-1]

        # print("[{}] State".format(counter), state)
        counter+=1

        if state_to_dict_key(state) == state_to_dict_key(goal):
            return counter, path

        if state_to_dict_key(state) not in closed:
            for successor in successors(state):
                new_path = copy.deepcopy(path)
                new_path.append(successor)
                fringe.append(new_path)
            closed[state_to_dict_key(state)] = state


def dfs(problem, goal):
    closed = {}
    fringe = [[problem]]
    counter = 0
    while True:
        if len(fringe) == 0:
            return math.inf, ["We failed, chief"]
        path = fringe.pop(len(fringe) - 1)
        state = path[-1]

        # print("[{}] State".format(counter), state)
        counter += 1

        if state_to_dict_key(state) == state_to_dict_key(goal):
            return counter, path

        if state_to_dict_key(state) not in closed:
            for successor in successors(state):
                new_path = copy.deepcopy(path)
                new_path.append(successor)
                fringe.append(new_path)
            closed[state_to_dict_key(state)] = state

def state_to_dict_key(state):
    return "{},{},{}\n{},{},{}".format(
            state["left"]["chickens"],
            state["left"]["wolves"],
            1 if state["left"]["boat"] else 0,
            state["right"]["chickens"],
            state["right"]["wolves"],
            1 if state["right"]["boat"] else 0,
        )

def successors(s):
    data = []
    side = "left" if s["left"]["boat"] else "right"
    other_side = "right" if s["left"]["boat"] else "left"
    entry = {
        "left":  {
            "boat": not s["left"]["boat"],
        },
        "right": {
            "boat": not s["right"]["boat"],
        }
    }

    animals = ["chickens", "wolves"]
    for animal in range(len(animals)):
        for i in range(s[side][animals[animal]] + 1):
            if i < 1: continue
            if i > 2: break
            this_data = copy.deepcopy(entry)

            this_data[side][animals[animal]] = s[side][animals[animal]] - i
            this_data[other_side][animals[animal]] = s[other_side][animals[animal]] + i

            # This just copies the data, it doesn't need to modify it
            this_data[side][animals[animal ^ 1]] = s[side][animals[animal ^ 1]]
            this_data[other_side][animals[animal ^ 1]] = s[other_side][animals[animal ^ 1]]

            data.append(this_data)


    if s[side]["chickens"] > 0 and s[side]["wolves"] > 0:
        this_data = copy.deepcopy(entry)

        this_data[side]["chickens"] = s[side]["chickens"] - 1
        this_data[other_side]["chickens"] = s[other_side]["chickens"] + 1
        this_data[side]["wolves"] = s[side]["wolves"] - 1
        this_data[other_side]["wolves"] = s[other_side]["wolves"] + 1

        data.append(this_data)


    filtered = []
    for entry in data:
        if (entry["left"]["wolves"] <= entry["left"]["chickens"] or entry["left"]["chickens"] == 0) and (entry["right"]["wolves"] <= entry["right"]["chickens"] or entry["right"]["chickens"] == 0):
            filtered.append(entry)

    return filtered

if __name__ == "__main__":
    args = sys.argv
    data = load(args[1])
    goal = load(args[2])
    mode = args[3]
    output = args[4]

    counter, path = 0, []
    if mode == "bfs":
        counter, path = bfs(data, goal)
    elif mode == "dfs":
        counter, path = dfs(data, goal)

    for node in path:
        print(node)
    print("Path generated in {} steps".format(counter))
