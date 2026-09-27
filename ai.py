#ai.py
"""
Not much code yet
Ideas:
    In main.py setupgame, this is when we init ai, ask difficulty and if interactive mode
        This means in index.html we need to implement a UI element that will send main.py the mode and difficulty, which will init ai.py
        Also in index.html we need a UI element that says "AI's turn" or "Player's Turn"
    In main.py we can create a new @app.post for the AI specifically for when it is the AI's turn
        /board and /flag can be just for the human (although probably need to add safety for "you cannot play it is the ai's turn" and swapping the turn to the AI from the human)
    In ai.py, we pass in the difficulty and board, we will return our clicks given the visible state of the board.
        board.visited will contain what the AI knows and we update by doing .outcome() method
        board.visited will return values of adjacent mines and will return None for unmarked cells
"""
from Minesweeper import Minesweeper
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

        
    #returns a list of len() == 3, a list that had mode (0 for click 1 for flag) and coordinates (x, y)
    def easyTurn(self) -> list:
        pass
    def mediumTurn(self) -> list:
        pass
    def hardTurn(self) -> list:
        pass