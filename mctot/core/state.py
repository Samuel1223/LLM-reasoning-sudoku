from __future__ import annotations

import json
import re
from typing import List, Optional


class State:
    """Sudoku state: a 2-D list-of-lists of single-char strings.

    Cells are ``"*"`` for blank or ``"1".."n"`` for filled.
    """

    def __init__(self, sudoku_board: List[List[str]]):
        self.sudoku = sudoku_board  # [["1", "2", "*"], ...]
        self.visit_count = 1  # when created, visit count = 1

    def increment_visit_count(self) -> None:
        self.visit_count += 1

    def get_board(self) -> List[List[str]]:
        return self.sudoku

    def __str__(self) -> str:
        return str(self.sudoku)


class StateParser:
    """Methods to parse a string from an LLM into a State."""

    @staticmethod
    def parse_single(llm_response: str) -> Optional[State]:
        # parse the llm response to state; return None if fail to parse
        sudoku_board_json_obj = StateParser._extract_json_from_text_string(llm_response)
        if sudoku_board_json_obj is None:
            return None

        key = "rows"
        if key not in sudoku_board_json_obj:
            return None

        rows = sudoku_board_json_obj[key]

        rectified_rows = []
        for row in rows:
            rectified_row = []
            for cell in row:
                if (
                    cell is None
                    or str(cell).lower() == "none"
                    or str(cell).lower() == "null"
                ):
                    rectified_cell = "*"
                else:
                    rectified_cell = str(cell)
                rectified_row.append(rectified_cell)
            rectified_rows.append(rectified_row)

        return State(rectified_rows)

    @staticmethod
    def parse_multi(llm_response: str) -> Optional[List[List[List[str]]]]:
        # parse the llm response to a list of boards; return None if fail to parse
        sudoku_board_json_obj = StateParser._extract_json_from_text_string(llm_response)
        if sudoku_board_json_obj is None:
            return None

        key = "solutions"
        if key not in sudoku_board_json_obj:
            return None

        sols = sudoku_board_json_obj[key]
        valid_sols = []
        key2 = "rows"
        for sol in sols:
            if key2 not in sol:
                continue
            rows = sol[key2]
            rectified_rows = []
            for row in rows:
                rectified_row = []
                for cell in row:
                    if (
                        cell is None
                        or str(cell).lower() == "none"
                        or str(cell).lower() == "null"
                    ):
                        rectified_cell = "*"
                    else:
                        rectified_cell = str(cell)
                    rectified_row.append(rectified_cell)
                rectified_rows.append(rectified_row)
            valid_sols.append(rectified_rows)

        if len(valid_sols) == 0:
            return None

        return valid_sols

    @staticmethod
    def _extract_json_from_text_string(text_str: str):
        """Extract a JSON object from a string; return None on error."""
        try:
            lp_idx = text_str.index("{")
            rp_idx = text_str.rindex("}")
            json_str = text_str[lp_idx : rp_idx + 1]
            json_str = json_str.replace("'", '"')
            # Quote unquoted * characters
            json_str = re.sub(r"(?<=\[|\s|,)(\*)(?=\s|,|\])", r'"\1"', json_str)
            # Quote unquoted integers
            json_str = re.sub(r"(?<=\[|\s|,)(\d+)(?=\s|,|\])", r'"\1"', json_str)
            return json.loads(json_str)
        except Exception:
            return None
