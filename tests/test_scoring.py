from __future__ import annotations

from plantqa.eval.score import numeric_match, program_score
from plantqa.methods.base import parse_final


def test_numeric_match_needs_every_number_and_unit() -> None:
    must = ["266 psi", "1834 kPa"]
    assert numeric_match(must, "Max casing pressure 266 psi (1834 kPa).") is True
    assert numeric_match(must, "Max casing pressure 266 psi.") is False
    assert numeric_match(must, "266 bar (1834 kPa)") is False


def test_numeric_match_declines_text_items() -> None:
    assert numeric_match(["raised face flanges", "4 in"], "anything") is None
    assert numeric_match([], "anything") is None


def test_parse_final_reads_embedded_json() -> None:
    assert parse_final('ok {"answer": ["P-1-1"], "not_present": false} done') == {
        "answer": ["P-1-1"],
        "not_present": False,
    }
    assert parse_final("no json here") is None


def _free(answerable: str, must: list[str]) -> dict[str, object]:
    return {"source": {"kind": "plantdocs"}, "gold": {"answerable": answerable, "must": must}}


def test_abstention_rules() -> None:
    no = {"final": {"answer": None, "not_present": True}}
    assert program_score(_free("no", []), no) == {
        "source": "program",
        "verdict": "correct",
        "detail": "not_present",
    }
    assert program_score(_free("yes", ["5 bar"]), no)["verdict"] == "wrong"  # type: ignore[index]


def test_unscorable_text_goes_to_judge() -> None:
    answer = {"final": {"answer": "It is a globe valve.", "not_present": False}}
    assert program_score(_free("yes", ["globe-style control valve"]), answer) is None
    assert program_score(_free("no", []), answer) is None


def test_flagged_answer_with_text_goes_to_judge() -> None:
    answer = {
        "final": {
            "answer": "P-2-2 has a mechanical seal; part number not stated.",
            "not_present": True,
        }
    }
    assert program_score(_free("partial", ["mechanical seal"]), answer) is None
