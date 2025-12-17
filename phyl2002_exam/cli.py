import argparse
import random
import textwrap
from typing import Dict, List, Tuple

from .content import ensure_available, load_content, topics_from_content


def wrap(text: str, width: int = 80) -> str:
    return "\n".join(textwrap.wrap(text, width=width))


def render_mnemonics(content: Dict[str, List[Dict]], topic: str | None, search: str | None) -> None:
    mnemonics = content.get("mnemonics", [])
    if topic:
        mnemonics = [item for item in mnemonics if topic.lower() in item["topic"].lower()]
    if search:
        mnemonics = [
            item
            for item in mnemonics
            if search.lower() in item["title"].lower() or search.lower() in item["mnemonic"].lower()
        ]
    mnemonics = ensure_available(mnemonics, "No mnemonics found for that selection.")

    for item in mnemonics:
        print(f"\n[{item['topic']}] {item['title']}")
        print(f"  Mnemonic : {wrap(item['mnemonic'])}")
        print(f"  Why it helps: {wrap(item['explanation'])}")


def evaluate_keywords(answer: str, keywords: List[str]) -> Tuple[int, List[str]]:
    normalized = answer.lower()
    matched = [kw for kw in keywords if kw.lower() in normalized]
    return len(matched), matched


def ask_mcq(question: Dict) -> bool:
    print("\n" + wrap(question["stem"]))
    options = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for idx, choice in enumerate(question["choices"]):
        print(f"  {options[idx]}. {choice}")
    user = input("Your answer (letter): ").strip().upper()
    correct = user == question["answer"].upper()
    print(f"Answer: {question['answer']} — {question['explanation']}\n")
    return correct


def ask_short(question: Dict) -> bool:
    print("\n" + wrap(question["stem"]))
    response = input("Your answer: ").strip()
    hits, matched = evaluate_keywords(response, question.get("keywords", []))
    print(f"Key points: {', '.join(question.get('keywords', []))}")
    print(f"You mentioned: {', '.join(matched) if matched else 'none of the expected keywords'}")
    print(f"Explanation: {question['explanation']}\n")
    return hits >= max(1, len(question.get("keywords", [])) // 2)


def run_quiz(content: Dict[str, List[Dict]], mode: str, count: int, topic: str | None, seed: int | None) -> None:
    if seed is not None:
        random.seed(seed)

    pool = content.get("questions", [])
    if topic:
        pool = [q for q in pool if topic.lower() in q["topic"].lower()]
    if mode != "mixed":
        pool = [q for q in pool if q["type"] == mode]
    pool = ensure_available(pool, "No questions available for that selection.")

    selected = random.sample(pool, k=min(count, len(pool)))
    correct = 0
    for question in selected:
        if question["type"] == "mcq":
            correct += ask_mcq(question)
        else:
            correct += ask_short(question)

    print(f"Score: {correct}/{len(selected)} correct")


def run_flashcards(content: Dict[str, List[Dict]], topic: str | None, count: int, seed: int | None) -> None:
    if seed is not None:
        random.seed(seed)

    cards = content.get("flashcards", [])
    if topic:
        cards = [card for card in cards if topic.lower() in card["topic"].lower()]
    cards = ensure_available(cards, "No flashcards found for that selection.")

    subset = random.sample(cards, k=min(count, len(cards)))
    for card in subset:
        print(f"\n[{card['topic']}] {wrap(card['front'])}")
        input("Press Enter to reveal...")
        print(f"  ➜ {wrap(card['back'])}")


def build_plan(blocks: List[Dict], focus: str | None, minutes: int) -> List[Dict]:
    filtered = blocks
    if focus:
        filtered = [blk for blk in blocks if focus.lower() in blk["focus"].lower()]
    if not filtered:
        filtered = blocks
    filtered = ensure_available(filtered, "No study blocks available.")

    remaining = minutes
    plan: List[Dict] = []
    for block in filtered:
        if remaining <= 0:
            break
        duration = min(block["duration"], remaining)
        plan.append({**block, "duration": duration})
        remaining -= duration

    if remaining > 0:
        plan.append(
            {
                "title": "Self-quiz and teach-back",
                "focus": focus or "Mixed",
                "duration": remaining,
                "actions": [
                    "Write three questions you missed recently",
                    "Teach a tough concept aloud or to a peer"
                ],
            }
        )
    return plan


def render_plan(blocks: List[Dict]) -> None:
    print("\nStudy Plan")
    print("-" * 40)
    for idx, block in enumerate(blocks, start=1):
        print(f"{idx}. {block['title']} ({block['duration']} min) — Focus: {block['focus']}")
        for action in block.get("actions", []):
            print(f"   - {action}")


def show_topics(content: Dict[str, List[Dict]]) -> None:
    topics = topics_from_content(content)
    print("Available topics:")
    for topic in topics:
        print(f" • {topic}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Interactive PHYL2002 exam preparation aid with mnemonics, questions, and flashcards."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    mnemonics_parser = subparsers.add_parser("mnemonics", help="Browse mnemonics with explanations.")
    mnemonics_parser.add_argument("--topic", help="Filter by topic.")
    mnemonics_parser.add_argument("--search", help="Keyword search in mnemonic titles or phrases.")

    quiz_parser = subparsers.add_parser("quiz", help="Practice questions.")
    quiz_parser.add_argument("--mode", choices=["mcq", "short", "mixed"], default="mixed", help="Question type.")
    quiz_parser.add_argument("--count", type=int, default=5, help="How many questions to attempt.")
    quiz_parser.add_argument("--topic", help="Filter questions by topic.")
    quiz_parser.add_argument("--seed", type=int, help="Seed for reproducible question order.")

    flash_parser = subparsers.add_parser("flashcards", help="Review flashcards.")
    flash_parser.add_argument("--topic", help="Filter flashcards by topic.")
    flash_parser.add_argument("--count", type=int, default=4, help="Number of flashcards to review.")
    flash_parser.add_argument("--seed", type=int, help="Seed for reproducible ordering.")

    plan_parser = subparsers.add_parser("plan", help="Generate a focused study plan.")
    plan_parser.add_argument("--focus", help="Topic to prioritize.")
    plan_parser.add_argument("--minutes", type=int, default=60, help="Total minutes available.")

    subparsers.add_parser("topics", help="List available topics.")
    return parser


def main(argv: List[str] | None = None) -> None:
    content = load_content()
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "mnemonics":
            render_mnemonics(content, args.topic, args.search)
        elif args.command == "quiz":
            run_quiz(content, args.mode, args.count, args.topic, args.seed)
        elif args.command == "flashcards":
            run_flashcards(content, args.topic, args.count, args.seed)
        elif args.command == "plan":
            plan = build_plan(content.get("study_blocks", []), args.focus, args.minutes)
            render_plan(plan)
        elif args.command == "topics":
            show_topics(content)
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
