# phyl2002-exam-master

Interactive exam preparation tool for PHYL2002 (Cellular Physiology) with mnemonics, practice questions, and study aids.

## Features

- Curated mnemonics with short explanations for rapid recall.
- Multiple-choice, short-answer, and mixed quizzes with scoring.
- Flashcard review sessions filtered by topic.
- Auto-generated study plans tailored to your available time and focus area.

## Getting started

1. Ensure you have Python 3.10+ installed.
2. Run commands from the repository root with `python -m phyl2002_exam.cli <command>`.

### Available commands

- `topics`: list all available topics.
- `mnemonics [--topic TOPIC] [--search TERM]`: browse mnemonic phrases and explanations.
- `quiz [--mode mcq|short|mixed] [--count N] [--topic TOPIC] [--seed SEED]`: practice questions with immediate feedback.
- `flashcards [--topic TOPIC] [--count N] [--seed SEED]`: step through flashcards interactively.
- `plan [--focus TOPIC] [--minutes TOTAL]`: generate a study plan using curated study blocks.

### Examples

List topics:

```bash
python -m phyl2002_exam.cli topics
```

Review mnemonics about action potentials:

```bash
python -m phyl2002_exam.cli mnemonics --topic "Action Potentials"
```

Run a mixed quiz with reproducible order:

```bash
python -m phyl2002_exam.cli quiz --mode mixed --count 4 --seed 42
```

Generate a 45-minute plan focused on membrane transport:

```bash
python -m phyl2002_exam.cli plan --focus "Membrane Transport" --minutes 45
```
