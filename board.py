"""
board.py - Tic-tac-toe board validation and move selection.
"""

from typing import Optional


def _parse_board(text: str) -> Optional[list[list[str]]]:
    """
    Parse the board text into a 2D list.
    Returns None if the format is invalid.
    """
    # Must not have trailing blank lines beyond a single optional newline
    # Normalize: allow exactly one optional trailing newline
    if text.endswith("\n"):
        body = text[:-1]
        # No second newline allowed at end
        if body.endswith("\n"):
            return None
    else:
        body = text

    rows = body.split("\n")

    # Must have exactly 3 rows
    if len(rows) != 3:
        return None

    board = []
    for row in rows:
        # Each row must match exactly "C C C" where C is X, O, or .
        cells = row.split(" ")
        if len(cells) != 3:
            return None
        # Validate each cell
        for cell in cells:
            if cell not in ("X", "O", "."):
                return None
        # Also validate the raw row format (no double spaces, no leading/trailing spaces)
        expected = " ".join(cells)
        if row != expected:
            return None
        board.append(cells)

    return board


def _check_winner(board: list[list[str]], player: str) -> bool:
    """Return True if the given player has three in a row."""
    # Rows
    for row in board:
        if all(c == player for c in row):
            return True
    # Columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def _can_win_next(board: list[list[str]], player: str) -> Optional[tuple[int, int]]:
    """
    Return the (row, col) where `player` can win in one move, or None.
    """
    for r in range(3):
        for c in range(3):
            if board[r][c] == ".":
                board[r][c] = player
                won = _check_winner(board, player)
                board[r][c] = "."
                if won:
                    return (r, c)
    return None


def validate_board(text: str) -> bool:
    """
    Return True if the board is valid, False otherwise.

    Validity rules:
    1. Format: exactly 3x3, cells are X/O/., single spaces between cells,
       no extra spaces or characters.
    2. Turn count: X count == O count (X's turn) or X count == O count + 1 (O's turn).
    3. No winner already on the board.
    """
    board = _parse_board(text)
    if board is None:
        return False

    # Count pieces
    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)

    # Turn count check
    if x_count != o_count and x_count != o_count + 1:
        return False

    # No winner already
    if _check_winner(board, "X") or _check_winner(board, "O"):
        return False

    return True


def choose_move(text: str, player: str) -> tuple[int, int]:
    """
    Choose the best move for `player` on the given board.

    Strategy:
    1. If the opponent can win next turn, block them (defense first).
    2. If the player can win immediately, do so.
    3. Otherwise, pick the first available cell (center, then corners, then edges).
    """
    board = _parse_board(text)
    if board is None:
        raise ValueError("Invalid board")

    opponent = "O" if player == "X" else "X"

    # 1. Block opponent's immediate win
    block_move = _can_win_next(board, opponent)
    if block_move is not None:
        return block_move

    # 2. Win immediately if possible
    win_move = _can_win_next(board, player)
    if win_move is not None:
        return win_move

    # 3. Prefer center, then corners, then edges
    preferred = [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2), (0, 1), (1, 0), (1, 2), (2, 1)]
    for r, c in preferred:
        if board[r][c] == ".":
            return (r, c)

    raise ValueError("No available moves")