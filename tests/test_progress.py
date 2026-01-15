from datetime import date, timedelta
from pathlib import Path

from phyl2002_exam.progress import DATE_FORMAT, is_due, load_progress, save_progress, update_sm2


def test_update_sm2_resets_on_low_rating():
    entry = {"repetitions": 2, "interval": 6, "efactor": 2.5, "due": "2024-01-01"}
    today = date(2024, 1, 2)

    state = update_sm2(entry, rating=2, today=today)

    assert state.repetitions == 0
    assert state.interval == 1
    assert state.due == today + timedelta(days=1)


def test_update_sm2_grows_interval_for_good_rating():
    entry = {"repetitions": 1, "interval": 1, "efactor": 2.5, "due": "2024-01-01"}
    today = date(2024, 1, 2)

    state = update_sm2(entry, rating=5, today=today)

    assert state.repetitions == 2
    assert state.interval == 6
    assert state.due == today + timedelta(days=6)


def test_is_due_checks_due_date():
    today = date(2024, 1, 5)
    entry = {"due": (today + timedelta(days=2)).strftime(DATE_FORMAT)}

    assert is_due(entry, today) is False
    assert is_due(entry, today + timedelta(days=2)) is True


def test_load_save_progress(tmp_path):
    path = tmp_path / "progress.json"
    progress = {"Action::Define": {"interval": 1, "repetitions": 1, "efactor": 2.5, "due": "2024-01-02"}}

    save_progress(progress, path)
    loaded = load_progress(path)

    assert loaded == progress
    assert path.exists()
    assert Path(path).read_text(encoding="utf-8").strip()
