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

from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Minesweeper import Minesweeper
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/sounds", StaticFiles(directory="frontend/sounds"), name="sounds")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

game = None
mine_count = 10

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
    
    # the mine_count given is assigned
    mine_count = setup.n
    # and the game state is reverted to None to prepare for a new game
    game = None

# Trey - 09/17/26 and 09/18/26
# endpoint that takes the x and y information of a click, handles the initialization of the game
# game state if neccessary, passes of the information as to determine the outcome of the game
# and hands back an updated board, the result of the game, and the remaining mines.
@app.post("/board")
def boardUpdate(click: clickRequest):
    # the global variable tracked across the file for the game state
    global game

    # if the game is not initialized
    if game is None:
        # initialized it using the mine_count determined in setup, and provide the x and y 
        # cordinates for the cell clicked
        game = Minesweeper(click.x,click.y,mine_count)

    # pass of the information about the cell click and store the information about the result
    result = game.Outcome(click.x, click.y)

    return {
            "board": game.visited, # return the board that was updated by backend processes
            "result": result, # return the retrieved result
            "mines": game.RemainingMines() # return the count of remaining mines
            }

# Trey - 09/17/26
# endpoint that takes x and y information of a click, returns an updated board after the placed flag
# and the remaining number of mines
@app.post("/flag")
def flagCell(click: clickRequest):
    # if the game exists
    if game:
        # then pass the click information to the Flag function
        game.Flag(click.x, click.y)
        return {
            "board": game.visited, # return the updated board state
            "mines": game.RemainingMines() # and the count of remaining mines
            }
    else:
        raise HTTPException(status_code=404, detail="Board not found")
