"""
Connect Four Game Implementation
CS 4320 PA3: Game Playing with UCT

This module implements the Connect Four game board, game logic, and terminal state checking.
"""

import copy
from typing import Optional, List, Tuple


class ConnectFour:
    """
    Represents a Connect Four game board and provides game logic.

    The board is 7 columns (1-7) by 6 rows (0-5 from bottom to top).
    Players: 'R' (Red, Min player, value -1) and 'Y' (Yellow, Max player, value 1)
    Empty spaces are represented by 'O'.
    """

    ROWS = 6
    COLS = 7

    def __init__(self, board: Optional[List[List[str]]] = None):
        """
        Initialize a Connect Four board.

        Args:
            board: Optional 2D list representing the board state.
                  If None, creates an empty board.
        """
        if board is None:
            self.board = [["O" for _ in range(self.COLS)] for _ in range(self.ROWS)]
        else:
            # Deep copy to avoid reference issues
            self.board = copy.deepcopy(board)

        # Track the last move for efficient win checking
        self.last_move: Optional[Tuple[int, int]] = None
        # Move stack for efficient undo operations
        self.move_stack: List[Tuple[int, int]] = []  # (row, col) pairs

    def copy(self) -> "ConnectFour":
        """Create a deep copy of the current game state."""
        new_game = ConnectFour(self.board)
        new_game.last_move = self.last_move
        new_game.move_stack = self.move_stack.copy()  # Shallow copy is fine for tuples
        return new_game

    def get_legal_moves(self) -> List[int]:
        """
        Get list of legal column moves (1-indexed).

        Returns:
            List of column numbers (1-7) that are not full.
        """
        legal_moves = []
        for col in range(self.COLS):
            if self.board[self.ROWS - 1][col] == "O":
                legal_moves.append(col + 1)  # Convert to 1-indexed
        return legal_moves

    def make_move(self, column: int, player: str) -> bool:
        """
        Make a move by placing a piece in the specified column.

        Args:
            column: Column number (1-indexed)
            player: Player character ('R' or 'Y')

        Returns:
            True if move was successful, False if column is full
        """
        col_idx = column - 1  # Convert to 0-indexed

        # Find the first empty row in this column
        for row in range(self.ROWS):
            if self.board[row][col_idx] == "O":
                self.board[row][col_idx] = player
                self.last_move = (row, col_idx)
                self.move_stack.append((row, col_idx))
                return True

        return False  # Column is full

    def undo_move(self, column: int):
        """
        Undo a move by removing the top piece from the specified column.
        Uses move stack for O(1) performance.

        Args:
            column: Column number (1-indexed)
        """
        col_idx = column - 1

        # Optimized: Use move_stack directly if the last move is in this column
        if self.move_stack and self.move_stack[-1][1] == col_idx:
            # Last move is in this column - use stack directly (O(1))
            row, col = self.move_stack.pop()
            self.board[row][col] = "O"
            # Update last_move efficiently using move stack
            if self.move_stack:
                self.last_move = self.move_stack[-1]
            else:
                self.last_move = None
            return

        # Fallback: Find the topmost piece in this column (shouldn't happen in normal MCTS usage)
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col_idx] != "O":
                self.board[row][col_idx] = "O"
                # Remove from move stack if it matches
                if self.move_stack and self.move_stack[-1] == (row, col_idx):
                    self.move_stack.pop()
                # Update last_move efficiently using move stack
                if self.move_stack:
                    self.last_move = self.move_stack[-1]
                else:
                    self.last_move = None
                return

    def is_terminal(self) -> Tuple[bool, Optional[int]]:
        """
        Check if the current game state is terminal (win or draw).

        Returns:
            Tuple of (is_terminal, value)
            - is_terminal: True if game is over
            - value: -1 if Red wins, 1 if Yellow wins, 0 if draw, None if not terminal
        """
        # Check for win (efficiently using last_move if available)
        if self.last_move is not None:
            winner = self._check_win(self.last_move[0], self.last_move[1])
            if winner is not None:
                value = -1 if winner == "R" else 1
                return (True, value)
        else:
            # Fallback: check entire board for wins if last_move is not set
            # This handles edge cases like loaded game states
            winner = self._check_board_for_win()
            if winner is not None:
                value = -1 if winner == "R" else 1
                return (True, value)

        # Check for draw (board is full)
        if len(self.get_legal_moves()) == 0:
            return (True, 0)

        return (False, None)

    def _check_win(self, row: int, col: int) -> Optional[str]:
        """
        Check if the last move resulted in a win.
        Only checks lines that include the last move position.

        Args:
            row: Row index of last move (0-indexed)
            col: Column index of last move (0-indexed)

        Returns:
            'R' if Red wins, 'Y' if Yellow wins, None if no win
        """
        player = self.board[row][col]

        # Check horizontal, vertical, and both diagonals
        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)],  # Diagonal /
            [(1, -1), (-1, 1)],  # Diagonal \
        ]

        for dir_pair in directions:
            count = 1  # Count the current piece

            # Check in both directions
            for dx, dy in dir_pair:
                r, c = row + dx, col + dy
                while (
                    0 <= r < self.ROWS
                    and 0 <= c < self.COLS
                    and self.board[r][c] == player
                ):
                    count += 1
                    r += dx
                    c += dy

            if count >= 4:
                return player

        return None

    def _check_board_for_win(self) -> Optional[str]:
        """
        Check the entire board for a win (fallback when last_move is not available).

        Returns:
            'R' if Red wins, 'Y' if Yellow wins, None if no win
        """
        # Check all positions on the board for wins
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.board[row][col] != "O":
                    winner = self._check_win(row, col)
                    if winner is not None:
                        return winner
        return None

    def __str__(self) -> str:
        """String representation of the board (for debugging)."""
        lines = []
        for row in range(self.ROWS - 1, -1, -1):
            lines.append("".join(self.board[row]))
        return "\n".join(lines)

    @staticmethod
    def from_file(filename: str) -> Tuple["ConnectFour", str, str]:
        """
        Load a game state from a file.

        File format:
        Line 1: Algorithm name (UR, PMCGS, or UCT)
        Line 2: Player to move ('R' or 'Y')
        Lines 3-8: Board state (6 rows, 7 columns)

        Args:
            filename: Path to the input file

        Returns:
            Tuple of (game, algorithm, player)
        """
        with open(filename, "r") as f:
            lines = [line.strip() for line in f.readlines()]

        algorithm = lines[0]
        player = lines[1]

        # Parse board (6 rows) - lines 3-8 (indices 2-7)
        if len(lines) < 8:
            raise ValueError(
                f"File must have at least 8 lines (algorithm, player, 6 board rows), got {len(lines)}"
            )

        board_lines = lines[2:8]  # Lines 3-8 (6 rows)
        board = []
        for i, line in enumerate(board_lines):
            if len(line) != ConnectFour.COLS:
                raise ValueError(
                    f"Board row {i+3} must have exactly {ConnectFour.COLS} characters, got {len(line)}"
                )
            board.append(list(line))

        # File format: top row first, but our internal representation is bottom row first
        # So we reverse the board
        board.reverse()

        game = ConnectFour(board)

        # Find last move for win checking and initialize move_stack
        for row in range(game.ROWS):
            for col in range(game.COLS):
                if game.board[row][col] != "O":
                    game.last_move = (row, col)
                    # Initialize move_stack with last move (for loaded games)
                    game.move_stack = [(row, col)] if game.last_move else []

        return game, algorithm, player
