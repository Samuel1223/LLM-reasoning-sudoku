from __future__ import annotations

from mctot.experts.base import Board, Expert, Proposal


class TotExpert(Expert):
    """Adapter around the upstream Tree-of-Thought puzzle solver
    (``tree-of-thought-puzzle-solver/``).

    All heavy/strategy imports happen lazily inside :meth:`propose` so that
    importing this module never pulls in langchain/openai/numpy.
    """

    name = "tot"

    def propose(self, board: Board) -> Proposal:
        try:
            # Lazy import of the upstream ToT solver. Any failure (missing
            # module, missing LLM config, runtime error) falls through to the
            # declined proposal below.
            import importlib

            importlib.import_module("tot")  # noqa: F841

            # The real ToT solver requires an LLM backend that is unavailable
            # in the offline base; a fully wired invocation is out of scope.
            raise RuntimeError("tot strategy not configured for offline use")
        except Exception:
            return Proposal(response=None, score=0.0, expert_name=self.name)

    def affinity(self, board):
        from mctot.core.board import blank_count, size

        n = size(board)
        total = n * n if n else 1
        r = blank_count(board) / total
        return 1.0 - abs(r - 0.5) * 2.0
