"""Acceptance tests (AC2-AC4) written before refactoring to lock in behaviour."""
import json
import re

import pytest

from tasktracker.cli import main
from tasktracker.storage import Storage


@pytest.fixture
def tasks_file(tmp_path, monkeypatch):
    path = tmp_path / "tasks.json"
    monkeypatch.setenv("TASKS_FILE", str(path))
    main(["add", "banana", "--priority", "low",
          "--due", "2026-12-01", "--tags", "home"])
    main(["add", "Apple", "--priority", "high", "--tags", "work"])
    main(["add", "cherry", "--priority", "medium", "--due", "2026-11-25"])
    return path


def listed_titles(capsys, *args):
    capsys.readouterr()
    assert main(["list", *args]) == 0
    lines = capsys.readouterr().out.strip().splitlines()
    return [re.match(r"\[.\] #\d+ (.+?) \(", line).group(1) for line in lines]


@pytest.mark.parametrize(
    "sort, expected",
    [
        ("id", ["banana", "Apple", "cherry"]),
        ("priority", ["Apple", "cherry", "banana"]),
        ("due", ["cherry", "banana", "Apple"]),
        ("title", ["Apple", "banana", "cherry"]),
    ],
)
def test_ac4_sort_orders(tasks_file, capsys, sort, expected):
    assert listed_titles(capsys, "--sort", sort) == expected


def test_ac4_filters(tasks_file, capsys):
    main(["done", "2"])
    assert listed_titles(capsys, "--status", "done") == ["Apple"]
    assert listed_titles(capsys, "--status", "open") == ["banana", "cherry"]
    assert listed_titles(capsys, "--tag", "home") == ["banana"]


def test_ac2_done_only_marks_one_task(tasks_file):
    assert main(["done", "3"]) == 0
    assert [t.done for t in Storage().load()] == [False, False, True]


def test_ac3_invalid_priority_saves_nothing(tasks_file):
    before = tasks_file.read_text()
    assert main(["add", "X", "--priority", "urgent"]) == 1
    assert tasks_file.read_text() == before


def test_ac5_storage_format_is_list_of_objects(tasks_file):
    data = json.loads(tasks_file.read_text())
    assert isinstance(data, list)
    assert set(data[0]) == {"id", "title", "priority", "due", "done", "tags"}
