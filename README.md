# Task Tracker

A simple command-line task tracker written in Python. Tasks are stored in a JSON file.

## Setup

```
pip install -r requirements.txt
```

## Usage

```
python -m tasktracker add "Buy milk" --priority high --due 2026-11-25 --tags home,shop
python -m tasktracker list --status open --sort priority
python -m tasktracker done 1
python -m tasktracker delete 1
python -m tasktracker stats
```

Tasks are saved to `~/.tasks.json` (override with the `TASKS_FILE` environment variable).

## Tests

```
pytest
```
