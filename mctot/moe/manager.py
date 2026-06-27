from __future__ import annotations

from enum import Enum
from typing import List, Optional

from mctot.core.checker import SudokuChecker
from mctot.experts.base import Board, Expert, Proposal


class WaitPolicy(Enum):
    FIRST_VALID = "first_valid"
    WAIT_ALL = "wait_all"


class Manager:
    """Coordinates the selected experts to produce a solution."""

    def __init__(self, puzzle_size: int) -> None:
        self.puzzle_size = puzzle_size
        self.checker = SudokuChecker(puzzle_size)

    def choose_policy(self, board: Board) -> WaitPolicy:
        """Choose how to coordinate experts for ``board``."""
        raise NotImplementedError

    def is_valid_solution(self, board: Board) -> bool:
        """Return whether ``board`` is an acceptable final solution."""
        raise NotImplementedError

    def aggregate(self, proposals: List[Proposal]) -> Optional[Board]:
        """Combine expert proposals into a single board."""
        raise NotImplementedError

    def solve(self, board: Board, experts: List[Expert]) -> Optional[Board]:
        """Produce a solution for ``board`` using ``experts``."""
        raise NotImplementedError
