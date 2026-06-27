from __future__ import annotations

from mctot.experts.base import Board, Expert, Proposal


class MctsExpert(Expert):
    """Adapter around the upstream Monte-Carlo Tree Search solver (``mcts/``).

    All heavy/strategy imports happen lazily inside :meth:`propose` so that
    importing this module never pulls in langchain/openai/numpy.
    """

    name = "mcts"

    def propose(self, board: Board) -> Proposal:
        try:
            # Lazy import of the upstream MCTS strategy. Any failure (missing
            # module, missing LLM config, runtime error) falls through to the
            # declined proposal below.
            from mcts.MctsController import MctsController  # noqa: F401

            # The real MCTS controller requires LLM/policy-model configuration
            # that is unavailable in the offline base; a fully wired invocation
            # is intentionally out of scope here.
            raise RuntimeError("mcts strategy not configured for offline use")
        except Exception:
            return Proposal(response=None, score=0.0, expert_name=self.name)

    def affinity(self, board):
        from mctot.core.board import blank_count, size

        n = size(board)
        total = n * n if n else 1
        return blank_count(board) / total
