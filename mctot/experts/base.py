from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

Board = List[List[str]]  # n x n grid; "*" = blank, "1".."n" = filled


@dataclass(frozen=True)
class Proposal:
    """An expert's raw answer for a board.

    response: the expert's raw text answer (LLM-style), or None if it declined.
    score: the expert's self-reported confidence in [0, 1].
    expert_name: name of the producing expert.
    """

    response: Optional[str]
    score: float = 0.0
    expert_name: str = ""


class Expert(ABC):
    """A sudoku-solving strategy that can be mixed by the MoE."""

    name: str = "expert"

    def affinity(self, board: Board) -> float:
        """Cheap, deterministic routing score for ``board`` (no LLM). Default: none."""
        return 0.0

    @abstractmethod
    def propose(self, board: Board) -> Proposal:
        """Return this expert's raw Proposal for ``board``."""
        ...
