from Board import *
from collections import deque
import heapq

def print_sequence(state):
    print("Reached through the following sequence:")
    while state:
        for row in state.get_state_vals():
            print(row)
        print()
        state = state.previous_state

def element_in_list(arr, elem):
    for i in range(len(arr)):
        if arr[i].get_state_vals()==elem:
            return i
    return -1

def BFS(initial_state):
    frontier = deque()
    frontier_states = deque()
    explored = []

    frontier.append(initial_state)
    frontier_states.append(initial_state.get_state_vals())

    while frontier:
        state = frontier.popleft()
        frontier_states.popleft()
        explored.append(state.get_state_vals())

        print("Visiting: ", end='')
        print(state.get_state_vals())

        if state.is_target_state():
            return state
        
        for neighbor in state.get_neighbors():
            if neighbor.get_state_vals() in explored or neighbor.get_state_vals() in frontier_states:
                continue
            else:
                frontier.append(neighbor)
                frontier_states.append(neighbor.get_state_vals())

    return None

def DFS(initial_state):
    frontier = deque()
    frontier_states = deque()
    explored = []

    frontier.append(initial_state)
    frontier_states.append(initial_state.get_state_vals())

    while frontier:
        state = frontier.pop()
        frontier_states.pop()
        explored.append(state.get_state_vals())

        print("Visiting: ", end='')
        print(state.get_state_vals())

        if state.is_target_state():
            return state
        
        for neighbor in state.get_neighbors():
            if neighbor.get_state_vals() in explored or neighbor.get_state_vals() in frontier_states:
                continue
            else:
                frontier.append(neighbor)
                frontier_states.append(neighbor.get_state_vals())

    return None

def A_star(initial_state):
    frontier = []
    explored = []

    heapq.heappush(frontier, initial_state)

    while frontier:
        state = heapq.heappop(frontier)
        explored.append(state.get_state_vals())

        print("Visiting: ", end='')
        print(state.get_state_vals())

        if state.is_target_state():
            return state
        
        for neighbor in state.get_neighbors():
            i = element_in_list(frontier, neighbor.get_state_vals())
            if neighbor.get_state_vals() in explored or i>-1:
                if i>-1:
                    #del frontier[i]
                    frontier[i].g, frontier[i].previous_state = state.g, state.previous_state
                    frontier[i].initial = state.initial

                    heapq.heapify(frontier)
                    #heapq.heappush(frontier, (neighbor.get_cost(), neighbor))
            else:
                heapq.heappush(frontier, neighbor)

    return None




# state = [[3,6,4],
#          [2,0,7],
#          [1,8,5]]

# target_state = [[0,1,2],
#                 [3,4,5],
#                 [6,7,8]]

# # 182754630

# state_test = [[2,3,6],
#               [5,7,4],
#               [1,0,8]]

# new_state = [[6, 7, 8], [0, 3, 1], [4, 5, 2]]


# state_easy = [[1,0,2],
#               [3,4,5],
#               [6,7,8]]


# b = State(state_test, None)

# t_start = time.time()

# final = BFS(b)

# t = time.time() - t_start

# print(f"Finished in %s s" % (t))

# print_sequence(final)