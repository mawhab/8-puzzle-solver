import pygame
import pygame.locals
from Button import *
import numpy as np
from test import *
import time
from Board import *
from collections import deque
import heapq
import cProfile

# gui settings
padding = 20
btn_x = 460
btn_w = 100
btn_h = 30
spc_long = 90
spc_short = 10
solving = False

block_color = (117,163,163)
blank_color = (117,163,163)
solve_color = (117,163,163)
btn_color = (192,194,188)
screen_color = (128,134,121)
text_color = (255,255,255)
btn_text_color = (0,0,0)
btn_hover_color = (128,128,128)
btn_blocked_color = (128,128,128)

btn_colors = [btn_text_color, btn_color, btn_hover_color, btn_blocked_color]

play_lw = 420

sq = (play_lw/3) - 2

bfs_y = (30+btn_h+spc_long)
dfs_y = (bfs_y+btn_h+spc_short)
ast_y = (dfs_y+btn_h+spc_short)
sol_y = (ast_y+btn_h+spc_long)

buttons = pygame.sprite.Group()


# selected algorithm (-1 indicates none selected)
algorithm = -1



# function to check gui events
def check_events():
    global buttons, solvable
    if algorithm == -1 or not solvable:
        buttons.sprites()[4].block()
    else:
        buttons.sprites()[4].unblock()

    if solving:
        buttons.sprites()[5].unblock()
    else:
        buttons.sprites()[5].block()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


        if event.type == pygame.MOUSEMOTION:
            for btn in buttons:
                if btn.rect.collidepoint(pygame.mouse.get_pos()):
                    btn.hover()
                else:
                    btn.not_hover()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in buttons:
                if btn.rect.collidepoint(pygame.mouse.get_pos()):
                    btn.cb()

    
    buttons.update()
    buttons.draw(screen)

    pygame.display.flip()


def BFS(initial_state):
    global solving # global variable that indicates wether user wants to solve or stop
    frontier = deque() # main queue
    frontier_states = {} # dictionary to keep track of nodes in frontier faster
    explored = {} # dictionary to keep track of visited nodes

    frontier.append(initial_state) # adding initial state
    frontier_states[tuple(map(tuple,initial_state.get_state_vals()))] = True # adding initial state to dict

    # while there are states not visited in frontier
    while frontier and solving: # while frontier is not empty and user hasn't requested stopping of solution
    # while frontier:
        # check_events()

        state = frontier.popleft() # get next state in queue
        frontier_states[tuple(map(tuple,state.get_state_vals()))] = False # remove state from dictionary
        explored[tuple(map(tuple,state.get_state_vals()))] = True # add state to explored

        # prints used for debuging and watching output

        # if len(explored) % 10000 == 0:
        #     print(f"Explored %s nodes" % (len(explored)))

        # if len(frontier) % 10000 == 0:
        #     print(f"%s nodes in frontier" % (len(frontier)))

        # print("Visiting: ", end='')
        # print(state.get_state_vals())

        # check if goal state reached
        if state.is_target_state():
            print(state.get_state_vals())
            print(f"Explored %s nodes" % (len(explored)))
            return state
        
        # for each neighbor generated
        for neighbor in state.get_neighbors():
            # try to access element in dictionary if KeyError is reached then element is not found in dictionary
            try:
                exp = explored[tuple(map(tuple,neighbor.get_state_vals()))]
            except KeyError:
                exp = False

            # try to access element in dictionary if KeyError is reached then element is not found in dictionary
            try:
                front = frontier_states[tuple(map(tuple,neighbor.get_state_vals()))]
            except KeyError:
                front = False

            # if neighbor isn't in frontier or explored nodes add it to queue
            if not (exp or front):
                frontier.append(neighbor)
                frontier_states[tuple(map(tuple,state.get_state_vals()))] = True

    # if we reach this state then either no nodes found or user requested to stop solving
    print("None")
    print(f"Explored %s nodes" % (len(explored)))
    return None

def DFS(initial_state):
    global solving # global variable that indicates wether user wants to solve or stop
    frontier = deque() # main stack
    frontier_states = {} # dictionary to keep track of nodes in frontier faster
    explored = {} # dictionary to keep track of visited nodes

    frontier.append(initial_state) # adding initial state
    frontier_states[tuple(map(tuple,initial_state.get_state_vals()))] = True # adding initial state to dict

    while frontier and solving: # while frontier is not empty and user hasn't requested stopping of solution
    # while frontier:
        # check_events()

        state = frontier.pop() # get next element in stack
        frontier_states[tuple(map(tuple,state.get_state_vals()))] = False # remove element from dict
        explored[tuple(map(tuple,state.get_state_vals()))] = True # add element to visted

        # print used for debuging and watching solution as it runs (it slows down excution)
        # print("Visiting: ", end='')
        # print(state.get_state_vals())


        # check if goal state reached
        if state.is_target_state():
            print(state.get_state_vals())
            print(f"Explored %s nodes" % (len(explored)))
            return state
        
        # for each neighbor generated
        for neighbor in state.get_neighbors():
            # try to access element in dictionary if KeyError is reached then element is not found in dictionary
            try:
                exp = explored[tuple(map(tuple,neighbor.get_state_vals()))]
            except KeyError:
                exp = False
            # try to access element in dictionary if KeyError is reached then element is not found in dictionary
            try:
                front = frontier_states[tuple(map(tuple,neighbor.get_state_vals()))]
            except KeyError:
                front = False

            # if neighbor is not in frontier or in explored at it to stack
            if not (exp or front):
                frontier.append(neighbor)
                frontier_states[tuple(map(tuple,state.get_state_vals()))] = True

    # if we reach this state then either no nodes found or user requested to stop solving
    print("None")
    print(f"Explored %s nodes" % (len(explored)))
    return None

def A_star(initial_state):
    global solving # global variable that indicates wether user wants to solve or stop
    frontier = [] # main heap
    # frontier_states = {}
    explored = {} # dictionary to keep track of visited nodes

    heapq.heappush(frontier, initial_state) # pushing initial node to heap
    # frontier_states[tuple(map(tuple,initial_state.get_state_vals()))] = True
    

    while frontier and solving: # while frontier is not empty and user hasn't requested stopping of solution
    # while frontier:
        # check_events()

        state = heapq.heappop(frontier) # get next element in priority queue

        # check if element has already been visited because in this implementation we allow the same state to be in frontier mut
        try:
            exp = explored[tuple(map(tuple,state.get_state_vals()))]
        except KeyError:
            exp = False
        if exp:
            continue
        explored[tuple(map(tuple,state.get_state_vals()))] = True # add element to visted

        # prints used for debugging and  viewing solution live
        # if len(explored) % 1000 == 0:
        #     print(f"Explored %s nodes" % (len(explored)))

        # if len(frontier) % 1000 == 0:
        #     print(f"%s nodes in frontier" % (len(frontier)))

        # print("Visiting: ", end='')
        # print(state.get_state_vals())

        # chek if this is the goal state
        if state.is_target_state():
            print(state.get_state_vals())
            print(f"Explored %s nodes" % (len(explored)))
            return state
        
        # for each neighbor check if the neighbor has been explored
        for neighbor in state.get_neighbors():
            try:
                exp = explored[tuple(map(tuple,neighbor.get_state_vals()))]
            except KeyError:
                exp = False
            # if neighbor hasn't been explored add it to frontier
            if not exp:
                heapq.heappush(frontier, neighbor)

    # if we reach this state then either no nodes found or user requested to stop solving
    print("None")
    print(f"Explored %s nodes" % (len(explored)))
    return None

# undim all buttons
def unblock_all():
    global buttons
    for btn in buttons:
        btn.unblock()

# get random 3x3 list with non repeating elements
def random_state():
    state = np.random.choice(9,(3,3),replace=False)
    return state.tolist()

# call back for randomise button
def random_cb():
    global state, z, solvable
    state = random_state()
    print(state)
    draw_state(state)
    z = (-1,-1)
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                z = (i,j)
    solvable = isSolvable(state)
    if not solvable:
        print("No solution")

# call back for bfs selector button
def bfs_cb():
    global algorithm
    algorithm = 1
    unblock_all()
    buttons.sprites()[1].block()

# call back for dfs selector button
def dfs_cb():
    global algorithm
    algorithm = 2
    unblock_all()
    buttons.sprites()[2].block()

# call back for A* selector button
def ast_cb():
    global algorithm
    algorithm = 3
    unblock_all()
    buttons.sprites()[3].block()

# function to print each states from state list
def print_states(states):
    for state in states:
        for row in state:
            print(row)
        print()

# function to display state sequence from initial state to given state in gui given a node
def display_seq(state):
    global font
    states = []
    while state:
        check_events()
        states.append(state.get_state_vals())
        state = state.previous_state

    states.reverse()
    print_states(states)
    l = len(states)
    if l == 0:
        return
    s = ((15 / l)*1000000000) # time between each state. Total time should always be 15 s
    for i in range(l):
        check_events()
        pygame.draw.rect(screen, screen_color, (120, 450, 100,30))
        draw_state(states[i])
        moves_count = font.render(str(i), True, text_color)
        screen.blit(moves_count, pygame.Rect(120, 450, 100,30))
        pygame.display.flip()
        t_old = time.time_ns()
        while (time.time_ns() - t_old) <= s:
            check_events()
    
# callback function for solve button
def solve():
    global algorithm, state, solving, screen, screen_color, z # get global vars

    seq = None # final solution sequence
    state_obj = State(state, z) # state object from given state
    solving = True # flag to indicate solution is running
    unblock_all() # unblock all buttons
    pygame.draw.rect(screen, screen_color, (500, 450, 100,30)) 
    t_start = time.time() # start time

    # selecting algorithm to run
    if algorithm == 1:
        algorithm = -1
        seq = BFS(state_obj)
    elif algorithm == 2:
        algorithm = -1
        seq = DFS(state_obj)
    elif algorithm == 3:
        algorithm = -1
        seq = A_star(state_obj)

    solving = False # finished solving

    t = font.render('%.2f s' % (time.time() - t_start), True, text_color) # render sol time
    # if seq is available 
    if seq:
        screen.blit(t, pygame.Rect(500, 450, 100,30))
        pygame.display.flip()
    
    # display found sequence
    display_seq(seq)

# callback function for stop button
def stop():
    global solving
    solving = False

# A utility function to count
# inversions in given array 'arr[]'
def getInvCount(arr):
	inv_count = 0
	for i in range(0, 9):
		for j in range(i + 1, 9):
			if arr[i]!= 0 and arr[j] != 0 and arr[i] > arr[j]:
				inv_count += 1
	return inv_count

	
# This function returns true
# if given 8 puzzle is solvable.
def isSolvable(puzzle) :

	# Count inversions in given 8 puzzle
	inv_count = getInvCount([j for sub in puzzle for j in sub])

	# return true if inversion count is even.
	return (inv_count % 2 == 0)
	
# draw a given state on the screen
def draw_state(state=None):
    global sq, block_color,blank_color,font,text_color,screen
    for i in range(3):
        for j in range(3):
            color = block_color
            text = str(state[j][i])
            if state[j][i]==0:
                color = blank_color
                text = ''
            pygame.draw.rect(screen, color, pygame.Rect(22+(i*(sq+1)),22+(j*(sq+1)),sq,sq))
            txt = font.render(text, True, text_color)
            txt_Rect = txt.get_rect(center=(22+(i*(sq+1)+sq/2), 22+(j*(sq+1))+sq/2))
            screen.blit(txt, txt_Rect)

pygame.init() # init pygame

# setup gui and screen
def setup():
    global screen,btn_h,btn_h,spc_long,spc_short,play_lw,screen_color,text_color,bfs_y,dfs_y,ast_y,sol_y
    global buttons,btn_colors,font,state_easy,state
    
    screen = pygame.display.set_mode((580,530))
    
    pygame.display.set_caption('8 puzzle solver')
    
    screen.fill(screen_color)
    buttons.add(Button(screen, (btn_x, 30), 'Randomise', 20, btn_colors).set_cb(random_cb))
    
    buttons.add(Button(screen, (btn_x, bfs_y), 'BFS', 20, btn_colors).set_cb(bfs_cb))
    buttons.add(Button(screen, (btn_x, dfs_y), 'DFS', 20, btn_colors).set_cb(dfs_cb))
    buttons.add(Button(screen, (btn_x, ast_y), 'A*', 20, btn_colors).set_cb(ast_cb))

    
    buttons.add(Button(screen, (btn_x-10, sol_y), 'Solve', 20, btn_colors).set_cb(solve))
    buttons.add(Button(screen, (btn_x+70, sol_y), 'Stop', 20, btn_colors).set_cb(stop))

    font = pygame.font.Font('FreeSans.ttf', 25)

    moves = font.render('Moves: ', True, text_color)
    moves_count = font.render('0', True, text_color)
    screen.blit(moves_count, pygame.Rect(120, 450, 100,30))

    solved_in = font.render('Solved in: ', True, text_color)

    screen.blit(moves, pygame.Rect(20, 450, 100,30))
    screen.blit(solved_in, pygame.Rect(380, 450, 100,30))


    pygame.draw.rect(screen, (0,0,0), pygame.Rect(20,20,play_lw,play_lw))


    draw_state(state)

    buttons.update()
    buttons.draw(screen)

    pygame.display.flip()

state = random_state()
# state = [[8, 5, 2], [1, 4, 0], [6, 7, 3]]
# state = [[1, 2, 5], [3, 4, 0], [6, 7, 8]]
# state = [[5, 0, 2], [6, 8, 7], [3, 1, 4]]
# state = [[3, 6, 7],
#          [1, 4, 2],
#          [0, 8, 5]]

# state = [[1, 2, 5],
#          [3, 4, 0],
#          [6, 7, 8]]
solvable = isSolvable(state)
z = (-1,-1)
for i in range(3):
    for j in range(3):
        if state[i][j] == 0:
            z = (i,j)
# state = [[4, 5, 7], [8, 6, 1], [2, 0, 3]]
# state = [[3,6,4],
#          [2,0,7],
#          [1,8,5]]

setup()
# state = [[8,6,1],
#          [0,7,3],
#          [4,2,5]]
# print(state)
# if not solvable:
#     print("No solution")
# else:
#     state_obj = State(state, z)
#     cProfile.run('BFS(state_obj)')
# print(BFS(state_obj))

while True:
    check_events()


