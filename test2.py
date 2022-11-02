from Board import *
import heapq
import numpy as np
import cProfile

state = [[3,6,4],
         [2,0,7],
         [1,8,5]]

target_state = [[0,1,2],
                [3,4,5],
                [6,7,8]]

# 182754630

state_test = [[1,8,2],
              [7,5,4],
              [6,3,0]]


state_easy = [[1,0,2],
              [3,4,5],
              [6,7,8]]

d = State(state_easy)

b = State(state)
s = State(state_test)

l = []

one = 1

three = 3

five = 5 

heapq.heappush(l, (five,d))

heapq.heappush(l, (one,s))

heapq.heappush(l, (three,b))

print(heapq.heappop(l))
print(heapq.heappop(l))
print(heapq.heappop(l))

colors = [1,2,3,4]

o,t,tt,f = colors

print(o)
print(t)
print(tt)
print(f)


state = np.random.choice(9,(3,3),replace=False)

print(state)

def fun():
    print("fun")

x = fun

x()

for i in range(7000000):
    # print(i)
    pass

print('done')

p = {'al': 2, 'lsos':4}

print(len(p))

# cProfile.run('fun()')
x = [[0]*3]*3
print(x)