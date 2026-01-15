import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_PROGRESS_PATH = Path.home() / ".phyl2002_exam_progress.json"
DATE_FORMAT = "%Y-%m-%d"


@dataclass(frozen=True)
class ReviewState:
    repetitions: int
    interval: int
    efactor: float
    due: date

    def to_json(self) -> Dict[str, Any]:
        return {
            "repetitions": self.repetitions,
            "interval": self.interval,
            "efactor": self.efactor,
            "due": self.due.strftime(DATE_FORMAT),
        }


def load_progress(path: Path = DEFAULT_PROGRESS_PATH) -> Dict[str, Dict[str, Any]]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_progress(progress: Dict[str, Dict[str, Any]], path: Path = DEFAULT_PROGRESS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(progress, handle, indent=2, sort_keys=True)


def is_due(entry: Optional[Dict[str, Any]], today: date) -> bool:
    if not entry:
        return True
    due_str = entry.get("due")
    if not due_str:
        return True
    due = datetime.strptime(due_str, DATE_FORMAT).date()
    return due <= today


def update_sm2(entry: Optional[Dict[str, Any]], rating: int, today: date) -> ReviewState:
    repetitions = int(entry.get("repetitions", 0) if entry else 0)
    interval = int(entry.get("interval", 0) if entry else 0)
    efactor = float(entry.get("efactor", 2.5) if entry else 2.5)

    rating = max(0, min(5, rating))
    efactor = efactor + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02))
    efactor = max(1.3, efactor)

    if rating < 3:
        repetitions = 0
        interval = 1
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = max(1, int(round(interval * efactor)))
        repetitions += 1

    due = today + timedelta(days=interval)
    return ReviewState(
        repetitions=repetitions,
        interval=interval,
        efactor=efactor,
        due=due,
    )
