from __future__ import annotations

from typing import List, Optional

from mctot.experts.base import Board, Expert
from mctot.moe.gate import Gate
from mctot.moe.manager import Manager


class MixtureOfExperts:
    """Top-level mixture-of-experts Sudoku solver."""

    def __init__(self, experts: List[Expert], puzzle_size: int, k: int = 2) -> None:
        self.gate = Gate(experts, k=k)
        self.manager = Manager(puzzle_size)

    def solve(self, board: Board) -> Optional[Board]:
        """Return a solution for ``board``."""
        raise NotImplementedError
