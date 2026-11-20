import json
import os

from .models import Task

DEFAULT_FILE = os.path.join(os.path.expanduser("~"), ".tasks.json")


class Storage:
    def __init__(self, path=None):
        self.path = path or os.environ.get("TASKS_FILE", DEFAULT_FILE)

    def load(self):
        if not os.path.exists(self.path):
            return []
        with open(self.path) as f:
            data = json.load(f)
        return [Task.from_dict(d) for d in data]

    def save(self, tasks):
        with open(self.path, "w") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=2)

    def next_id(self, tasks):
        # R1: use max id, not count, so ids stay unique after deletions
        return max((t.id for t in tasks), default=0) + 1
