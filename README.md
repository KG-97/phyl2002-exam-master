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
- `review [--topic TOPIC] [--count N] [--seed SEED] [--progress PATH]`: spaced repetition review for due flashcards.
- `plan [--focus TOPIC] [--minutes TOTAL]`: generate a study plan using curated study blocks.
- `stats`: show counts of content items and topics covered.

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

Review due flashcards using spaced repetition scheduling:

```bash
python -m phyl2002_exam.cli review --count 6
```

## Deploy with Docker

Build a lightweight container image and run any CLI command by passing arguments after the image name:

```bash
docker build -t phyl2002-exam .
docker run --rm phyl2002-exam topics
docker run --rm phyl2002-exam mnemonics --topic "Action Potentials"
```

By default the container shows the CLI help (`--help`) if no arguments are provided. Mount a volume if you extend the content locally and want those changes reflected at runtime:

```bash
docker run --rm -v "$PWD/phyl2002_exam:/app/phyl2002_exam" phyl2002-exam stats
```
