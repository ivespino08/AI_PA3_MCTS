"""
Algorithm 3: Upper Confidence bounds applied to Trees (UCT)
CS 4320 PA3: Game Playing with UCT

This module implements Upper Confidence bound for Trees: MCTS with UCB for node selection.
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


class UCT(MCTSAlgorithm):
    """
    Upper Confidence bound for Trees: MCTS with UCB for node selection.
    """

    def __init__(
        self,
        game: ConnectFour,
        player: str,
        num_simulations: int,
        verbose: bool = False,
        brief: bool = False,
        exploration_constant: float = math.sqrt(2),
        suppress_output: bool = False,
    ):
        """
        Initialize UCT algorithm.

        Args:
            exploration_constant: UCB exploration constant (default sqrt(2))
            brief: Whether to print brief output
            suppress_output: If True, suppress all output (for tournaments)
        """
        super().__init__(game, player, num_simulations, verbose, brief, suppress_output)
        self.exploration_constant = exploration_constant

    def select_move(self) -> int:
        """
        Run UCT algorithm and select best move.

        Returns:
            Selected column number (1-indexed)
        """
        for _ in range(self.num_simulations):
            # Selection: traverse tree using UCB until leaf
            # Optimization: use do/undo moves instead of copying board
            node = self.root
            current_player = self.player
            moves_to_undo = []  # Track moves for undo

            # Selection and expansion phase
            # Optimize: check legal_moves first (faster than full terminal check)
            legal_moves = self.game.get_legal_moves()
            while len(legal_moves) > 0:
                # Check for win only if we have moves (optimization)
                is_terminal, _ = self.game.is_terminal()
                if is_terminal:
                    break

                # Check if node is fully expanded
                if node.is_fully_expanded(legal_moves):
                    # Select using UCB
                    best_move = None
                    best_ucb = float("-inf") if current_player == "Y" else float("inf")

                    ucb_values = {}
                    # Calculate UCB for all children (when fully expanded, all legal moves are children)
                    for move in legal_moves:
                        child = node.children[move]
                        is_max = current_player == "Y"
                        ucb = child.get_ucb_value(self.exploration_constant, is_max)
                        ucb_values[move] = ucb

                        if current_player == "Y":
                            # Max player: choose highest UCB
                            if ucb > best_ucb:
                                best_ucb = ucb
                                best_move = move
                        else:
                            # Min player: choose lowest UCB
                            if ucb < best_ucb:
                                best_ucb = ucb
                                best_move = move

                    if self.verbose:
                        print(f"wi: {node.wi}")
                        print(f"ni: {node.ni}")
                        # Print UCB values for all children (sorted by column number)
                        # When fully expanded, all legal moves are children
                        for col in sorted(legal_moves):
                            print(f"V{col}: {ucb_values[col]:.2f}")
                        print(f"Move selected: {best_move}\n")

                    move = best_move
                    node = node.children[move]
                    # Make move
                    self.game.make_move(move, current_player)
                    moves_to_undo.append(move)
                    current_player = "R" if current_player == "Y" else "Y"
                else:
                    # Expansion: add new node
                    unexplored = [m for m in legal_moves if m not in node.children]
                    move = random.choice(unexplored)

                    if self.verbose:
                        print(f"wi: {node.wi}")
                        print(f"ni: {node.ni}")
                        print(f"Move selected: {move}\n")

                    new_node = MCTSNode(parent=node, move=move)
                    node.children[move] = new_node
                    node = new_node

                    if self.verbose:
                        print("NODE ADDED\n")

                    # Make move and switch to rollout
                    self.game.make_move(move, current_player)
                    moves_to_undo.append(move)
                    current_player = "R" if current_player == "Y" else "Y"
                    break

                # Update legal_moves for next iteration
                legal_moves = self.game.get_legal_moves()

            # Rollout: random simulation (optimized - use do/undo instead of copy)
            rollout_moves = []
            legal_moves = self.game.get_legal_moves()

            while len(legal_moves) > 0:
                # Check for win only if we have moves (optimization)
                is_terminal, _ = self.game.is_terminal()
                if is_terminal:
                    break

                move = random.choice(legal_moves)
                self.game.make_move(move, current_player)
                rollout_moves.append(move)
                current_player = "R" if current_player == "Y" else "Y"
                legal_moves = self.game.get_legal_moves()

            # Get terminal value
            _, terminal_value = self.game.is_terminal()
            if terminal_value is None:
                terminal_value = 0

            if self.verbose:
                for m in rollout_moves:
                    print(f"Move selected: {m}")
                print(f"TERMINAL NODE VALUE: {terminal_value}\n")

            # Undo all rollout moves (in reverse order)
            for move in reversed(rollout_moves):
                self.game.undo_move(move)

            # Undo all moves made during selection/expansion
            for move in reversed(moves_to_undo):
                self.game.undo_move(move)

            # Backpropagate
            self.backpropagate(node, terminal_value)

            if self.verbose:
                # Print updated values up the path
                path = []
                n = node
                while n is not None:
                    path.append(n)
                    n = n.parent
                path.reverse()

                for n in path[1:]:  # Skip root
                    print("Updated values:")
                    print(f"wi: {n.wi}")
                    print(f"ni: {n.ni}\n")

        # Select best move based on average value (not UCB)
        best_move = None
        best_value = float("-inf") if self.is_max_player else float("inf")

        legal_moves = self.game.get_legal_moves()
        move_values = {}

        for move in legal_moves:
            if move in self.root.children:
                value = self.root.children[move].get_value()
            else:
                value = 0.0

            move_values[move] = value

            if self.is_max_player:
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move

        # Print column values (for Brief or Verbose mode only)
        if self.brief or self.verbose:
            for col in range(1, 8):
                if col in move_values:
                    print(f"Column {col}: {move_values[col]:.2f}")
                else:
                    print(f"Column {col}: Null")

        if best_move is None:
            best_move = legal_moves[0] if legal_moves else 1

        # Always print final move (unless suppress_output is True for tournaments)
        if not self.suppress_output:
            print(f"FINAL Move selected: {best_move}")
        return best_move

