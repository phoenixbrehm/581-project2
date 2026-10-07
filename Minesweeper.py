#Prologue Comment
#Module: Minesweeper.py
#Description: Contains Minesweeper class which is responsible for all the logic in Minesweeper project. It tracks authoritative board states and provides calculations/storage for other relavant information.
#Input: Initalization requires n: requested mine count, x: inital x coordinate of click, y: inital y coordinate of click.
#Output:    visited stores the visible 10x10 version of the matrix
#           matrix stores the authoritative location of the bombs in the 10x10 matrix
#           Allows call to request remaining mine/flag calculation
#Authors:
#   Joshua Lin
#   Tyler Oswald
#   Lena Palmieri
#   Nickan Safi
#   John Platkowski
#Creation Date:
#   September 16, 2026
import random
from collections import deque
import time



#MATRIX CONSTANTS
EMPTY = 0
EXPLODED_MINE = -2
MINE = -3
FLAG = -1
UNVISITED = None
#VISITED = >= 0

#Running Game State Constant
WIN = 1
LOSS = 0
RUNNING = 2

class Minesweeper:
    #How many placements MineAlgorithm tries before settling for the last one
    MAX_PLACEMENT_ATTEMPTS = 100

    #intialization function - Joshua Lin - 9/16/26
    #requires input of x, y (coordinates of click in 10x10 grid)
    #And n or number of mines requested
    def __init__(self, x, y, n):
        #Board sizes
        self.x_size = 10
        self.y_size = 10

        #This will be a 10x10 matrix that stores where the mines are
        self.matrix = self._empty()

        #This will be a 10x10 matrix that stores what the visited version of the grid looks like
        self.visited = self._empty()
        self.MineAlgorithm(x, y, n)

        self.start_time = time.time()
        self.end_time = None

    #Tyler - 9/16/2026
    #Edited by Josh
    def RecOpen(self, x, y):
        #Takes matrix cell position as input in the form of (x,y) pair
        #Outputs new board state with cells that have no mine neighbors revealed starting from input coords
        #Check if the coords passed in are invalid 
        if x < 0 or y < 0 or x >= self.x_size or y >= self.y_size:
            return
        #Check if we have already checked this square
        if self.visited[x][y] is not UNVISITED:
            return

        #Check for mines in near by squares
        adjacentMines = self.CheckSquare(x,y)
        #Uncover this tile. Storing the count is what /board serves, and it doubles as
        #the marker that keeps this recursion from running back over itself
        self.visited[x][y] = adjacentMines
        #We only want to reveal tiles if this square has no mines near it
        if adjacentMines == 0:
            #Check all adjacent tiles
            for neighbor in self._Neighbors(x, y):
                 self.RecOpen(*neighbor)
        return

    # John - 09/17/2026
    def CheckSquare(self, x, y):
        #Returns how many mines border (x, y)
        count = 0
        for nx, ny in self._Neighbors(x, y):
            if self.matrix[nx][ny] == MINE:
                count += 1
        return count
    # John - 09/17/2026
    def MineAlgorithm(self, x: int, y: int, n: int) -> list[list[int]]:
        #Spawns n mines in a board such that the first click at (x, y) neither instantly loses nor wins
        #(x, y) and its 8 neighbors start without mines, so (x, y) opens a 0 square
        total = self.x_size * self.y_size
        if not (0 <= n < total):
            raise ValueError(f"cannot place {n} mines on {total} cells")

        #Block x,y and its neighbors
        blocked = {(x, y)}
        for nx, ny in self._Neighbors(x, y):
            blocked.add((nx, ny))
        # Or just block x,y if there are too many bombs to guarantee the neighbors
        if n > total - len(blocked):
            blocked = {(x, y)}

        candidates = []
        for cx in range(self.x_size):
            for cy in range(self.y_size):
                if (cx, cy) not in blocked:
                    candidates.append((cx, cy))

        grid = None
        for _ in range(self.MAX_PLACEMENT_ATTEMPTS):
            grid = [[EMPTY] * self.y_size for _ in range(self.x_size)]
            for cx, cy in random.sample(candidates, n):
                grid[cx][cy] = MINE
            #CheckSquare reads self.matrix, so we have to install candidates now
            self.matrix = grid
            self.visited = self._empty()
            self.state = RUNNING
            if self.Outcome(x, y) == 2:
                return grid

        return grid
    # John - 09/17/2026
    def _Neighbors(self, x, y):
        #The in bounds cells touching (x, y)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.x_size and 0 <= ny < self.y_size:
                    yield (nx, ny)
    # John - 09/17/2026
    # def _IsInstantWin(self, x, y, n):
    #     #True when opening (x, y) on self.matrix would uncover every safe cell at once
    #     #Basically RecOpen but BFS to not break recursion depth
    #     seen = {(x, y)}
    #     queue = deque([(x, y)])
    #     while queue:
    #         cx, cy = queue.popleft()
    #         if self.CheckSquare(cx, cy) != 0:
    #             continue
    #         for nx, ny in self._Neighbors(cx, cy):
    #             if (nx, ny) not in seen:
    #                 seen.add((nx, ny))
    #                 queue.append((nx, ny))
    #     return len(seen) == self.x_size * self.y_size - n

    #Nothing should return matrix, should just use internal
    #UI should only call outcome and flag, use self.matrix
    def Outcome(self, x: int, y: int) -> int: #Get the outcome of the game after a click
        #First written by Nickan on 9/17, commented/type annotated on 9/19
        #Edited by Joshua, Tyler
        #Inputs: Minesweeper object and two coordinates
        #Output: A number equivalent to an outcome
        if self.state != RUNNING: #If the game is not running
            return self.state #Return the game state
        
        if self.visited[x][y] == FLAG: #If the user tries to click on a flag
            self.state = RUNNING #The game is running
            return RUNNING #Ignore the input
        
        if self.matrix[x][y] == MINE: #If the user clicks a mine
            self.visited[x][y] = EXPLODED_MINE #The mine explodes
            self.EndBoard() #The game is over
            self.state = LOSS #The game state is a loss
            self.end_time = time.time()
            return LOSS #Return that the game has been lost
        
        self.RecOpen(x,y) #Otherwise, start opening tiles
        total = sum(self.visited[i].count(UNVISITED) for i in range(len(self.visited))) #Get the number of unvisited tiles
        total += sum(self.visited[i].count(FLAG) for i in range(len(self.visited))) #Add the number of the number of flagged tiles
        if total == sum(self.matrix[i].count(MINE) for i in range(len(self.matrix))): #If all mines are unvisited or flagged 
            self.EndBoard() #The game is over
            self.state = WIN #The game state is a win
            self.end_time = time.time()
            return WIN #Return that the game has been won
        
        return RUNNING #Otherwise, the game continues

    #Lena - 09/17/26
    #This function places and removes flags on the board
    def Flag(self, x, y):
        #If no available flags, don't do anything
        #Places a flag on the square if it's uncovered
        if (self.visited[x][y] is UNVISITED) and self.RemainingMines() > 0:
            self.visited[x][y] = FLAG
        #Remove flag if the square has a flag
        elif (self.visited[x][y] == FLAG):
            self.visited[x][y] = UNVISITED
        #If the flag action is accidentally done on an already uncovered square, do nothing
        else:
            pass
            
    def Elapsed(self):
        end = self.end_time if self.end_time is not None else time.time()
        return end - self.start_time

    #Joshua - 9/19/26
    #This returns a board filled in with NONE values
    def _empty(self):
        return [[UNVISITED] * self.y_size for _ in range(self.x_size)]

    #Tyler - 9/19/26
    #This is used to update the visited board to display mine location at the end of the game
    def EndBoard(self):
        #Loop over all cells in the board
        for i in range(self.x_size):
            for j in range(self.y_size):
                #Updated visited to display all hidden mines
                if self.matrix[i][j] == MINE and self.visited[i][j] != EXPLODED_MINE:
                    self.visited[i][j] = MINE
    #Tyler - 9/19/2026
    def RemainingMines(self):
        #Returns the number of remaining mines calculated as number of mines - number of flags
        #Find the number of mines
        mine_count = sum(row.count(MINE) for row in self.matrix)
        #Find the number of flags placed
        flag_count = sum(row.count(FLAG) for row in self.visited)
        return mine_count - flag_count
