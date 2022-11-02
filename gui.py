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

algorithm = -1

bfs_y = (30+btn_h+spc_long)
dfs_y = (bfs_y+btn_h+spc_short)
ast_y = (dfs_y+btn_h+spc_short)
sol_y = (ast_y+btn_h+spc_long)

buttons = pygame.sprite.Group()





play_lw = 420

sq = (play_lw/3) - 2

def check_events():
    global buttons
    if algorithm == -1:
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


def element_in_list(arr, elem):
    for i in range(len(arr)):
        if arr[i].get_state_vals()==elem:
            return i
    return -1

def BFS(initial_state):
    global solving
    frontier = deque()
    #frontier_states = deque()
    frontier_states = {}
    explored = {}

    frontier.append(initial_state)
    frontier_states[tuple(map(tuple,initial_state.get_state_vals()))] = True

    # while frontier and solving:
    while frontier:
        # check_events()

        state = frontier.popleft()
        frontier_states[tuple(map(tuple,state.get_state_vals()))] = False
        explored[tuple(map(tuple,state.get_state_vals()))] = True

        if len(explored) % 1000 == 0:
            print(f"Explored %s nodes" % (len(explored)))

        if len(frontier) % 1000 == 0:
            print(f"%s nodes in frontier" % (len(frontier)))

        # print("Visiting: ", end='')
        # print(state.get_state_vals())

        if state.is_target_state():
            return state
        
        for neighbor in state.get_neighbors():
            try:
                exp = explored[tuple(map(tuple,neighbor.get_state_vals()))]
            except KeyError:
                exp = False
            try:
                front = explored[tuple(map(tuple,neighbor.get_state_vals()))]
            except KeyError:
                front = False
            if exp or front:
                continue
            else:
                frontier.append(neighbor)
                #frontier_states.append(neighbor.get_state_vals())
                frontier_states[tuple(map(tuple,state.get_state_vals()))] = True

    return None

def DFS(initial_state):
    global solving
    frontier = deque()
    frontier_states = deque()
    explored = {}

    frontier.append(initial_state)
    frontier_states.append(initial_state.get_state_vals())

    while frontier and solving:
        check_events()

        state = frontier.pop()
        frontier_states.pop()
        explored[tuple(map(tuple,state.get_state_vals()))] = True

        # print("Visiting: ", end='')
        # print(state.get_state_vals())

        if state.is_target_state():
            return state
        
        for neighbor in state.get_neighbors():
            try:
                exp = explored[tuple(map(tuple,neighbor.get_state_vals()))]
            except KeyError:
                exp = False
            if exp or neighbor.get_state_vals() in frontier_states:
                continue
            else:
                frontier.append(neighbor)
                frontier_states.append(neighbor.get_state_vals())

    return None

def A_star(initial_state):
    global solving
    frontier = []
    # frontier_states = {}
    explored = {}

    heapq.heappush(frontier, initial_state)
    # frontier_states[tuple(map(tuple,initial_state.get_state_vals()))] = True
    

    # while frontier and solving:
    while frontier:
        #check_events()

        state = heapq.heappop(frontier)
        try:
            exp = explored[tuple(map(tuple,state.get_state_vals()))]
        except KeyError:
            exp = False
        if exp:
            continue
        explored[tuple(map(tuple,state.get_state_vals()))] = True
        if len(explored) % 1000 == 0:
            print(f"Explored %s nodes" % (len(explored)))

        if len(frontier) % 1000 == 0:
            print(f"%s nodes in frontier" % (len(frontier)))

        # print("Visiting: ", end='')
        # print(state.get_state_vals())

        if state.is_target_state():
            return state
        
        for neighbor in state.get_neighbors():
            try:
                exp = explored[tuple(map(tuple,neighbor.get_state_vals()))]
            except KeyError:
                exp = False

            # try:
            #     front = frontier_states[tuple(map(tuple,neighbor.get_state_vals()))]
            # except KeyError:
            #     front = False

            if exp:
                continue
                # if i>-1 and neighbor.g < frontier[i].g:
                #     #del frontier[i]
                #     frontier[i].g, frontier[i].previous_state = neighbor.g, neighbor.previous_state
                #     frontier[i].initial = neighbor.initial

                #     heapq.heapify(frontier)
                #     #heapq.heappush(frontier, (neighbor.get_cost(), neighbor))
            else:
                heapq.heappush(frontier, neighbor)

    return None


def unblock_all():
    global buttons
    for btn in buttons:
        btn.unblock()

def random_state():
    state = np.random.choice(9,(3,3),replace=False)
    return state.tolist()

def random_cb():
    global state
    state = random_state()
    draw_state(state)
    print(state)

def bfs_cb():
    global algorithm
    algorithm = 1
    unblock_all()
    buttons.sprites()[1].block()

def dfs_cb():
    global algorithm
    algorithm = 2
    unblock_all()
    buttons.sprites()[2].block()

def ast_cb():
    global algorithm
    algorithm = 3
    unblock_all()
    buttons.sprites()[3].block()

def print_states(states):
    for state in states:
        for row in state:
            print(row)
        print()

def display_seq(state):
    global font
    states = []
    while state:
        check_events()
        states.append(state.get_state_vals())
        state = state.previous_state

    states.reverse()
    print_states(states)
    for i in range(len(states)):
        check_events()
        pygame.draw.rect(screen, screen_color, (120, 450, 100,30))
        draw_state(states[i])
        moves_count = font.render(str(i), True, text_color)
        screen.blit(moves_count, pygame.Rect(120, 450, 100,30))
        pygame.display.flip()
        time.sleep(1)
    

def solve():
    global algorithm, state, solving, screen, screen_color
    seq = None
    state_obj = State(state)
    solving = True
    unblock_all()
    pygame.draw.rect(screen, screen_color, (500, 450, 100,30))
    t_start = time.time()
    if algorithm == 1:
        algorithm = -1
        seq = BFS(state_obj)
    elif algorithm == 2:
        algorithm = -1
        seq = DFS(state_obj)
    elif algorithm == 3:
        algorithm = -1
        seq = A_star(state_obj)

    solving = False

    t = font.render('%.2f s' % (time.time() - t_start), True, text_color)
    if seq:
        screen.blit(t, pygame.Rect(500, 450, 100,30))
        pygame.display.flip()
    display_seq(seq)

def stop():
    global solving
    solving = False
    


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

pygame.init()

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
# state = [[3,6,4],
#          [2,0,7],
#          [1,8,5]]
# setup()
# state = [[8,6,1],
#          [0,7,3],
#          [4,2,5]]

state_obj = State(state)
cProfile.run('A_star(state_obj)')
# print(BFS(state_obj))

# while True:
#     check_events()

