## Authors

- **Omer Menchik**: 207811779
- **Amit Levy**: 315031138

# backgammon
Python modules to play backgammon (human or computer)

## System Requirements

- Python 3 (you may need to change the commands below to `python3 ...` if that is how you run python 3 on your machine)

## Platform Overview

The Backgammon platform is a Python-based implementation of the backgammon game. It is designed to allow both human and AI players to compete in various configurations, from single games to full tournaments. The platform provides an intuitive user interface, AI strategy integration, and robust game mechanics to ensure rule compliance and a smooth gaming experience.

---

### Key Functionalities

#### 1. **Board Management (`board.py`)**
   The `Board` class is responsible for managing the state of the backgammon board. It provides functionality to update the board, validate moves, and track the status of the game. Key functions include:
   - **`create_starting_board()`**:
     Initializes the board with the standard starting positions for a backgammon game.
   - **`move_piece(piece, die_roll)`**:
     Moves a piece on the board based on a dice roll while enforcing backgammon rules (e.g., handling blocked positions, capturing opponent pieces).
   - **`export_state()` / `import_state(state)`**:
     Exports and imports the board state in a compact format, allowing for debugging or game restoration.
   - **`has_game_ended()`**:
     Checks if the game has ended by determining if one player has moved all their pieces off the board.

---

#### 2. **Game Flow (`game.py`)**
   The `Game` class orchestrates the flow of a single game, managing player turns, dice rolls, and victory conditions. Key functions include:
   - **`run_game()`**:
     Runs the main game loop, alternating turns between players, validating moves, and detecting game completion.
   - **`get_rolls_to_move(location, requested_move, available_rolls)`**:
     Determines the dice rolls needed to execute a requested move, checking for feasibility and rule compliance.
   - **`who_won()`**:
     Returns the winner of the game once it has concluded.

---

#### 3. **Tournament Mode (`tournament.py`)**
   The tournament mode allows multiple players (human or AI) to compete in a series of games, ultimately determining a champion. Key functions include:
   - **`run_tournament(player_names, player_strategies)`**:
     Manages the tournament, including player matchups, round progression, and winner determination.
   - **`print_tournament_branch(tournament_branch)`**:
     Displays the progression of matchups and winners in the tournament.
   - **`print_tournament_placement(player_names)`**:
     Displays the initial placement of players in the tournament bracket.

---

#### 4. **Single-Player Mode (`single_player.py`)**
   The single-player mode allows a human player to compete against an AI-controlled opponent. Key elements include:
   - **Human vs AI Gameplay**:
     The player chooses a strategy for the AI opponent and sets a time limit for moves.
   - **Integration with `Game` Class**:
     Orchestrates a single game, using the `Game` class to manage moves, dice rolls, and turn-taking.

---

#### 5. **AI Strategies (`strategies.py`)**
   The `Strategy` interface provides a foundation for implementing AI behaviors. Existing strategies include:
   - **`MoveFurthestBackStrategy`**:
     Moves the piece furthest from home, aiming to progress pieces efficiently. This is a medium-difficulty strategy.
   - **`MoveRandomPiece`**:
     Selects a piece and move randomly. This is a simple, easy-difficulty strategy.
   - **`HumanStrategy`**:
     Allows human players to manually input their moves.

---

### Why Use This Platform?

1. **Versatility**:
   - Supports multiple game configurations (human vs human, human vs AI, AI vs AI).
   - Offers single-game and tournament modes.

2. **Robust Implementation**:
   - Enforces all backgammon rules, including move validation, capturing pieces, and endgame detection.

3. **AI Integration**:
   - Includes prebuilt AI strategies of varying difficulty.
   - Provides a flexible framework for creating custom AI strategies.

4. **Debugging Tools**:
   - Compact board state export/import functionality.
   - Comprehensive logging of moves and game status.

This platform is ideal for anyone looking to learn backgammon, experiment with AI strategies, or simulate competitive games.

## How to run the game

* **Human vs Computer**: run `python single_player.py`, then choose the computer strategy to play against

* **Human vs Human**: run `python two_player.py`

* **Computer vs Computer**: run `python main.py` The two 'players' can have different strategies.

* **tournament**: run `python tournament.py`

## Features

1. **Move Validation**:
   - Ensures all moves comply with backgammon rules.
2. **Customizable AI Strategies**:
   - Choose from prebuilt AI strategies or implement your own.
3. **Game Mechanics**:
   - Handles dice rolls, piece movements, and victory conditions.
4. **Tournament Support**:
   - Run tournaments with configurable players and strategies.
5. **Compact State Export/Import**:
   - Save and restore game states for debugging or analysis.

---

## AI Strategies

Each AI strategy is implemented in `strategies.py` and adheres to the `Strategy` interface:

- **MoveFurthestBackStrategy**:
  - Medium difficulty.
  - Prioritizes moving the piece furthest from home.
- **MoveRandomPiece**:
  - Easy difficulty.
  - Chooses a random piece to move.
- **HumanStrategy**:
  - For human players to manually input their moves.

---

## Example Usage

1. **Play a Single Game**:
    python single_player.py
2. **Run a Tournament**:
    python tournament.py

## Example Turn:
What is your name?
omer
Available Strategies:
[0] MoveRandomPiece (Easy)
[1] MoveFurthestBackStrategy (Medium)
[2] CompareAllMovesSimple (Hard)
Pick a strategy:
0
Enter time limit in seconds (or 'inf' for no limit): inf
It is omer's turn, you are white, your roll is [4, 3]
  13                  18   19                  24   25
---------------------------------------------------
| 5B  .   .   .   3W  .  | 5W  .   .   .   .   2B | .  
|                        |                        |
|                        |                        |
|                        |                        |
| 5W  .   .   .   3B  .  | 5B  .   .   .   .   2W | .  
---------------------------------------------------
  12                  7    6                   1    0
You have [4, 3] left
Enter the location of the piece you want to move?
12
How far (or 0 to move another piece)?
3

  13                  18   19                  24   25
---------------------------------------------------
| 5B  .   1W  .   3W  .  | 5W  .   .   .   .   2B | .  
|                        |                        |
|                        |                        |
|                        |                        |
| 4W  .   .   .   3B  .  | 5B  .   .   .   .   2W | .  
---------------------------------------------------
  12                  7    6                   1    0
You have [4] left
Enter the location of the piece you want to move?
15
How far (or 0 to move another piece)?
4

Done!
It is omer's turn, you are white, your roll is [2, 1]
  13                  18   19                  24   25
---------------------------------------------------
| 3B  .   .   .   3W  .  | 6W  .   .   .   .   2B | .  
|                        |                        |
|                        |                        |
|                        |                        |
| 4W  .   .   .   4B  1B | 5B  .   .   .   .   2W | .  
---------------------------------------------------
  12                  7    6                   1    0
You have [2, 1] left
Enter the location of the piece you want to move?


## Future Enhancements

1. **Heuristic-Based AI**:
   - Add a Minimax algorithm with heuristic evaluation.

2. **Monte Carlo Tree Search**:
   - Implement advanced AI search techniques.

3. **Improved GUI**:
   - Enhance the graphical interface for better visualization and interaction.
