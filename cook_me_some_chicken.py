import sys

def load(path):

    with open(path, "r") as f:
        left = f.readline().split(',')
        right = f.readline().split(",")

        data = {
            "left": {
                "chickens": left[0],
                "wolves": left[1],
                "boat": left[2] == "1",
            },
            "right": {
                "chickens": right[0],
                "wolves": right[1],
                "boat": right[2] == "1",
            }
        }

        return data

if __name__ == "__main__":
    args = sys.argv
    data = load(args[1])
    goal = load(args[2])
    mode = args[3]
    output = args[4]


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
