from __future__ import annotations

from typing import List

from mctot.experts.base import Board, Expert


class Gate:
    """Routes a board to a subset of the registered experts."""

    def __init__(self, experts: List[Expert], k: int = 2) -> None:
        self.experts = list(experts)
        self.k = k

    def score(self, expert: Expert, board: Board) -> float:
        """Return a routing score for ``expert`` on ``board``."""
        raise NotImplementedError

    def rank(self, board: Board) -> List[Expert]:
        """Return the registered experts ordered for ``board``."""
        raise NotImplementedError

    def select(self, board: Board) -> List[Expert]:
        """Return the experts to consult for ``board``."""
        raise NotImplementedError
