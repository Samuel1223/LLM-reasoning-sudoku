from __future__ import annotations
from enum import Enum
from typing import List, Optional
from mctot.experts.base import Board, Expert, Proposal
from mctot.core.checker import SudokuChecker


class WaitPolicy(Enum):
    FIRST_VALID = "first_valid"  # stop at the first checker-valid complete solution
    WAIT_ALL = "wait_all"  # run all selected experts, then aggregate


class Manager:
    """Aggregator: runs gate-selected experts sequentially and combines them.

    Execution is sequential and short-circuiting: under FIRST_VALID the Manager
    stops calling experts as soon as one returns a SudokuChecker-valid complete
    solution. Fully deterministic and offline.
    """

    def __init__(self, puzzle_size: int) -> None:
        self.puzzle_size = puzzle_size
        self.checker = SudokuChecker(puzzle_size)

    def choose_policy(self, board: Board) -> "WaitPolicy":
        """Pick a wait policy from board difficulty (deterministic)."""
        raise NotImplementedError

    def is_valid_solution(self, board: Board) -> bool:
        """True iff ``board`` is a complete, checker-valid solution."""
        raise NotImplementedError

    def aggregate(self, proposals: List[Proposal]) -> Optional[Board]:
        """Combine WAIT_ALL proposals into one board (per-cell majority vote
        among valid proposals; ties broken toward the higher-scored proposal,
        then expert order)."""
        raise NotImplementedError

    def solve(self, board: Board, experts: List[Expert]) -> Optional[Board]:
        """Run ``experts`` (already gate-ordered) under the chosen policy and
        return the final board, or None if no valid solution is produced."""
        raise NotImplementedError
