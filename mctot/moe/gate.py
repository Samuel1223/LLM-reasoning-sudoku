from __future__ import annotations

from typing import List

from mctot.experts.base import Board, Expert


class Gate:
    """Top-K router: scores experts for a board and selects the best K.

    Scoring MUST be deterministic and offline (board features only) — never
    call an LLM here.
    """

    def __init__(self, experts: List[Expert], k: int = 2) -> None:
        self.experts = list(experts)
        self.k = k

    def score(self, expert: Expert, board: Board) -> float:
        """Routing score for ``expert`` on ``board`` (higher = better fit)."""
        raise NotImplementedError

    def select(self, board: Board) -> List[Expert]:
        """Top-K experts for ``board``, highest score first. Ties broken
        deterministically by registration order in ``self.experts``. Returns
        at most ``k`` experts (never more than are registered)."""
        raise NotImplementedError
