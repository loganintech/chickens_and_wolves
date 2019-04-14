import sys
import pprint
import copy

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
    closed = []
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
    fringe = [problem]

    while fringe:
        state = fringe.pop(0)

        for i in successor(state):
            print(i)

def successor(s):
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

    print("Start State")
    pprint.pprint(s)
    print("\n")

    animals = ["chickens", "wolves"]
    for animal in range(len(animals)):
        for i in range(s[side][animals[animal]] + 1):
            if i < 1 or i > 2: continue
            this_data = copy.deepcopy(entry)

            this_data[side][animals[animal]] = s[side][animals[animal]] - i
            this_data[other_side][animals[animal]] = s[other_side][animals[animal]] + i
            this_data[side][animals[animal ^ 1]] = s[side][animals[animal ^ 1]]
            this_data[other_side][animals[animal ^ 1]] = s[other_side][animals[animal ^ 1]]

            pprint.pprint(this_data)
            data.append(this_data)


    if s[side]["chickens"] > 0 and s[side]["wolves"] > 0:
        this_data = copy.deepcopy(entry)

        this_data[side]["chickens"] = s[side]["chickens"] - 1
        this_data[other_side]["chickens"] = s[other_side]["chickens"] + 1
        this_data[side]["wolves"] = s[side]["wolves"] - 1
        this_data[other_side]["wolves"] = s[other_side]["wolves"] + 1

        pprint.pprint(this_data)
        data.append(this_data)

    return data

if __name__ == "__main__":
    args = sys.argv
    data = load(args[1])
    goal = load(args[2])
    mode = args[3]
    output = args[4]

    # res = bfs(data, goal)
    adjacent = successor(data)

