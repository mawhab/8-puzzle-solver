from math import sqrt
import copy


class State:

    TARGET_VALS = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]] # map of correct positions for each number

    def __init__(self, init_state, previous_state=None) -> None:

        self.state_vals = init_state # initial state of board given by user

        self.previous_state = previous_state

        self.initial = False
        self.g = 0

        if self.previous_state == None:
            self.initial = True
            self.g = 0
        else:
            self.g = self.previous_state.get_g()+1

        self.state_coords = [[-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1], [-1,-1]]

        for i in range(3):
            for j in range(3):
                self.state_coords[self.state_vals[i][j]] = [i,j]

    # returns the target position of a given value
    def get_targetxy(val):
        return State.TARGET_VALS[val]

    # returns manhattan huerestic value of a given value in its current state
    def get_manhattan(self, val=-1):
        if val==-1:
            h = 0
            for i in range(9):
                h += self.get_manhattan(i)
            return h
        else:
            target = State.get_targetxy(val)
            dx = abs(self.state_coords[val][0] - target[0])
            dy = abs(self.state_coords[val][1] - target[1])
            return dx + dy

    # returns eucledian huerestic value of a given value in its current state
    def get_eucledian(self, val=-1):
        if val==-1:
            h = 0
            for i in range(9):
                h += self.get_eucledian(i)
            return h
        else:
            target = State.get_targetxy(val)
            dx_sq = (self.state_coords[val][0] - target[0])**2
            dy_sq = (self.state_coords[val][1] - target[1])**2
            return sqrt(dx_sq + dy_sq)
    def copy(state):
        new_state = [[0,0,0],
                     [0,0,0],
                     [0,0,0]]
        for i in range(3):
            for j in range(3):
                new_state[i][j] = state[i][j]
        return new_state

    # returns all neighboring states to current state
    def get_neighbors(self):
        """Returns all neighboring states to current state
           1- Get empty block's position
           2- If next block to the right is within board, create new state where they are swapped and add it to neighbors
           3- If next block to the left is within board, create new state where they are swapped and add it to neighbors
           4- If next block upward is within board, create new state where they are swapped and add it to neighbors
           5- If next block downward is within board, create new state where they are swapped and add it to neighbors
           6- Return neighbors
        """
        empty_block_row = self.state_coords[0][0]
        empty_block_column = self.state_coords[0][1]
        neighbors = []
        if empty_block_row+1 <= 2:
            new_state = State.copy(self.state_vals)
            new_state[empty_block_row][empty_block_column] = new_state[empty_block_row+1][empty_block_column]
            new_state[empty_block_row+1][empty_block_column] = 0
            neighbors.append(State(new_state, self))
        
        if empty_block_row-1 >= 0:
            new_state = State.copy(self.state_vals)
            new_state[empty_block_row][empty_block_column] = new_state[empty_block_row-1][empty_block_column]
            new_state[empty_block_row-1][empty_block_column] = 0
            neighbors.append(State(new_state, self))

        if empty_block_column+1 <= 2:
            new_state = State.copy(self.state_vals)
            new_state[empty_block_row][empty_block_column] = new_state[empty_block_row][empty_block_column+1]
            new_state[empty_block_row][empty_block_column+1] = 0
            neighbors.append(State(new_state, self))
        
        if empty_block_column-1 >= 0:
            new_state = State.copy(self.state_vals)
            new_state[empty_block_row][empty_block_column] = new_state[empty_block_row][empty_block_column-1]
            new_state[empty_block_row][empty_block_column-1] = 0
            neighbors.append(State(new_state, self))

        return neighbors

    def get_state_coords(self):
        return self.state_coords

    def get_state_vals(self):
        return self.state_vals

    def is_target_state(self):
        if self.state_coords == State.TARGET_VALS:
            return True
        else:
            return False

    def get_g(self):
        return self.g

    def get_cost(self, type=0):
        if type==0:
            return self.g + self.get_manhattan()
        elif type==1:
            return self.g + self.get_eucledian()

    def __lt__(self, state):
        return self.get_cost() < state.get_cost()

    def __le__(self, state):
        return self.get_cost() <= state.get_cost()

    def __gt__(self, state):
        return self.get_cost() > state.get_cost()

    def __ge__(self, state):
        return self.get_cost() >= state.get_cost()