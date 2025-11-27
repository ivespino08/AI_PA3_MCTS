# CS 4320 PA3: Game Playing with UCT

## Project Overview

This project implements Monte Carlo Tree Search (MCTS) algorithms for playing Connect Four, including:
1. **Uniform Random (UR)**: Baseline algorithm that selects moves uniformly at random
2. **Pure Monte Carlo Game Search (PMCGS)**: MCTS with random selection in the tree
3. **Upper Confidence bound for Trees (UCT)**: MCTS with UCB for intelligent node selection

## Files

- `connect_four.py`: Connect Four game board and game logic implementation
- `mcts.py`: MCTS node class and three algorithm implementations
- `main.py`: Command-line interface for Part I
- `tournament.py`: Tournament system for Part II
- `README.md`: This file

## Part I: Algorithms for Selecting Moves

### Usage

```bash
python main.py <input_file> <Verbose|Brief|None> <parameter>
```

### Examples

```bash
# Uniform Random
python main.py test1.txt Verbose 0

# Pure Monte Carlo Game Search with 500 simulations
python main.py test4.txt Brief 500

# UCT with 10000 simulations
python main.py test4.txt None 10000
```

### Input File Format

The input file should have the following format:
- Line 1: Algorithm name (`UR`, `PMCGS`, or `UCT`)
- Line 2: Player to move (`R` for Red or `Y` for Yellow)
- Lines 3-8: Board state (6 rows, 7 columns)
  - `R` = Red piece
  - `Y` = Yellow piece
  - `O` = Empty space

Example:
```
UR
R
OOOOOOO
OOOOOOO
OOYOOOY
OOROOOY
OYRYOYR
YRRYORR
```

### Output

- **Verbose**: Detailed output showing each simulation step
- **Brief**: Shows column values and final move selection
- **None**: Only shows final move selection (for tournaments)

## Part II: Algorithm Tournaments

### Usage

```bash
python tournament.py [num_games]
```

Default: 100 games per pair

### Tournament Configuration

The tournament runs a round-robin between:
1. UR (Uniform Random)
2. PMCGS (500 simulations)
3. PMCGS (10000 simulations)
4. UCT (500 simulations)
5. UCT (10000 simulations)

### Output

The tournament prints a table showing win percentages for each algorithm pair.

## Implementation Details

### Game Representation
- Board: 7 columns × 6 rows
- Red (R) = Min player (value -1)
- Yellow (Y) = Max player (value 1)
- Draw = 0

### MCTS Components
- **Selection**: Traverse tree using UCB (UCT) or random (PMCGS)
- **Expansion**: Add new node when reaching unexplored state
- **Simulation**: Random playout to terminal state
- **Backpropagation**: Update node statistics up the tree

### Performance Optimizations
- Efficient win checking (only checks lines through last move)
- Do/undo moves instead of copying entire board
- Tree nodes only store statistics (wi, ni), not full board state
- Output suppression for tournament play

## Notes

- The implementation uses efficient memory management to handle large numbers of simulations
- Win checking is optimized to only examine lines through the last move
- The backpropagation correctly handles alternating player perspectives

## Testing

Test files can be created following the input format described above. The algorithms have been tested with various board configurations and simulation counts.

