"""Sort strategies for `list --sort` (Strategy pattern).

Each strategy is a function that takes a list of tasks and returns a new sorted list.
To add a sort order, add one entry to SORT_STRATEGIES; the CLI picks it up automatically.
"""
from .models import PRIORITIES


def by_id(tasks):
    return sorted(tasks, key=lambda t: t.id)


def by_priority(tasks):
    return sorted(tasks, key=lambda t: PRIORITIES.index(t.priority), reverse=True)


def by_due(tasks):
    return sorted(tasks, key=lambda t: t.due or "9999-12-31")


def by_title(tasks):
    return sorted(tasks, key=lambda t: t.title.lower())


SORT_STRATEGIES = {
    "id": by_id,
    "priority": by_priority,
    "due": by_due,
    "title": by_title,
}
