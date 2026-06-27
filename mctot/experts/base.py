from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

Board = List[List[str]]  # n x n grid; "*" = blank, "1".."n" = filled


@dataclass(frozen=True)
class Proposal:
    """An expert's proposed answer for a board.

    solution: a full board (same shape as input), or None if the expert
        declined / failed to produce anything.
    score: the expert's self-reported confidence in [0, 1]. The Manager uses
        it only as a tie-breaker, never as a validity signal.
    expert_name: name of the producing expert.
    """

    solution: Optional[Board]
    score: float = 0.0
    expert_name: str = ""


class Expert(ABC):
    """A sudoku-solving strategy that can be mixed by the MoE."""

    #: stable identifier; also used as a deterministic tie-break key
    name: str = "expert"

    @abstractmethod
    def propose(self, board: Board) -> Proposal:
        """Return this expert's Proposal for ``board`` (must not mutate it)."""
        ...

    def affinity(self, board: Board) -> float:
        """Cheap, deterministic routing score for ``board`` (higher = better
        fit). The Gate uses this to choose experts WITHOUT running them, so it
        must never call an LLM. Default: no preference."""
        return 0.0
