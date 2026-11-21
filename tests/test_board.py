import pytest

from board import choose_move, validate_board


@pytest.mark.parametrize(
    "text",
    [
        ". . .\n. . .\n. . .",
        "X O .\n. X O\n. . .\n",
        "X X O\nO O X\nX . .",
    ],
)
def test_validate_board_accepts_well_formed_in_progress_boards(text):
    assert validate_board(text) is True


@pytest.mark.parametrize(
    "text",
    [
        ". .\n. .\n. .",
        ". . .\n. . .",
        ". . .\n. . .\n. . .\n\n",
        ". . . .\n. . .\n. . .",
        ". . .\n. . ?\n. . .",
        "X  . .\n. . .\n. . .",
        " X . .\n. . .\n. . .",
        ". . . \n. . .\n. . .",
        ". . .\n. . .\n. . .extra",
        ". . .\n\n. . .",
    ],
)
def test_validate_board_rejects_malformed_boards(text):
    assert validate_board(text) is False


@pytest.mark.parametrize(
    "text",
    [
        "X X .\nO . X\n. O X",
        "O O .\nO X .\n. X .",
    ],
)
def test_validate_board_rejects_unreachable_turn_counts(text):
    assert validate_board(text) is False


@pytest.mark.parametrize(
    "text",
    [
        "X X X\nO O .\nO X .",
        "X X .\nO O O\nX . .",
        "X O .\nX O .\nX . O",
        "X O .\nX O .\n. O X",
        "X O O\n. X .\nO . X",
        "O X X\n. O .\nX . O",
    ],
)
def test_validate_board_rejects_boards_with_a_winner(text):
    assert validate_board(text) is False


@pytest.mark.parametrize(
    ("text", "expected_move"),
    [
        ("O O .\nX . .\n. X .", (0, 2)),
        ("O X .\nO . X\n. . .", (2, 0)),
        ("O X .\nX O .\n. . .", (2, 2)),
        ("X . O\nX O .\n. . .", (2, 0)),
    ],
)
def test_choose_move_blocks_opponents_immediate_win(text, expected_move):
    assert validate_board(text) is True
    assert choose_move(text, "X") == expected_move
