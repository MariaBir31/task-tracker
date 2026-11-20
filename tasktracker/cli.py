import argparse
import sys
from datetime import date

from .models import Task, PRIORITIES
from .sorting import SORT_STRATEGIES
from .storage import Storage


def cmd_add(storage, args):
    tasks = storage.load()
    if args.priority not in PRIORITIES:
        print("Invalid priority: " + args.priority)
        return 1
    # R2: reject due dates that would later crash list/stats
    if args.due:
        try:
            date.fromisoformat(args.due)
        except ValueError:
            print(f"Invalid due date: {args.due} (expected YYYY-MM-DD)")
            return 1
    task = Task(
        id=storage.next_id(tasks),
        title=args.title,
        priority=args.priority,
        due=args.due or "",
        tags=args.tags.split(",") if args.tags else [],
    )
    tasks.append(task)
    storage.save(tasks)
    print(f"Added task #{task.id}: {task.title}")
    return 0


def cmd_list(storage, args):
    tasks = storage.load()

    # filtering
    if args.status == "open":
        tasks = [t for t in tasks if not t.done]
    elif args.status == "done":
        tasks = [t for t in tasks if t.done]
    if args.tag:
        tasks = [t for t in tasks if args.tag in t.tags]

    tasks = SORT_STRATEGIES[args.sort](tasks)

    if not tasks:
        print("No tasks.")
        return 0
    for t in tasks:
        mark = "x" if t.done else " "
        overdue = " (OVERDUE)" if t.is_overdue() else ""
        due = f" due {t.due}" if t.due else ""
        tags = f" [{', '.join(t.tags)}]" if t.tags else ""
        print(f"[{mark}] #{t.id} {t.title} ({t.priority}){due}{tags}{overdue}")
    return 0


def cmd_done(storage, args):
    tasks = storage.load()
    for t in tasks:
        if t.id == args.id:
            t.done = True
            storage.save(tasks)
            print(f"Task #{t.id} marked as done.")
            return 0
    print(f"Task #{args.id} not found.")
    return 1


def cmd_delete(storage, args):
    tasks = storage.load()
    new_tasks = [t for t in tasks if t.id != args.id]
    if len(new_tasks) == len(tasks):
        print(f"Task #{args.id} not found.")
        return 1
    storage.save(new_tasks)
    print(f"Task #{args.id} deleted.")
    return 0


def cmd_stats(storage, args):
    tasks = storage.load()
    total = len(tasks)
    done = len([t for t in tasks if t.done])
    overdue = len([t for t in tasks if t.is_overdue()])
    print(f"Total: {total}, done: {done}, open: {total - done}, overdue: {overdue}")
    print(f"Completion: {done / total * 100:.0f}%")
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="tasktracker", description="Simple CLI task tracker")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="add a task")
    a.add_argument("title")
    a.add_argument("--priority", default="medium")
    a.add_argument("--due", help="due date YYYY-MM-DD")
    a.add_argument("--tags", help="comma-separated tags")

    l = sub.add_parser("list", help="list tasks")
    l.add_argument("--status", choices=["all", "open", "done"], default="all")
    l.add_argument("--tag")
    l.add_argument("--sort", choices=list(SORT_STRATEGIES), default="id")

    d = sub.add_parser("done", help="mark task as done")
    d.add_argument("id", type=int)

    r = sub.add_parser("delete", help="delete a task")
    r.add_argument("id", type=int)

    sub.add_parser("stats", help="show statistics")
    return p


COMMANDS = {
    "add": cmd_add,
    "list": cmd_list,
    "done": cmd_done,
    "delete": cmd_delete,
    "stats": cmd_stats,
}


def main(argv=None):
    args = build_parser().parse_args(argv)
    storage = Storage()
    return COMMANDS[args.command](storage, args)


if __name__ == "__main__":
    sys.exit(main())
