from __future__ import annotations

from enum import Enum
from typing import List, Optional, Tuple

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

    def parse_response(self, text: Optional[str]) -> Optional[Board]:
        """Extract a board from a raw expert response, or None if unparseable."""
        raise NotImplementedError

    def choose_policy(self, board: Board) -> WaitPolicy:
        """Choose how to coordinate experts for ``board``."""
        raise NotImplementedError

    def is_valid_solution(self, board: Board) -> bool:
        """Return whether ``board`` is an acceptable final solution."""
        raise NotImplementedError

    def aggregate(self, candidates: List[Tuple[Board, float]]) -> Optional[Board]:
        """Combine parsed candidate boards into a single board."""
        raise NotImplementedError

    def solve(self, board: Board, experts: List[Expert]) -> Optional[Board]:
        """Produce a solution for ``board`` using ``experts``."""
        raise NotImplementedError
