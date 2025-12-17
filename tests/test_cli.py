import builtins
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phyl2002_exam import cli
from phyl2002_exam.content import load_content


@pytest.fixture()
def content():
    return load_content()


def test_evaluate_keywords_matches_all():
    hits, matched = cli.evaluate_keywords("This mentions ATP hydrolysis pump", ["ATP", "pump"])
    assert hits == 2
    assert set(matched) == {"ATP", "pump"}


def test_evaluate_keywords_accepts_missing_keywords():
    hits, matched = cli.evaluate_keywords("Any response", None)

    assert hits == 0
    assert matched == []


def test_ask_short_grades_empty_keywords_correct(monkeypatch):
    question = {
        "stem": "Describe anything",
        "keywords": [],
        "explanation": "No specific points expected.",
    }

    monkeypatch.setattr(builtins, "input", lambda _: "Some answer")

    assert cli.ask_short(question) is True


def test_build_plan_appends_self_quiz(content):
    blocks = content["study_blocks"]
    extra_minutes = 10
    requested = sum(block["duration"] for block in blocks) + extra_minutes
    plan = cli.build_plan(blocks, focus=None, minutes=requested)

    assert plan[-1]["title"] == "Self-quiz and teach-back"
    assert plan[-1]["duration"] == extra_minutes


def test_build_plan_respects_time_slice(content):
    blocks = content["study_blocks"]
    plan = cli.build_plan(blocks, focus=None, minutes=10)

    assert len(plan) == 1
    assert plan[0]["duration"] == 10


def test_render_stats_reports_counts(content, capsys):
    cli.render_stats(content)
    output = capsys.readouterr().out

    assert "Mnemonics" in output
    assert "Questions" in output
    assert "Flashcards" in output
    assert "Topics" in output


def test_render_stats_handles_no_topics(capsys):
    cli.render_stats({"mnemonics": [], "questions": [], "flashcards": [], "study_blocks": []})
    output = capsys.readouterr().out

    assert "No topics available" in output
