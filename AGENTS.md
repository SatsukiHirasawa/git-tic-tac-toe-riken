# Agent instructions

Follow these rules when validating or choosing moves for the tic-tac-toe board:

- A valid board has exactly 3 rows and 3 columns. Each cell is `X`, `O`, or `.`, with exactly one space between cells and no extra spaces or characters.
- X moves first. The board is in progress only when the X count equals the O count or is exactly one greater than the O count. Equal counts mean X is next; one extra X means O is next.
- A board with three of the same mark in any row, column, or diagonal is finished and invalid as an in-progress board.
- When choosing a move, block the opponent's immediate winning move if one exists. Defense takes priority over an immediate win for the current player.

Keep user-facing instructions and board behavior consistent with these rules. Do not change the tests unless explicitly asked.
