# a1.py

import sys
import time

from pip._vendor.html5lib._utils import memoize

sys.path.insert(0, '/Users/mac/aima-python')
from search import *


class EightPuzzle(Problem):

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        self.goal = goal
        Problem.__init__(self, initial, goal)

    def find_blank_square(self, state):  # check if ok
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):

        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):

        return state == self.goal

    def h(self, node):
        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

    def check_if_solvability(self, state):
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0


def display(state):
    print(" Unsolved state :")
    fin = [[state.initial[0], state.initial[1], state.initial[2]],
           [state.initial[3], state.initial[4], state.initial[5]],
           [state.initial[6], state.initial[7], state.initial[8]]]
    for i in range(len(fin)):
        for j in range(len(fin[i])):
            if fin[i][j] == 0:
                print("*  ", end="")
            else:
                print(fin[i][j], " ", end="")
        print("")


def make_rand_8puzzle(argument):
    if len(argument) == 0:
        temp = random.sample([i for i in range(0, 9)], 9)
    else:
        temp = list(map(int, argument))
    EightPuzzle_object = EightPuzzle(tuple(temp))
    solvable = False
    while solvable == False:
        if EightPuzzle_object.check_if_solvability(temp):
            print(temp)
            solvable = True
        else:
            print(temp)
            print(" The original is not solvability")
            temp = random.sample([i for i in range(0, 9)], 9)
    EightPuzzle_object.initial = tuple(temp)
    display(EightPuzzle_object)
    return EightPuzzle_object


def best_first_graph_search(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    count = 0
    while frontier:
        node = frontier.pop()
        count = count + 1
        if problem.goal_test(node.state):
            return (node, count)
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, count


def astar_search(inst, h=None, display=True):
    h = memoize(h or inst.h, 'h')
    return best_first_graph_search(inst, lambda n: n.path_cost + h(n), display)


def manhattan(node):
    # https://github.com/aimacode/aima-python this is the textbook code from Github
    # after modification in search.ipynb
    # In [40]: Heuristics for 8 Puzzle Problem

    # print(node)
    state = node.state
    goal_state = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2],
                  4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    temp = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1],
             [1, 2], [2, 0], [2, 1], [2, 2]]
    x, y = 0, 0

    for i in range(len(state)):
        temp[state[i]] = index[i]

    count = 0

    for i in range(1, 9):
        for j in range(2):
            count = abs(goal_state[i][j] - temp[i][j]) + count

    return count


def swap(state, a, b):
    temp = state[a]
    state[a] = state[b]
    state[b] = temp


def gaschnig(node):
    state = list(node.state)
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    moves = 0
    while state != goal_state:
        index_blank = state.index(0)
        if goal_state[index_blank] != 0:    # blank not in goal position
            temp = goal_state[index_blank]
            index_corresponding = state.index(temp)    # find the corresponding in unsolved part
            swap(state, index_corresponding, index_blank)
        else:
            for i in range(len(state)):
                if state[i] != goal_state[i]:
                    swap(state, i, index_blank)
                    break
        moves = moves + 1
    # print(state)
    return moves


def misplaced_tiles_heuristic(eight_puzzle):
    start_time = time.time()
    result_misplaced, count_misplaced = astar_search(eight_puzzle)
    elapsed_time = time.time() - start_time

    print("----->  A*-search by using the !! misplaced tile heuristic !!  <-----")
    print(f"The total running time in A* searching algorithm is (in seconds): {elapsed_time}")
    print("The total nodes that were expanded are", count_misplaced)
    print("The total length of moving for the solution are", len(result_misplaced.solution()))
    print(end="")


def manhattan_Distance_Heuristic(manhattan_use):
    start_time = time.time()
    result_manhattan, count_manhattan = astar_search(manhattan_use, h=manhattan)
    elapsed_time = time.time() - start_time
    print("----->  A*-search by using the !! Manhattan Distance Heuristic !!  <-----")
    print(f"The total running time in manhattan Distance algorithm is (in seconds): {elapsed_time}")
    print("The total nodes that were expanded are", count_manhattan)
    print("The total length of moving for the solution are", len(result_manhattan.solution()))
    print(end="")


def gaschnig_Heuristic(manhattan_use):
    start_time = time.time()
    count_gaschnig = astar_search(manhattan_use, h=gaschnig)
    elapsed_time = time.time() - start_time
    print("----->  A*-search by using the !! Gaschnig_Heuristic !!  <-----")
    print(f"The total running time in gaschnig Heuristic algorithm is (in seconds): {elapsed_time}")
    print("The total nodes that were expanded are", count_gaschnig)
    print(end="")


arr = make_rand_8puzzle(sys.argv[1:])
manhattan_arr = arr
gaschnig_arr = arr

misplaced_tiles_heuristic(arr)
manhattan_Distance_Heuristic(manhattan_arr)
gaschnig_Heuristic(gaschnig_arr)
