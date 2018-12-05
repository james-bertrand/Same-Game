from same_game import utils
import random
import numpy as np
from same_game import searches

# This module will store information on each iteration of the game,
# and be able to return modifications of the state

# Max 15x15 for the size---not really you can make it as big as you want currently
# Max 5 colors: Red Orange Yellow Green Blue---not really you can make as many colors as you want

class State:

    def __init__(self, name, size, colors, data=None):
        self.name = name  # String to represent state
        self.size = size  # Int between 1-15 for the length and width
        self.colors = colors  # Int between 1-5 picking the number of colors
        self.score = 0  # Keeps track of score for the board
        if data is None: # if no initial array is passed in, it will generate it's own
            self.data = self.setup()
        else:
            self.data = data  # 2D numpy array using int x, y, and value for color
        self.memory = [] # an array of coordinates (each coordinate is an array of two ints)
                         # that stores the values that have been visited by the sections function

    # def __init__(self, name, size, colors, data):
    #     self.name = name  # String to represent state
    #     self.size = size  # Int between 1-15 for the length and width
    #     self.colors = colors  # Int between 0-4 picking the number of colors
    #     self.data = data

    # randomly creates a 2D numpy array for a game state with the specified parameters
    def setup(self):
        matrix = np.empty([self.size,self.size])
        for row in range(self.size):
            for col in range(self.size):
                matrix[row][col] = random.randint(1,self.colors)
        return matrix

    # returns the int color value of the specified x y values
    def getColor(self, x, y):
        if x < self.size:
            if y < self.size:
                return self.data[x][y]

    # returns a list of valid moves
    def moves(self):
        moves = self.sections()
        toRemove = []
        count = 0
        for i in moves:
            if len(moves[count]) < 2:
                toRemove.append(i)
            count = count +1
        for i in toRemove:
            moves.remove(i)
            #print(i)

        return moves

    # returns true if there are moves left, will return false if there isnt
    def movesLeft(self):
        moves = self.moves()
        if moves == []:
            return False
        return True

    # creates a list of possible sections to select for removal
    # returns a list of arrays of coordinates that have the same color value and are touching
    # list layout: [ [[x,y],[x,y]], [[x,y],[x,y],[x,y]], ... ]
    def sections(self):
        self.memory = [] # makes sure the memory array is cleared
        moves = [] # creates a list to add the arrays of coordinates to
        for row in range(self.size): # for every row (x coordinate)
            for col in range(self.size): # for every column (y coordinate)
                if self.data[row][col] != 0: # if the current coordinate is not 0 (empty)
                    if [row, col] not in self.memory: # and if the current coordinate is not in the memory
                        self.memory.append([row,col]) # add the coordinate to memory
                        move = self.recSections([row,col], []) # call recursive function to check coordinates around the current for matches
                        moves.append([[row,col]] + move) # concatenates original coordinate and returned touching coordinates into list
        return moves # returns the list of arrays of coordinates

    # recursive function to determine the touching coordinates of the passed in variable
    # parameters: current - coordinate: [x,y], move - list that temporarily stores each branches' touching coordinates before concatenation
    # returns: list of coordinates [x,y] that touch the original passed-in coordinate
    def recSections(self, current, move):
        move1, move2, move3, move4 = [], [], [], [] # creates the placeholders for each branch test
        if current[0]-1 >= 0: # test to make sure the coordinate to the left is valid
            # if the color value of the current equals the color value to the left    and   the color value to the left is not in the memory
            if self.data[current[0]][current[1]] == self.data[current[0]-1][current[1]] and [current[0]-1,current[1]] not in self.memory:
                self.memory.append([current[0]-1, current[1]]) # add the color value to the left into the memory
                move1 = self.recSections([current[0] - 1, current[1]], move1) # call the recursive function on the new coordinate, and assign returned list
                move1.append([current[0]-1, current[1]]) # adds the coordinate passed to the list as well
        if current[0]+1 < self.size: # test to make sure the coordinate to the right is valid
            if self.data[current[0]][current[1]] == self.data[current[0]+1][current[1]] and [current[0]+1,current[1]] not in self.memory:
                self.memory.append([current[0]+1, current[1]])
                move2 = self.recSections([current[0]+1, current[1]], move2)
                move2.append([current[0]+1, current[1]])
        if current[1]-1 >= 0: # test to make sure the coordinate to the top is valid
            if self.data[current[0]][current[1]] == self.data[current[0]][current[1]-1] and [current[0], current[1]-1] not in self.memory:
                self.memory.append([current[0], current[1]-1])
                move3 = self.recSections([current[0], current[1]-1], move3)
                move3.append([current[0], current[1]-1])
        if current[1]+1 < self.size: # test to make sure the coordinate to the bottom is valid
            if self.data[current[0]][current[1]] == self.data[current[0]][current[1]+1] and [current[0], current[1]+1] not in self.memory:
                self.memory.append([current[0], current[1]+1])
                move4 = self.recSections([current[0], current[1]+1], move4)
                move4.append([current[0], current[1]+1])
        return move1 + move2 + move3 + move4 # combine the different branches into one list

    # will remove all of the squares from the coordinates passed in, and will move the rest of the squares down and to the left to fill in the space
    # parameters: move - array of coordinates
    # modifies the current state, doesnt return anything
    def remove(self, move):
        moveScore = self.count(move)    # get the score for the move
        self.score += ((moveScore - 2) ** 2)        # add it to the total score

        for i in range(len(move)):
            self.data[move[i][0], move[i][1]] = 0
        for i in range(self.size):
            for col in range(self.size): #pushes everything down starting from bottom and moving up
                for row in range(self.size-1):
                    if self.data[(self.size - row - 1), col] == 0:
                        self.data[(self.size - row - 1), col] = self.data[(self.size - row - 2), col]
                        self.data[(self.size - row - 2), col] = 0
        for i in range(self.size):
            for col in range(self.size-1):
                count = 0
                for row in range(self.size):
                    count += self.data[row, col]
                if count == 0:
                    for row in range(self.size):
                        self.data[row, col] = self.data[row,col+1]
                        self.data[row, col + 1] = 0

    # returns number of squares connected within a move (a move is a list of coordinates)
    def count(self, move):
        if move == None:
            return 0
        return len(move)

    # Returns the number of tiles that are left
    def remainingTiles(self):
        return np.count_nonzero(self.data)

    # Checks to see if the board is empty, returning true if it is, false otherwise
    def isEmpty(self):
        if np.count_nonzero(self.data) == 0:
            return True
        else:
            return False

    # will return the frequency of each color in the table, with each number correlating to the position
    # in the array returned
    def amounts(self):
        l = []
        for i in range(self.colors+1):
            l.append(0)
        for row in range(self.size):
            for col in range(self.size):
                l[int(self.data[row][col])] = l[int(self.data[row][col])] + 1
        return l

    # returns the number that has the highest frequency (excluding 0)
    def highest(self):
        l = self.amounts()
        highest = 1
        for i in range(len(l)-2):
            if l[i + 1] < l[i + 2]:
                highest = i+2
        return highest

    def lowest(self):
        l = self.amounts()
        lowest = 1
        for i in range(len(l)-2):
            if l[i + 1] > l[i + 2]:
                lowest = i+2
        return lowest

    # will change the specified amount of tiles randomly to the color that is most frequent
    def changeATile(self, amount):
        lowest = self.lowest()
        l = self.amounts()
        #print(highest)
        for i in range(amount):
            go = True
            while go:
                x = random.randint(0,self.size-1)
                y = random.randint(0,self.size-1)
                if self.data[x,y] != lowest and self.data[x,y] != 0 and l[int(self.data[x,y])] != 0:
                    self.data[x,y] = lowest
                    go = False




