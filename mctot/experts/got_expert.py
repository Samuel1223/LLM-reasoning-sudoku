from __future__ import annotations

from mctot.experts.base import Board, Expert, Proposal


class GotExpert(Expert):
    """Adapter around the upstream Graph-of-Thought solver (``got/``).

    All heavy/strategy imports happen lazily inside :meth:`propose` so that
    importing this module never pulls in langchain/openai/numpy.
    """

    name = "got"

    def propose(self, board: Board) -> Proposal:
        try:
            # Lazy import of the upstream GoT strategy. Any failure (missing
            # module, missing LLM config, runtime error) falls through to the
            # declined proposal below.
            from got.got import got  # noqa: F401

            # The real GoT solver requires an LLM backend that is unavailable
            # in the offline base; a fully wired invocation is out of scope.
            raise RuntimeError("got strategy not configured for offline use")
        except Exception:
            return Proposal(solution=None, score=0.0, expert_name=self.name)

    def affinity(self, board):
        from mctot.core.board import size

        n = size(board)
        return 1.0 / n if n else 0.0
