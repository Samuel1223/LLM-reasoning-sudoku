from __future__ import annotations

from mctot.experts.base import Board, Expert, Proposal


class LstmTotExpert(Expert):
    """Adapter around the upstream LSTM-guided Tree-of-Thought solver
    (the ``my-tot/`` package).

    All heavy/strategy imports happen lazily inside :meth:`propose` so that
    importing this module never pulls in langchain/openai/numpy.
    """

    name = "lstm_tot"

    def propose(self, board: Board) -> Proposal:
        try:
            # Lazy import of the upstream my-tot strategy. Any failure (missing
            # module, missing LLM config, runtime error) falls through to the
            # declined proposal below.
            import importlib

            importlib.import_module("prompter.prompter")  # noqa: F841

            # The real my-tot solver requires an LLM backend that is unavailable
            # in the offline base; a fully wired invocation is out of scope.
            raise RuntimeError("lstm_tot strategy not configured for offline use")
        except Exception:
            return Proposal(solution=None, score=0.0, expert_name=self.name)

    def affinity(self, board):
        from mctot.core.board import givens_ratio

        return givens_ratio(board)
