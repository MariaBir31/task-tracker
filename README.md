# Task Tracker

A simple command-line task tracker written in Python (3.10+, standard library only). Tasks are stored in a JSON file.

## Setup

```
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```
python -m tasktracker add "Buy milk" --priority high --due 2026-11-25 --tags home,shop
python -m tasktracker list --status open --sort priority     # sort: id | priority | due | title
python -m tasktracker done 1
python -m tasktracker delete 1
python -m tasktracker stats
```

- Priority: `low`, `medium` (default), `high`.
- Due date must be `YYYY-MM-DD`.
- Tasks are saved to `~/.tasks.json` (override with the `TASKS_FILE` environment variable).

## Tests and checks

```
python -m pytest -v
ruff check --select E,F .    # optional lint
mypy tasktracker             # optional type check
```

## Known limitations

- `stats` fails when there are no tasks (division by zero).
- A corrupted JSON file causes a traceback instead of a clear message.
- Tags are split on `,` without trimming spaces (`"home, work"` → tag `" work"`).

## For AI agents

See [AGENTS.md](AGENTS.md) for allowed commands, forbidden actions and acceptance criteria.
