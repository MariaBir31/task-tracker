"""Regression tests for the two mitigated risks (R1, R2)."""
from tasktracker.cli import main
from tasktracker.storage import Storage


def test_r1_ids_stay_unique_after_delete(tmp_path, monkeypatch):
    monkeypatch.setenv("TASKS_FILE", str(tmp_path / "tasks.json"))
    for title in ["A", "B", "C"]:
        main(["add", title])
    main(["delete", "1"])
    main(["add", "D"])
    ids = [t.id for t in Storage().load()]
    assert len(ids) == len(set(ids)), f"duplicate ids: {ids}"
    # deleting one id must remove exactly one task
    main(["delete", "3"])
    assert [t.title for t in Storage().load()] == ["B", "D"]


def test_r2_invalid_due_date_is_rejected(tmp_path, monkeypatch, capsys):
    path = tmp_path / "tasks.json"
    monkeypatch.setenv("TASKS_FILE", str(path))
    assert main(["add", "Pay rent", "--due", "tomorrow"]) == 1
    assert "Invalid due date" in capsys.readouterr().out
    assert not path.exists()  # nothing saved
    assert main(["list"]) == 0  # list still works


def test_r2_valid_due_date_still_accepted(tmp_path, monkeypatch):
    monkeypatch.setenv("TASKS_FILE", str(tmp_path / "tasks.json"))
    assert main(["add", "Pay rent", "--due", "2026-12-01"]) == 0
    assert Storage().load()[0].due == "2026-12-01"
