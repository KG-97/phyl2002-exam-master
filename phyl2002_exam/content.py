import json
from pathlib import Path
from typing import Dict, Iterable, List

DATA_FILE = Path(__file__).resolve().parent / "data" / "content.json"


def load_content() -> Dict[str, List[Dict]]:
    """
    Load static study content from JSON.

    Returns:
        Parsed content including mnemonics, questions, flashcards, and study blocks.
    """
    with DATA_FILE.open(encoding="utf-8") as handle:
        return json.load(handle)


def topics_from_content(content: Dict[str, List[Dict]]) -> List[str]:
    """Return a sorted list of topics present across all content types."""
    topic_fields = [
        (content.get("mnemonics", []), "topic"),
        (content.get("questions", []), "topic"),
        (content.get("flashcards", []), "topic"),
        (content.get("study_blocks", []), "focus"),
    ]
    topics: set[str] = set()
    for collection, key in topic_fields:
        topics.update(item.get(key, "") for item in collection if item.get(key))
    return sorted(topics)


def ensure_available(items: Iterable[Dict], fallback_message: str) -> List[Dict]:
    """Materialize an iterable and raise a clear error when empty."""
    materialized = list(items)
    if not materialized:
        raise ValueError(fallback_message)
    return materialized
