
# 8 Puzzle solver

Thre implementations of the 8 puzzle problem. BFS, DFS, and A*.


## BFS

We run a standard BFS algorithm that looks through the possible states level by level trying to reach an optimal path.
There are some optimizations used like keeping track of explored nodes and nodes in the frontier by keeping them in hash maps to allow for O(1) access and search.
This algorithm is guaranteed to find the optimal solution but it isn't the most effecient algorithm to get it.

### Path to goal
1. The algorithm takes an initial state and adds it to the frontier queue.
2. The algorithm runs in a loop while the frontier is not empty, the solution hasn't been found, and the user has not requested termination through the gui.

### Cost of path

The cost of path in BFS is the depth of node as all links between nodes are given as having a cost of 1.

### Nodes expanded
BFS has a worst case space complexity of O(B^m). In our case we have a max branching factor of 4 and a max depth of x. This shows we have a max number of nodes of O(4^x).
Another way we can show this is by saying that the total number of possible states is equal to 9^9. But you can only reach (9^9)/2 states from any given state. So in the worst possible case you would have (9^9)/2 expanded nodes.

### Running time
BFS has a worst case running time of O(B^m). In our case we have a max branching factor of 4 and a max depth of x. This shows we have a worst case running time of O(4^x).


## DFS

We run a standard DFS algorithm that looks through the possible states by depth trying to reach an optimal path.
There are some optimizations used like keeping track of explored nodes and nodes in the frontier by keeping them in hash maps to allow for O(1) access and search.
This algorithm is not guaranteed to find the optimal solution.

### Path to goal
1. The algorithm takes an initial state and adds it to the frontier queue.
2. The algorithm runs in a loop while the frontier is not empty, the solution hasn't been found, and the user has not requested termination through the gui.

### Cost of path

The cost of path in DFS is the depth of node as all links between nodes are given as having a cost of 1.

### Nodes expanded
DFS has a worst case space complexity of O(B^m). In our case we have a max branching factor of 4 and a max depth of x. This shows we have a max number of nodes of O(4^x).
Another way we can show this is by saying that the total number of possible states is equal to 9^9. But you can only reach (9^9)/2 states from any given state. So in the worst possible case you would have (9^9)/2 expanded nodes.

### Running time
DFS has a worst case running time of O(B^m). In our case we have a max branching factor of 4 and a max depth of x. This shows we have a worst case running time of O(4^x).


## A*

We run an A* algorithm by using both the cost between nodes (1) and one of two simple heuristic
functions (manhattan distance and eucledian). A* is guaranteed to find the optimal solution
and has relatively better performance compared to BFS and DFS.

### Path to goal
1. The algorithm takes an initial state and adds it to the frontier queue.
2. The algorithm runs in a loop while the frontier is not empty, the solution hasn't been found, and the user has not requested termination through the gui.

### Cost of path

The cost of path in DFS is the depth of node as all links between nodes are given as having a cost of 1.
The manhattan distance is given by abs(currentx - targetx) + abs(currenty- targety)
The eucledian distance is given by sqrt(abs(currentx - targetx)^2 + abs(currenty- targety)^2)


## Data structures used

### Hash maps
We used multiple hash maps to keep track of what states were visited and what states are currently
in the frontier list to utilize the O(1) access and search times.

### Python list
We used python lists as they provide implementation for stacks and queues out of the
box which is very convenient for this use case.

### Python heapq
We used a heapq to represent priority queues out of python lists.

## Algorithms used
Apart from BFS, DFS, and A*, we used a few algorithms to reach better performance.

### Check if puzzle is solvable
We used a simple algorithm that checked if a given state is solvable or not by checking the number of
misplaced tiles in the state. If the number is even then it is solvable otherwise there is no 
possible solution.

### Copying states
We initially were going to use python's copy.deepcopy() to copy states to generate neighbors
but that turned out to be very slow and time consuming so instead we implemented a
simple copy function that took a state and returned a new list bject representing 
the same state.

### Get neighbors
We keep track of the position of the empty box to be able to find the neighbors
of a given state. We do so by returning a list of states where each state
has the empty block swapped with an adjacent block given that the empty block
is not on the edge.

### Randomise
We generate a random 3x3 matrix with non repeating values then check if it is solvable.

## Screenshots
### State: 
![State](https://i.ibb.co/jZGC1qS/state.png)

### BFS:
![BFS](https://i.ibb.co/s5YW9bv/BFS.png)

### DFS:
![DFS](https://i.ibb.co/sCwpr7C/DFS.png)


### A*:
![A*](https://i.ibb.co/Pc3Wb5Y/As.png)