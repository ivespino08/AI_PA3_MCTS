"""
Algorithm 1: Uniform Random (UR)
CS 4320 PA3: Game Playing with UCT

This module implements the Uniform Random algorithm that selects a legal move uniformly at random.
"""

import random
import math
from typing import Dict, List, Optional, Tuple
from connect_four import ConnectFour


class MCTSNode:
    """
    Represents a node in the Monte Carlo Tree Search.

    Each node stores:
    - wi: Total wins accumulated from simulations
    - ni: Number of simulations that passed through this node
    - children: Dictionary mapping moves (column numbers) to child nodes
    - parent: Reference to parent node (None for root)
    - move: The move that led to this node (None for root)
    """

    def __init__(self, parent: Optional["MCTSNode"] = None, move: Optional[int] = None):
        """
        Initialize a new MCTS node.

        Args:
            parent: Parent node (None for root)
            move: The move that led to this node (None for root)
        """
        self.wi = 0  # Total wins
        self.ni = 0  # Number of visits
        self.children: Dict[int, "MCTSNode"] = {}
        self.parent = parent
        self.move = move

    def get_value(self) -> float:
        """
        Get the average value of this node.

        Returns:
            Average value (wi/ni), or 0.0 if node hasn't been visited
            Value is clamped to [-1, 1] range
        """
        if self.ni == 0:
            return 0.0
        value = self.wi / self.ni
        # Clamp to valid range [-1, 1]
        return max(-1.0, min(1.0, value))

    def is_fully_expanded(self, legal_moves: List[int]) -> bool:
        """
        Check if all legal moves have been explored.

        Args:
            legal_moves: List of legal moves from this state

        Returns:
            True if all legal moves have children nodes
        """
        return len(self.children) == len(legal_moves)

    def get_ucb_value(
        self, exploration_constant: float = math.sqrt(2), is_max_player: bool = True
    ) -> float:
        """
        Calculate UCB (Upper Confidence Bound) value for this node.

        Args:
            exploration_constant: Exploration constant (default sqrt(2))
            is_max_player: True if this node represents a max player move

        Returns:
            UCB value for this node
        """
        if self.ni == 0:
            return float("inf") if is_max_player else float("-inf")

        # Safety check: parent should have been visited
        if self.parent is None or self.parent.ni == 0:
            return self.get_value()

        exploitation = self.get_value()
        exploration = exploration_constant * math.sqrt(
            math.log(self.parent.ni) / self.ni
        )

        if is_max_player:
            return exploitation + exploration
        else:
            return exploitation - exploration


class MCTSAlgorithm:
    """
    Base class for Monte Carlo Tree Search algorithms.
    """

    def __init__(
        self,
        game: ConnectFour,
        player: str,
        num_simulations: int,
        verbose: bool = False,
        brief: bool = False,
        suppress_output: bool = False,
    ):
        """
        Initialize the MCTS algorithm.

        Args:
            game: Initial game state
            player: Player to make the move ('R' or 'Y')
            num_simulations: Number of simulations to run
            verbose: Whether to print detailed output
            brief: Whether to print brief output (column values and final move)
            suppress_output: If True, suppress all output (for tournaments)
        """
        self.game = game
        self.player = player
        self.num_simulations = num_simulations
        self.verbose = verbose
        self.brief = brief
        self.suppress_output = suppress_output
        self.root = MCTSNode()

        # Determine if player is max or min
        self.is_max_player = player == "Y"
        self.opponent = "R" if player == "Y" else "Y"

    def select_move(self) -> int:
        """
        Select the best move based on simulations.

        Returns:
            Column number (1-indexed) of the selected move
        """
        raise NotImplementedError("Subclasses must implement select_move")

    def simulate(self, game: ConnectFour, current_player: str) -> int:
        """
        Run a random simulation from the given game state.

        Args:
            game: Current game state
            current_player: Player whose turn it is

        Returns:
            Game result: -1 (Red wins), 0 (draw), or 1 (Yellow wins)
        """
        # Make random moves until terminal state
        while True:
            is_terminal, value = game.is_terminal()
            if is_terminal:
                return value if value is not None else 0

            legal_moves = game.get_legal_moves()
            if len(legal_moves) == 0:
                return 0

            # Random move
            move = random.choice(legal_moves)
            game.make_move(move, current_player)

            # Switch player
            current_player = "R" if current_player == "Y" else "Y"

    def backpropagate(self, node: MCTSNode, value: int):
        """
        Backpropagate the simulation result up the tree.

        The value is the terminal game result: -1 (Red wins), 0 (draw), or 1 (Yellow wins).
        As we go up the tree, we need to convert this to each node's perspective.

        Args:
            node: Node to update (leaf node where simulation ended)
            value: Terminal game result (-1, 0, or 1)
        """
        # Ensure value is in valid range
        value = max(-1, min(1, value))

        current = node
        depth = 0

        while current is not None:
            current.ni += 1

            # Determine whose perspective this node represents
            # Root is the player making the move
            # Each level alternates players
            is_max_at_depth = (depth % 2 == 0) == self.is_max_player

            # Convert value to this node's perspective
            if is_max_at_depth:
                # Max player: positive values are good
                current.wi += value
            else:
                # Min player: negative values are good (so flip)
                current.wi -= value

            current = current.parent
            depth += 1


class UniformRandom(MCTSAlgorithm):
    """
    Uniform Random algorithm: selects a legal move uniformly at random.
    """

    def select_move(self) -> int:
        """Select a random legal move."""
        legal_moves = self.game.get_legal_moves()
        if len(legal_moves) == 0:
            return 1  # Should not happen in valid game states

        move = random.choice(legal_moves)
        # Always print final move (unless suppress_output is True for tournaments)
        if not self.suppress_output:
            print(f"FINAL Move selected: {move}")
        return move

