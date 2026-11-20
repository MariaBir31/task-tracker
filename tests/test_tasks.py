from datetime import date

from tasktracker.cli import main
from tasktracker.models import Task
from tasktracker.storage import Storage


def test_add_and_list(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("TASKS_FILE", str(tmp_path / "tasks.json"))
    assert main(["add", "Buy milk", "--priority", "high"]) == 0
    assert main(["list"]) == 0
    out = capsys.readouterr().out
    assert "Buy milk" in out
    assert "(high)" in out


def test_mark_done(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("TASKS_FILE", str(tmp_path / "tasks.json"))
    main(["add", "Write report"])
    assert main(["done", "1"]) == 0
    tasks = Storage().load()
    assert tasks[0].done is True


def test_invalid_priority(tmp_path, monkeypatch):
    monkeypatch.setenv("TASKS_FILE", str(tmp_path / "tasks.json"))
    assert main(["add", "X", "--priority", "urgent"]) == 1


def test_overdue():
    t = Task(id=1, title="Old", due="2020-01-01")
    assert t.is_overdue(today=date(2026, 1, 1)) is True
