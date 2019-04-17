import sys
import math
import copy
import pprint
import heapq


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

def graph_search(start, fringe_tree) returns solution or failure
    closed = HASHSET_OF_VISITED_PLACES
    fringe = insert(create_node(initial_state[start]), fringe)
    while True:
        if fringe is empty return failure
        node = remove_front(fringe)
        if goal_test(start, state[node]) then return solution(node)
        if state[node] is not in closed
            closed[node] = state[node]
            fringe = insert_all(expand(node, start), fringe)
 """
def astar(start, goal):

    def heuristic(s, goal):
        animals_to_move = 0
        chickens = abs(s["left"]["chickens"] - goal["left"]["chickens"])
        wolves = abs(s["left"]["wolves"] - goal["left"]["wolves"])
        animals_to_move = (chickens + wolves) - (abs(chickens - wolves))
        if(animals_to_move > 2):
            animals_to_move *= 3
        return animals_to_move  # Divide by two, because we can move two animals per step

    closed_set = {}
    closed_set[state_to_dict_key(start)] = None
    open_set = []  # This will be a priority queue.
    heapq.heappush(open_set, (0, state_to_dict_key(start)))

    going_score = {state_to_dict_key(start): 0}
    counter = 0
    while len(open_set) > 0:
        (x, current) = heapq.heappop(open_set)
        current = dict_key_to_state(current)
        counter += 1
        if state_to_dict_key(current) == state_to_dict_key(goal):
            print("Goal found")
            path = []
            while closed_set.get(state_to_dict_key(current)) != None:
                path.insert(0, current)
                current = closed_set[state_to_dict_key(current)]
            path.insert(0, start)
            return counter, path


        for successor in successors(current):
            score = going_score[state_to_dict_key(current)] + 1
            if state_to_dict_key(successor) in closed_set and going_score[state_to_dict_key(successor)] <= score:
                continue

            if (x, successor) not in open_set:
                heapq.heappush(
                    open_set, (score  + heuristic(successor, goal), state_to_dict_key(successor)))
                closed_set[state_to_dict_key(successor)] = current
                going_score[state_to_dict_key(successor)] = score


def bfs(start, goal):
    closed = {}
    fringe = [start]
    closed[state_to_dict_key(start)] = None
    counter = 0
    while True:
        if len(fringe) == 0:
            return math.inf, ["We failed, chief"]
        state = fringe.pop(0)

        # print("[{}] State".format(counter), state)
        counter += 1

        if state_to_dict_key(state) == state_to_dict_key(goal):
            path = []
            while closed.get(state_to_dict_key(state)) != None:
                path.insert(0, state)
                state = closed[state_to_dict_key(state)]
            path.insert(0, start)
            return counter, path

        # print("exploring " + state_to_dict_key(state))

        for successor in successors(state):
            if state_to_dict_key(successor) not in closed:
                fringe.append(successor)
                closed[state_to_dict_key(successor)] = state


def dls(start, goal, depth):
    closed = {
        state_to_dict_key(start): (0, None)
    }
    fringe = [(0, start)]
    counter = 0
    while True:
        if len(fringe) == 0:
            return math.inf, ["We failed, chief"]
        completeState = fringe.pop(len(fringe) - 1)
        curDepth = completeState[0]
        state = completeState[1]
        if(curDepth > depth):
            continue

        # print("[{}] State".format(counter), state)
        counter += 1

        if state_to_dict_key(state) == state_to_dict_key(goal):
            path = []
            while closed.get(state_to_dict_key(state))[1] != None:
                path.insert(0, state)
                completeState = closed[state_to_dict_key(state)]
                depth = completeState[0]
                state = completeState[1]
            path.insert(0, start)
            return counter, path

        for successor in successors(state):
            if state_to_dict_key(successor) not in closed or closed[state_to_dict_key(successor)][0] > curDepth:
                fringe.append((curDepth+1, successor))
                closed[state_to_dict_key(successor)] = (curDepth + 1, state)


def iddfs(start, goal):
    depth = 0
    while(True):
        counter, path = dls(start, goal, depth)
        if(counter == math.inf):
            depth = depth+1
            print(depth)
        else:
            return counter, path


def dfs(start, goal):
    closed = {}
    closed[state_to_dict_key(start)] = None
    fringe = [start]
    counter = 0
    while True:
        if len(fringe) == 0:
            return math.inf, ["We failed, chief"]
        state = fringe.pop(len(fringe) - 1)

        # print("[{}] State".format(counter), state)
        counter += 1

        if state_to_dict_key(state) == state_to_dict_key(goal):
            path = []
            while closed.get(state_to_dict_key(state)) != None:
                path.insert(0, state)
                state = closed[state_to_dict_key(state)]
            path.insert(0, start)
            return counter, path

        # print("exploring " + state_to_dict_key(state))

        for successor in successors(state):
            if state_to_dict_key(successor) not in closed:
                fringe.append(successor)
                closed[state_to_dict_key(successor)] = state


def state_to_dict_key(state):
    return "{},{},{}\n{},{},{}".format(
        state["left"]["chickens"],
        state["left"]["wolves"],
        1 if state["left"]["boat"] else 0,
        state["right"]["chickens"],
        state["right"]["wolves"],
        1 if state["right"]["boat"] else 0,
    )


def dict_key_to_state(dict_key):
    values = dict_key.replace("\n", ",")
    values = values.split(",")
    dictReturn =  {}
    data = {
            "left": {
                "chickens": int(values[0]),
                "wolves": int(values[1]),
                "boat": int(values[2]),
            },
            "right": {
                "chickens": int(values[3]),
                "wolves": int(values[4]),
                "boat": int(values[5]),
            }
        }
    return data
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

    for i in range(1, 3):
        if s[side]["chickens"] < i:
            break
        this_data = copy.deepcopy(entry)

        this_data[side]["chickens"] = s[side]["chickens"] - i
        this_data[other_side]["chickens"] = s[other_side]["chickens"] + i

        # This just copies the data, it doesn't need to modify it
        this_data[side]["wolves"] = s[side]["wolves"]
        this_data[other_side]["wolves"] = s[other_side]["wolves"]

        data.append(this_data)

    if s[side]["wolves"] >= 1:
        # One wolf
        this_data = copy.deepcopy(entry)
        this_data[side]["wolves"] = s[side]["wolves"] - 1
        this_data[other_side]["wolves"] = s[other_side]["wolves"] + 1

        # This just copies the data, it doesn't need to modify it
        this_data[side]["chickens"] = s[side]["chickens"]
        this_data[other_side]["chickens"] = s[other_side]["chickens"]

        data.append(this_data)

    if s[side]["chickens"] > 0 and s[side]["wolves"] > 0:
        this_data = copy.deepcopy(entry)

        this_data[side]["chickens"] = s[side]["chickens"] - 1
        this_data[other_side]["chickens"] = s[other_side]["chickens"] + 1
        this_data[side]["wolves"] = s[side]["wolves"] - 1
        this_data[other_side]["wolves"] = s[other_side]["wolves"] + 1

        data.append(this_data)

    if s[side]["wolves"] >= 2:
        # Two wolves
        this_data = copy.deepcopy(entry)
        this_data[side]["wolves"] = s[side]["wolves"] - 2
        this_data[other_side]["wolves"] = s[other_side]["wolves"] + 2

        # This just copies the data, it doesn't need to modify it
        this_data[side]["chickens"] = s[side]["chickens"]
        this_data[other_side]["chickens"] = s[other_side]["chickens"]

        data.append(this_data)

    filtered = []
    for entry in data:
        if (entry["left"]["wolves"] <= entry["left"]["chickens"] or entry["left"]["chickens"] == 0) and (entry["right"]["wolves"] <= entry["right"]["chickens"] or entry["right"]["chickens"] == 0):
            filtered.append(entry)

    return filtered


def step_string(state, other):
    chicken_difference = abs(
        state["left"]["chickens"] - other["left"]["chickens"])
    wolf_difference = abs(
        state["left"]["wolves"] - other["left"]["wolves"])

    return_string = "{:<8}".format("[{}]".format(
        "Left" if state["left"]["boat"] else "Right"))
    if chicken_difference != 0 and wolf_difference != 0:
        return_string += "Put {} chicken and {} wolf on the boat.".format(
            chicken_difference, wolf_difference)
    elif wolf_difference != 0:
        return_string += "Put {} {} on the boat.".format(
            wolf_difference, "wolf" if wolf_difference == 1 else "wolves")
    elif chicken_difference != 0:
        return_string += "Put {} {} on the boat.".format(
            chicken_difference, "chicken" if chicken_difference == 1 else "chickens")
    else:
        return_string += "Two identical states were passed to this function."

    return return_string


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
    elif mode == "iddfs":
        counter, path = iddfs(data, goal)
    elif mode == "astar":
        counter, path = astar(data, goal)

    import os
    with open(output, "w") as f:
        for node in range(len(path) - 1):
            f.write("{}\n".format(step_string(path[node], path[node + 1])))
    print("Path generated in {} steps".format(counter))
