#tic tac toe implementation with minimax algorithm 
import math
import numpy as np

# the class with the required methods to play tic-tac-toe
class Tic_Tac_Toe():
    
    
    # method to initialize the class   
    def __init__ (self):
        self.game_board = [['#', '#', '#'], ['#', '#', '#'], ['#', '#', '#']]   #the game board is empty at first. We show the blank spaces with '#'
        self.n = 3  # the tic-tac-toe board is 3*3
    
            
    # terminal test would check if the game is over (whether the board is full, or one opponent wins)            
    def terminal_test(self, state):
        cnt_x = 0   # to count the x and os on the board
        cnt_o = 0
        
        if len(self.actions(state)) == 0:   # check whether the game board is full or not   
            return True
        
        for i in range(self.n):     # check whether they are 3 x or os on right diagonal 
            if state[i][i] == 'x':
                cnt_x+=1
            elif state[i][i] == 'o':
                cnt_o += 1
            if cnt_o == 3 or cnt_x == 3:
                return True
            
        cnt_x = 0   # set the counters back to 0 
        cnt_o = 0 
        
        for i in range(self.n):     # check whether they are 3 x or os on left diagonal 
            if state[i][self.n - i - 1] == 'x':
                cnt_x+=1
            elif state[i][self.n - i - 1] == 'o':
                cnt_o += 1
            if cnt_o == 3 or cnt_x == 3:
                return True    
        
        for row in state:   # to check the rows
            if len(set(row)) == 1 and row[0] != '#':    # we turn the row to a set, if the 3 elements are the same, the set would have only one element, and we check that the one element wouldn't be blank
                return True
        
        column = []  
        columns = []
        
        for j in range(self.n):     # we turn the columns to a list to check them further like the rows 
            column = []
            for i in range(self.n):
                column.append(state[i][j])
            columns.append(column)
        

        for column in columns:  # to check the columns
            if len(set(column)) == 1 and column[0] != '#':  # we turn the column to a set, if the 3 elements are the same, the set would have only one element, and we check that the one element wouldn't be blank
                return True
    
        else:
            return False    # all other states would result as non-terminal
            
        
        
    # the actions method would return the position of blank spaces that can be filled
    def actions(self, state):
        blank = []
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] != 'o' and state[i][j] != 'x':
                    blank.append((i,j))     # fill the blank list with the position coordinates of the blank spaces     
        return blank
    
    
    # the utility function works just like terminal test method but it returns the utilities, 0 for when o wins, 1/2 for draw, 1 for when x wins, the other lines have been explained before 
    def utility(self, state):
        
        cnt_x = 0
        cnt_o = 0
        
        for i in range(self.n):
            if state[i][i] == 'x':
                cnt_x+=1
            if cnt_x == 3:
                return 1
            elif state[i][i] == 'o':
                cnt_o += 1
            if cnt_o == 3:
                return 0
            
        cnt_x = 0
        cnt_o = 0 
        
        for i in range(self.n):
            if state[i][self.n - i - 1] == 'x':
                cnt_x+=1
            if cnt_x == 3:
                return 1
            elif state[i][self.n - i - 1] == 'o':
                cnt_o += 1
            if cnt_o == 3:
                return 0     
            
            
        for row in state:
            if len(set(row)) == 1 and row[0] == 'x':
                return 1
            elif len(set(row)) == 1 and row[0] == 'o':
                return 0
        
        column = []
        columns = []
        
        for j in range(self.n):
            column = []
            for i in range(self.n):
                column.append(state[i][j])
            columns.append(column)
        
        for column in columns:
            if len(set(column)) == 1 and column[0] == 'x':
                return 1
            if len(set(column)) == 1 and column[0] == 'o':
                return 0

        if len(self.actions(state)) == 0:    
            return 1/2
    
    
    # result method would take the state, position and a character as the input and insert the character at the given position at the current state, then returns it
    def result(self, state, position, char):
        state[position[0]][position[1]] = char  # position is a list of tuples so position[0] would mean i and position[1] would mean  j
        return state
    
    # this next three methods have been inspired by the recursive minimax pseudocode of the reference book                        
    def max_value(self, state): # this method would recursively traverse the game till the end to find the values of each state for max nodes
        char = 'x'
        if self.terminal_test(state):
            return self.utility(state)  # if the it is a terminal state the value would be same as utility
        v = -math.inf
        
        for blank in self.actions(state):
            v = max(v, self.min_value(self.result(np.copy(state),blank, char)))     # the max nodes must choose the maximum value from the min nodes of the level below in the minimax tree
        return v   
    
    
    def min_value(self, state):     # this method would recursively traverse the game till the end to find the values of each state for min nodes
        char = 'o'
        if self.terminal_test(state):
            return self.utility(state)  # if the it is a terminal state the value would be same as utility
        v = +math.inf
        
        for blank in self.actions(state):
            v = min(v, self.max_value(self.result(np.copy(state),blank, char)))   # the min nodes must choose the minimum value from the max nodes of the level below in the minimax tree
        return v         
                   
    
    # the minimax method would decide which action to choose between all the actions
    def Minimax(self,state):
        temp_v = -math.inf
        for blank in self.actions(state):
            v = self.min_value(self.result(np.copy(state), blank, 'x'))    # the computer plays as max (x)
            if v > temp_v:
                temp_v = v
                b = blank      # to find the best action (as the position of putting the next 'x')
        return b
    
    
    # this method would make turns possible 
    def play(self):
        while not self.terminal_test(self.game_board): #till the game is not over 
            position = self.Minimax(self.game_board)    # find the optimal decision for max(the computer)
            self.game_board[position[0]][position[1]] = 'x' # put the 'x' on the best found position on the game board
            print(self.game_board)      
            print("- - - - - -")
            if self.terminal_test(self.game_board):    # check whether the game is over after putting x on the board
                print("game over")
                return
            i = int(input("Enter the row: "))   # take the position of o from the user 
            j = int(input("Enter the column: "))
            self.game_board[i][j] = 'o' # insert the o on the game board at the given position
            print(self.game_board)
        print(self.game_board)    
            
            
            
            
                   
                   
                   
                            
# the driver code 
t = Tic_Tac_Toe()
t.play()