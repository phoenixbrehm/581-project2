#ai.py
"""
Ideas:
    In main.py setupgame, this is when we init ai, ask difficulty and if interactive mode (main will deal with interactive mode)
        This means in index.html we need to implement a UI element that will send main.py the mode and difficulty, which will init ai.py
        Also in index.html we need a UI element that says "AI's turn" or "Player's Turn"
    In main.py we can create a new @app.post for the AI specifically for when it is the AI's turn
        /board and /flag can be just for the human (although probably need to add safety within those methods for "you cannot play it is the ai's turn" and swapping the turn to the AI from the human)
    In ai.py, we pass in the difficulty and board, we will return our clicks given the visible state of the board.
        board.visited will contain what the AI knows and we update by doing .outcome() method
        board.visited will return values of adjacent mines and will return None for unmarked cells
"""
from Minesweeper import Minesweeper
import random
class AISolver:
    def __init__(self, difficulty: int, minesweeper: Minesweeper):
        """
        difficulty is an int
        0 = Easy
        1 = Medium
        2 = Hard
        """
        self.difficulty = difficulty
        self.board = minesweeper

    def takeTurn(self):
        if(self.difficulty == 0): #easy
            return self.easyTurn()
        elif(self.difficulty == 1): #medium
            return self.mediumTurn()
        elif(self.difficulty == 2): #hard
            return self.hardTurn()

        
    #returns a list of lists of len() == 3, a list that had mode (0 for click 1 for flag) and coordinates (x, y), each interior list is the list of moves to be made
    def easyTurn(self) -> list[list]:
        candidates = []
        for x in range(self.board.x_size):
            for y in range(self.board.y_size):
                if self.board.visited[x][y] is None:
                    candidates.append((x, y))
        x, y = random.choice(candidates)
        return [[0, x, y]]

    def _mediumRules(self):
        for x in range(self.board.x_size):
            for y in range(self.board.y_size):
                checkingCell = self.board.visited[x][y] #value is number of neighboring mines
                if checkingCell is None or checkingCell < 0: #<0 would be flags or other special values
                    continue #if covered or flag or special, do nothing and go to next cell
                hidden_neighbors = []
                flagged_neighbors = []
                for nx, ny in self.board._Neighbors(x, y):
                    if self.board.visited[nx][ny] == -1:
                        flagged_neighbors.append((nx, ny))
                    elif self.board.visited[nx][ny] is None:
                        hidden_neighbors.append((nx, ny))
                remaining_mines = checkingCell - len(flagged_neighbors)
                if remaining_mines == len(hidden_neighbors) and remaining_mines > 0:
                    ret_n = []
                    for elem in hidden_neighbors:
                        ret_n.append([1, elem[0], elem[1]])
                    return ret_n
                if remaining_mines == 0 and len(hidden_neighbors) > 0:
                    ret_n = []
                    for elem in hidden_neighbors:
                        ret_n.append([0, elem[0], elem[1]])
                    return ret_n
        return None
    def mediumTurn(self) -> list[list]:
        moves = self._mediumRules()
        if moves is None:
            return self.easyTurn()
        else:
            return moves


    def hardTurn(self) -> list[list]:
        moves = self._mediumRules()
        if moves is not None:
            return moves
        for x in range(self.board.x_size):
            for y in range(self.board.y_size - 2):
                c1 = self.board.visited[x][y]
                c2 = self.board.visited[x][y+1]
                c3 = self.board.visited[x][y+2]
                if c1 == 1 and c2 == 2 and c3 == 1:
                    #check if none on one side and not none on the other
                    nxd = x-1
                    nxu = x+1
                    if 0 <= nxd and nxu < self.board.x_size:
                        if(self.board.visited[nxd][y] is None and
                           self.board.visited[nxd][y+1] is None and
                           self.board.visited[nxd][y+2] is None and
                           self.board.visited[nxu][y] >= 0 and
                           self.board.visited[nxu][y+1] >= 0 and
                           self.board.visited[nxu][y+2] >= 0):
                            return [[1, nxd, y], [0, nxd, y+1], [1, nxd, y+2]]
                        if(self.board.visited[nxu][y] is None and
                           self.board.visited[nxu][y+1] is None and
                           self.board.visited[nxu][y+2] is None and
                           self.board.visited[nxd][y] >= 0 and
                           self.board.visited[nxd][y+1] >= 0 and
                           self.board.visited[nxd][y+2] >= 0):
                            return [[1, nxu, y], [0, nxu, y+1], [1, nxu, y+2]]

        for x in range(self.board.x_size - 2):
            for y in range(self.board.y_size):
                c1 = self.board.visited[x][y]
                c2 = self.board.visited[x+1][y]
                c3 = self.board.visited[x+2][y]
                if c1 == 1 and c2 == 2 and c3 == 1:
                    #check if none on one side and not none on the other
                    nyl = y-1
                    nyr = y+1
                    if 0 <= nyl and nyr < self.board.y_size:
                        if(self.board.visited[x][nyl] is None and
                           self.board.visited[x+1][nyl] is None and
                           self.board.visited[x+2][nyl] is None and
                           self.board.visited[x][nyr] >= 0 and
                           self.board.visited[x+1][nyr] >= 0 and
                           self.board.visited[x+2][nyr] >= 0):
                            return [[1, x, nyl], [0, x+1, nyl], [1, x+2, nyl]]
                        if(self.board.visited[x][nyr] is None and
                           self.board.visited[x+1][nyr] is None and
                           self.board.visited[x+2][nyr] is None and
                           self.board.visited[x][nyl] >= 0 and
                           self.board.visited[x+1][nyl] >= 0 and
                           self.board.visited[x+2][nyl] >= 0):
                            return [[1, x, nyr], [0, x+1, nyr], [1, x+2, nyr]]
        return self.easyTurn()