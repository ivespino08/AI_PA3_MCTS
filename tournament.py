"""
Tournament System for Part II
CS 4320 PA3: Game Playing with UCT

Runs round-robin tournament between different algorithm configurations.
"""

import sys
from connect_four import ConnectFour
from algorithm1_ur import UniformRandom
from algorithm2_pmcgs import PMCGS
from algorithm3_uct import UCT


class Tournament:
    """
    Manages tournament between different algorithm configurations.
    """

    def __init__(self, num_games: int = 100):
        """
        Initialize tournament.

        Args:
            num_games: Number of games to play between each pair
        """
        self.num_games = num_games
        self.algorithms = [
            ("UR", 0),
            ("PMCGS", 500),
            ("PMCGS", 10000),
            ("UCT", 500),
            ("UCT", 10000),
        ]
        self.results = {}  # (algo1, algo2) -> (wins_algo1, wins_algo2, draws)

    def play_game(
        self,
        algo1_name: str,
        algo1_param: int,
        algo2_name: str,
        algo2_param: int,
        algo1_starts: bool = False,
    ) -> str:
        """
        Play a single game between two algorithms.

        Args:
            algo1_name: Name of first algorithm
            algo1_param: Parameter for first algorithm
            algo2_name: Name of second algorithm
            algo2_param: Parameter for second algorithm
            algo1_starts: If True, algo1 (Red) goes first; if False, algo2 (Yellow) goes first

        Returns:
            'algo1' if algo1 wins, 'algo2' if algo2 wins, 'draw' if draw
        """
        # Start with empty board
        game = ConnectFour()
        current_player = "R" if algo1_starts else "Y"  # Alternate who starts

        while True:
            # Check for terminal state
            is_terminal, value = game.is_terminal()
            if is_terminal:
                if value == 1:
                    return "algo2"  # Yellow (algo2) wins
                elif value == -1:
                    return "algo1"  # Red (algo1) wins
                else:
                    return "draw"

            # Select move based on current player
            # Use the game directly - algorithms use do/undo pattern internally
            if current_player == "Y":
                # Yellow player (algo2)
                algo = self._create_algorithm(algo2_name, algo2_param, game, "Y")
            else:
                # Red player (algo1)
                algo = self._create_algorithm(algo1_name, algo1_param, game, "R")

            move = algo.select_move()

            # Make move on the actual game state
            game.make_move(move, current_player)

            # Switch player
            current_player = "R" if current_player == "Y" else "Y"

    def _create_algorithm(
        self, algo_name: str, param: int, game: ConnectFour, player: str
    ):
        """
        Create an algorithm instance.

        Args:
            algo_name: Algorithm name
            param: Algorithm parameter
            game: Game state
            player: Player to move

        Returns:
            Algorithm instance
        """
        if algo_name == "UR":
            return UniformRandom(
                game, player, 0, verbose=False, brief=False, suppress_output=True
            )
        elif algo_name == "PMCGS":
            return PMCGS(
                game, player, param, verbose=False, brief=False, suppress_output=True
            )
        elif algo_name == "UCT":
            return UCT(
                game, player, param, verbose=False, brief=False, suppress_output=True
            )
        else:
            raise ValueError(f"Unknown algorithm: {algo_name}")

    def run_tournament(self):
        """Run the full round-robin tournament."""
        print("Starting tournament...")
        print(f"Playing {self.num_games} games between each pair\n")

        total_combinations = len(self.algorithms) * len(self.algorithms)
        combo_num = 0

        for i, (algo1_name, algo1_param) in enumerate(self.algorithms):
            for j, (algo2_name, algo2_param) in enumerate(self.algorithms):
                combo_num += 1
                print(
                    f"Combination {combo_num}/{total_combinations}: {algo1_name}({algo1_param}) vs {algo2_name}({algo2_param})"
                )

                wins_algo1 = 0
                wins_algo2 = 0
                draws = 0

                for game_num in range(self.num_games):
                    if (game_num + 1) % 20 == 0:
                        print(f"  Game {game_num + 1}/{self.num_games}...")

                    # Alternate who goes first for fairness
                    algo1_starts = game_num % 2 == 0
                    result = self.play_game(
                        algo1_name, algo1_param, algo2_name, algo2_param, algo1_starts
                    )

                    if result == "algo1":
                        wins_algo1 += 1
                    elif result == "algo2":
                        wins_algo2 += 1
                    else:
                        draws += 1

                self.results[(algo1_name, algo1_param, algo2_name, algo2_param)] = (
                    wins_algo1,
                    wins_algo2,
                    draws,
                )

                print(
                    f"  Results: {algo1_name}({algo1_param}): {wins_algo1} wins, "
                    f"{algo2_name}({algo2_param}): {wins_algo2} wins, "
                    f"Draws: {draws}\n"
                )

        self.print_results()

    def print_results(self):
        """Print tournament results in table format."""
        print("\n" + "=" * 80)
        print("TOURNAMENT RESULTS")
        print("=" * 80)
        print("\nWin percentages (row vs column):\n")

        # Header
        header = "Algorithm".ljust(20)
        for algo_name, algo_param in self.algorithms:
            header += f"{algo_name}({algo_param})".ljust(15)
        print(header)
        print("-" * (20 + 15 * len(self.algorithms)))

        # Rows
        for i, (algo1_name, algo1_param) in enumerate(self.algorithms):
            row = f"{algo1_name}({algo1_param})".ljust(20)

            for j, (algo2_name, algo2_param) in enumerate(self.algorithms):
                if i == j:
                    # Self-play: should be 50% (or marked as N/A)
                    row += "N/A".ljust(15)
                else:
                    # Find result - always use the key as stored
                    key = (algo1_name, algo1_param, algo2_name, algo2_param)
                    if key in self.results:
                        wins1, wins2, draws = self.results[key]
                        total = wins1 + wins2 + draws
                        pct = (wins1 / total * 100) if total > 0 else 0.0
                    else:
                        # If not found, try reverse (shouldn't happen with all combinations)
                        key = (algo2_name, algo2_param, algo1_name, algo1_param)
                        if key in self.results:
                            wins2, wins1, draws = self.results[key]
                            total = wins1 + wins2 + draws
                            pct = (wins1 / total * 100) if total > 0 else 0.0
                        else:
                            pct = 0.0

                    row += f"{pct:.1f}%".ljust(15)

            print(row)

        print("\n" + "=" * 80)


def main():
    """Main function for tournament."""
    num_games = 100
    if len(sys.argv) > 1:
        try:
            num_games = int(sys.argv[1])
        except ValueError:
            print("Usage: python tournament.py [num_games]")
            print("Default: 100 games per pair")
            sys.exit(1)

    tournament = Tournament(num_games)
    tournament.run_tournament()


if __name__ == "__main__":
    main()
