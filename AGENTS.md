# AGENTS.md — instructions for AI coding agents

## Purpose
`tasktracker` is a small command-line task tracker (Python 3.10+, standard library only).
Users add, list, complete, delete tasks and view statistics. Data lives in one JSON file.

## Architecture
| Path | Role |
|---|---|
| `tasktracker/__main__.py` | Entry point for `python -m tasktracker` |
| `tasktracker/cli.py` | argparse parser + command handlers (`cmd_add`, `cmd_list`, ...) |
| `tasktracker/models.py` | `Task` dataclass, `PRIORITIES`, overdue logic |
| `tasktracker/storage.py` | JSON load/save and ID generation |
| `tests/` | pytest suite |

Storage file: `$TASKS_FILE`, default `~/.tasks.json`. The JSON format (list of task objects) must stay backward compatible.

## Setup
```
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Safe commands (allowed without asking)
- `python -m pytest -v` — run tests
- `ruff check --select E,F .` — lint (read-only)
- `mypy tasktracker` — type check (read-only)
- `git status`, `git diff`, `git log` — read-only git
- Running the CLI **only** with a temporary file: `TASKS_FILE=/tmp/tasks-test.json python -m tasktracker ...`

## Coding conventions
- Standard library only in `tasktracker/`; keep functions small, PEP 8, 4-space indent.
- Command handlers return an exit code (`0` ok, `1` user error) and never call `sys.exit` themselves.
- User errors print a one-line message, never a traceback.
- Do not change the JSON storage format without a migration and a test.

## Test expectations
- Every behaviour change or bug fix comes with a pytest test that fails before the change.
- Tests must use `tmp_path` + `monkeypatch.setenv("TASKS_FILE", ...)`; never touch `~/.tasks.json`.
- All tests must pass before a change is proposed. Report the exact command and pass/fail totals; never claim results you did not run.

## Acceptance criteria (must stay true after any change)
1. AC1 `add` then `list` shows the task with its title and priority.
2. AC2 `done <id>` marks exactly that task as done and it is persisted.
3. AC3 An invalid priority is rejected with exit code 1 and nothing is saved.
4. AC4 `list --sort id|priority|due|title` returns the documented order; `--status` and `--tag` filter correctly.
5. AC5 `python -m pytest` passes and existing task files remain readable.

## Forbidden actions
- Never read, create or commit secrets, tokens, `.env` files or real personal data.
- Never run the CLI against the real `~/.tasks.json` or delete user data files.
- No destructive commands: `rm -rf`, `git push --force`, `git reset --hard`, rewriting history, deleting branches or tags (`baseline`).
- No production deployment, publishing to PyPI or pushing to `main`.
- No new or upgraded dependencies without explicit human approval in the PR.
- Do not disable, skip or weaken existing tests to make a change pass.

## Review gates
- Work on a feature branch; open a pull request; a human reviews the diff and test output before merge.
- One focused change per commit, with a message that references the risk ID (e.g. `R1`).
