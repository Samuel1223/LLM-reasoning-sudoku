from __future__ import annotations

from typing import List, Optional

from mctot.experts.base import Board, Expert
from mctot.moe.gate import Gate
from mctot.moe.manager import Manager


class MixtureOfExperts:
    """Top-level MoE solver: Gate selects top-K experts, Manager aggregates."""

    def __init__(self, experts: List[Expert], puzzle_size: int, k: int = 2) -> None:
        self.gate = Gate(experts, k=k)
        self.manager = Manager(puzzle_size)

    def solve(self, board: Board) -> Optional[Board]:
        """Route ``board`` to top-K experts and return the aggregated answer."""
        raise NotImplementedError
