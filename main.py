"""
Main entry point for Connect Four MCTS algorithms
CS 4320 PA3: Game Playing with UCT

Command line usage:
    python main.py <input_file> <Verbose|Brief|None> <parameter>

Example:
    python main.py test1.txt Verbose 0
    python main.py test4.txt Brief 500
"""

import sys
from connect_four import ConnectFour
from algorithm1_ur import UniformRandom
from algorithm2_pmcgs import PMCGS
from algorithm3_uct import UCT


def main():
    """Main function to run the MCTS algorithms."""
    if len(sys.argv) != 4:
        print("Usage: python main.py <input_file> <Verbose|Brief|None> <parameter>")
        sys.exit(1)

    input_file = sys.argv[1]
    verbosity = sys.argv[2]
    parameter = int(sys.argv[3])

    # Validate verbosity
    if verbosity not in ["Verbose", "Brief", "None"]:
        print("Error: Verbosity must be 'Verbose', 'Brief', or 'None'")
        sys.exit(1)

    # Load game state from file
    try:
        game, algorithm, player = ConnectFour.from_file(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Validate player
    if player not in ["R", "Y"]:
        print(f"Error: Invalid player '{player}'. Must be 'R' or 'Y'")
        sys.exit(1)

    # Set verbosity
    verbose = verbosity == "Verbose"
    brief = verbosity == "Brief"
    # suppress_output is only for tournaments, not for "None" mode
    # "None" mode still shows final move, just not intermediate details
    suppress_output = False

    # Run appropriate algorithm
    if algorithm == "UR":
        if parameter != 0:
            print("Warning: Parameter should be 0 for UR algorithm")

        algo = UniformRandom(game, player, 0, verbose, brief, suppress_output)
        algo.select_move()

    elif algorithm == "PMCGS":
        if parameter <= 0:
            print("Error: Parameter must be positive for PMCGS")
            sys.exit(1)

        algo = PMCGS(game, player, parameter, verbose, brief, suppress_output)
        algo.select_move()

    elif algorithm == "UCT":
        if parameter <= 0:
            print("Error: Parameter must be positive for UCT")
            sys.exit(1)

        algo = UCT(game, player, parameter, verbose, brief, suppress_output)
        algo.select_move()

    else:
        print(
            f"Error: Unknown algorithm '{algorithm}'. Must be 'UR', 'PMCGS', or 'UCT'"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
