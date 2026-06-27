from __future__ import annotations

import re

from mctot.experts.base import Board


def parse_board(s: str) -> Board:
    """Parse a string like ``"[[*, 3, 1], [*, 2, 3], [3, *, 2]]"`` into a
    list of lists of single-char strings (digits or ``"*"``).

    Tolerant of surrounding/interior whitespace and of optional quotes around
    individual cells.
    """
    board: Board = []
    for inner in re.findall(r"\[([^\[\]]*)\]", s):
        row: list[str] = []
        for raw in inner.split(","):
            cell = raw.strip().strip("'\"")
            if cell:
                row.append(cell)
        board.append(row)
    return board


def size(board: Board) -> int:
    return len(board)


def blank_count(board: Board) -> int:
    """Number of ``"*"`` cells."""
    return sum(1 for r in board for cell in r if cell == "*")


def givens_ratio(board: Board) -> float:
    """Filled cells / total cells. Returns 0.0 for an empty board."""
    total = sum(len(r) for r in board)
    if total == 0:
        return 0.0
    filled = total - blank_count(board)
    return filled / total
