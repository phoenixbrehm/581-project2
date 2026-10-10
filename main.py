#Prologue Comment
#Module: Main.py
#Description: Contains FastAPI application that connects frontend to Minesweeper logic. It ahndles API request for board control/input.
#Input: Inital Mine Count -> mine_count; x,y coordinates for clicks
#Output:    returns JSON payload containing board state, game state, and remaining mine count

#Authors:
#   Joshua Lin
#   Tyler Oswald
#   Trey Timko
#Creation Date:
#   September 17, 2026


"""
Project 2 Authors
Phoenix Brehm
Collin Tullis

Last Updated - 10/10/26

Added interaction with the AI, return time elapsed, and new post method for the AI.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Minesweeper import Minesweeper
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from ai import AISolver

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

game = None
ai_solver = None
mine_count = 10
current_turn = "player" #player or ai
interactive_mode = False

# Trey - 09/17/26
# pydantic schemas
# this ensures the data from the frontend is modeled correctly
class clickRequest(BaseModel):
    # clickRequest is the model of a request sent upon every user click
    
    # it holds the x value of the click
    x: int
    # as well as the y
    y: int

class setupRequest(BaseModel):
    # setup request is the model of a request that needs a new board setup

    # it takes the desired minecount of the user
    n: int
    difficulty: str = "off"
    interactive: bool = False

# fastapi endpoints to be used

# Trey - 09/17/26
# endpoint to provide the frontend
@app.get("/")
def index():
    # when accessing the "/" endpoint of the server index.html is returned
    # as to be rendered in the users browser
    return FileResponse("frontend/index.html")

# Trey - 09/17/26 and 09/18/26
# endpoint that takes the mine configuration value and resets the game state to prepare for a new game
@app.post("/setup")
def setupGame(setup: setupRequest):
    # because this file keeps track of the users specified mine_count
    # and the game state, the global variables are used in this function
    global mine_count
    global game
    global ai_solver
    global current_turn
    global interactive_mode
    
    # the mine_count given is assigned
    mine_count = setup.n
    interactive_mode = setup.interactive
    current_turn = "player"
    # and the game state is reverted to None to prepare for a new game
    game = None
    if setup.difficulty != "off":
        diffic_map = {"easy": 0, "medium": 1, "hard": 2}
        diffic_val = diffic_map.get(setup.difficulty, 0)
        ai_solver = {"difficulty": diffic_val, "active": True}
    else:
        ai_solver = None

# Trey - 09/17/26 and 09/18/26
# endpoint that takes the x and y information of a click, handles the initialization of the game
# game state if neccessary, passes of the information as to determine the outcome of the game
# and hands back an updated board, the result of the game, and the remaining mines.
@app.post("/board")
def boardUpdate(click: clickRequest):
    # the global variable tracked across the file for the game state
    global game
    global ai_solver
    global current_turn

    # if the game is not initialized
    if game is None:
        # initialized it using the mine_count determined in setup, and provide the x and y 
        # cordinates for the cell clicked
        game = Minesweeper(click.x,click.y,mine_count)
        if ai_solver and isinstance(ai_solver, dict):
            ai_solver = AISolver(ai_solver["difficulty"], game)
    cellval = game.visited[click.x][click.y]
    # pass of the information about the cell click and store the information about the result
    result = game.Outcome(click.x, click.y)
    if ai_solver and result == 2:
        if cellval is not None: #is used to not pass the turn if the player clicks on an already uncovered cell
            current_turn = "player"
        else:
            current_turn = "ai"
    return {
            "board": game.visited, # return the board that was updated by backend processes
            "result": result, # return the retrieved result
            "mines": game.RemainingMines(), # return the count of remaining mines
            "elapsed": game.Elapsed(), #return the elapsed time
            "turn": current_turn #returns whose turn it is
            }

# Trey - 09/17/26
# endpoint that takes x and y information of a click, returns an updated board after the placed flag
# and the remaining number of mines
@app.post("/flag")
def flagCell(click: clickRequest):
    # if the game exists
    global game
    global current_turn
    global ai_solver
    if game:
        # then pass the click information to the Flag function
        game.Flag(click.x, click.y)
        cellval = game.visited[click.x][click.y]
        if cellval == -1:
            if ai_solver and current_turn == "player": #swap turn from player
                current_turn = "ai"
        else:
            current_turn = "player"
        return {
            "board": game.visited, # return the updated board state
            "mines": game.RemainingMines(), # and the count of remaining mines
            "turn": current_turn
            }
    else:
        raise HTTPException(status_code=404, detail="Board not found")

#endpoint that runs the AI solver
@app.post("/ai-turn")
def aiTurn():
    global game
    global ai_solver
    global current_turn
    if game is None:
        game = Minesweeper(0, 0, mine_count) #inits game if no game is found for non-interactive mode
        if ai_solver and isinstance(ai_solver, dict):
            ai_solver = AISolver(ai_solver["difficulty"], game)
    if ai_solver is None or isinstance(ai_solver, dict):
        raise HTTPException(status_code=400, detail="AI or game not properly initialized")

    moves = ai_solver.takeTurn()

    result = 2
    for mode, x, y in moves: #performs moves obtained
        if mode == 0:
            result = game.Outcome(x, y)
        elif mode == 1:
            game.Flag(x, y)
        if result != 2:
            break

    if result == 2:
        current_turn = "ai" if not interactive_mode else "player" #swaps turn or not.

    return {
        "board": game.visited,
        "result": result,
        "mines": game.RemainingMines(),
        "elapsed": game.Elapsed(),
        "turn": current_turn
    }