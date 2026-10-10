## Core Features To Test:

* Game Setup

  * First clicked cell is mine-free and is a valid cell (aka cannot click on an invalid coordinate of the UI)

    * Clicking on other areas of the screen that are not on the board - ***PASS***

      * **Does not count as valid initial input**
    * Clicking on the grid coordinate cells (A-J and 0-9) - ***PASS***

      * **Does not count as valid initial input**
    * Right clicking anywhere on the screen - ***PASS***

      * **Attempting to flag as the first move does not count as valid initial input**
  * Mines must be from 10-20 input-wise - ***PASS (Former fail)***

    * **See stress testing below**
    * **The program does currently allow for number of mine values below 10 but greater than 0, which the requirements specified as invalid input**

      * **HAS NOW BEEN PATCHED**
* Gameplay

  * Left-clicking to uncover cells works - ***PASS***

    * **See stress testing for edge-cases**
    * **Base Functionality works - confirmed after several standard baseline tests / simulations of play**
  * Right-clicking to flag and unflag cells works **- *PASS***

    * **See stress testing for edge-cases**
    * **Base Functionality works - confirmed after several standard baseline tests / simulations of play**
  * Uncovering a mine ends a game ***- PASS***

    * **Base Functionality works - confirmed after several standard baseline tests / simulations of play**
  * Neighboring Mine Indicators display the correct value ***- PASS***

    * **Base Functionality works - confirmed after several standard baseline tests / simulations of play. Confirmed based on post-game display**
  * Recursive uncovering works ***- PASS***

    * **Base Functionality works - confirmed after several standard baseline tests / simulations of play. Confirmed based on post-game display**
  * Mine Flagging

    * Covered in above
* Player Interface

  * Display grid is correct in real-time - ***PASS***
* Game Conclusion

  * Loss / Wins works

    * **Base Functionality works - confirmed after several standard baseline tests / simulations of play.**





## Additional Features:

* Timer ***- PASS***

  * No AI

    * Server \& Game Start Time Are Relatively Equal ***- PASS***

      * Starts at first cell uncovering
      * Ends properly upon loss and win, no time added after end
      * Timer reset upon the beginning of another successive game works
    * Server \& Game Start Time Are Offset By A Long Margin ***- PASS***

      * Starts at first cell uncovering
      * Ends properly upon loss and win, no time added after end
      * Timer reset upon the beginning of another successive game works
  * AI

    * Server \& Game Start Time Are Relatively Equal ***- PASS***

      * Starts at first cell uncovering
      * Ends properly upon loss and win, no time added after end
      * Timer reset upon the beginning of another successive game works
    * Server \& Game Start Time Are Offset By A Long Margin ***- PASS***

      * Starts at first cell uncovering
      * Ends properly upon loss and win, no time added after end
      * Timer reset upon the beginning of another successive game works
* AI ***- PASS***

  * Easy - Random uncovering that avoids flagged and uncovered cells ***- PASS***

    * All rules followed at # of mines = 10
    * All rules followed at # of mines = 20
    * All rules followed at # of mines between 10-20
    * Interactive Mode follows the above as well
    * *Bug:* The user can just right-click on a flag to skip their turn - ***HAS BEEN FIXED***
  * Medium - AI flags all hidden neighbors if number of hidden neighbors equals that cell's number AND if number of flagged neighbors of a revealed cell equals that cell's number, AI should open all other hidden neighbors. Otherwise, AI picks random uncovered cell - ***PASS***

    * All rules followed at # of mines = 10
    * All rules followed at # of mines = 20
    * All rules followed at # of mines between 10-20
    * Interactive Mode follows the above as well
    * *Bug:* The user can just right-click on a flag to skip their turn - ***HAS BEEN FIXED***
  * Hard - Medium + 1-2-1 pattern rule. - ***PASS***

    * All rules followed at # of mines = 10
    * All rules followed at # of mines = 20
    * All rules followed at # of mines between 10-20
    * Interactive Mode follows the above as well
    * *Bug:* The user can just right-click on a flag to skip their turn - ***HAS BEEN FIXED***



## Stress Testing:

* Mine Input

  * Large negative numbers - ***PASS***

    * **Does not allow for this input**
  * Negative number - ***PASS***

    * **Does not allow for this input**
  * Zero ***- PASS***

    * **Does not allow for this input**
  * Large positive number that exceeds grid size and/or max mine value of 20 ***- PASS***

    * **Does not allow for this input**
  * Words - ***PASS***

    * **Does not allow for this input**
* User Clicking

  * Mass Left-clicking ***- PASS***

    * **"POST /board HTTP/1.1"** holds under mass clicking, though this may be due to being locally hosted
  * Mass Right-clicking ***- PASS***

    * **"POST /flag HTTP/1.1"** holds under mass clicking, though this may be due to being locally hosted

