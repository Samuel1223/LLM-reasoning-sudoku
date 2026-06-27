from __future__ import annotations

from mctot.experts.base import Expert
from mctot.experts.got_expert import GotExpert
from mctot.experts.lstm_tot_expert import LstmTotExpert
from mctot.experts.mcts_expert import MctsExpert
from mctot.experts.tot_expert import TotExpert


def default_experts() -> list[Expert]:
    """The default expert roster, in registration order (MCTS first)."""
    return [MctsExpert(), TotExpert(), LstmTotExpert(), GotExpert()]
