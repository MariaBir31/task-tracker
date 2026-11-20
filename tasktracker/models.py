from dataclasses import dataclass, field, asdict
from datetime import date


PRIORITIES = ["low", "medium", "high"]


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    due: str = ""          # ISO date string, e.g. "2026-11-25"; empty = no due date
    done: bool = False
    tags: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return Task(**d)

    def is_overdue(self, today=None):
        if not self.due or self.done:
            return False
        today = today or date.today()
        return date.fromisoformat(self.due) < today
