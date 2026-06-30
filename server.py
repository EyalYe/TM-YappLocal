#!/usr/bin/env python3
"""
yapplocal — a platform-agnostic LAN task source for TaskMaster-C3.

Implements the device REST contract (the "known endpoints") over an in-memory
task store, so the device's "Local" Task Manager app has something to talk to
that is NOT Todoist. Swap the store for a DB/file/whatever — the contract is the
only spec the device knows.

  GET  /tasks                      -> { "etag", "tasks":[ {id,parent_id,title,
                                        due,priority(1..4),done}, ... ] }
  POST /tasks/{id}/complete        -> mark complete (drops it from /tasks)
  POST /tasks/{id}/postpone {due}  -> reschedule
  GET  /health                     -> { "ok": true }

Run:  python3 server.py [--port 8080]
No third-party dependencies (Python stdlib only).
"""
import argparse
import hashlib
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Contract bounds. TITLE_MAX must be <= the device's TASK_TITLE_MAX-1 so titles
# arrive pre-truncated (the device also bounds them).
DEFAULT_PORT = 8080
TITLE_MAX = 47
PRIO_MIN, PRIO_MAX = 1, 4          # 4 = highest (matches Todoist P1)

# In-memory store — canned tasks for the "Local" app + tests.
TASKS = [
    {"id": "1", "parent_id": "",  "title": "Water the plants",       "due": "today",    "priority": 4, "done": False},
    {"id": "2", "parent_id": "",  "title": "Read a chapter",          "due": "tomorrow", "priority": 2, "done": False},
    {"id": "3", "parent_id": "2", "title": "Find the bookmark",       "due": "",         "priority": 2, "done": False},
    {"id": "4", "parent_id": "",  "title": "Reply to the long email", "due": "fri",      "priority": 3, "done": False},
]


def open_tasks():
    out = []
    for t in TASKS:
        if t["done"]:
            continue
        out.append({
            "id": str(t["id"]),
            "parent_id": str(t["parent_id"]),
            "title": t["title"][:TITLE_MAX],
            "due": t["due"],
            "priority": max(PRIO_MIN, min(PRIO_MAX, int(t["priority"]))),
            "done": False,
        })
    # priority-sorted, highest first (mirrors todomark / §8.2)
    out.sort(key=lambda x: x["priority"], reverse=True)
    return out


def etag_for(tasks):
    raw = json.dumps(tasks, sort_keys=True).encode()
    return hashlib.sha1(raw).hexdigest()[:16]


def find(task_id):
    for t in TASKS:
        if str(t["id"]) == str(task_id):
            return t
    return None


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj=None):
        body = b"" if obj is None else json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/tasks"):
            tasks = open_tasks()
            self._send(200, {"etag": etag_for(tasks), "tasks": tasks})
        elif self.path == "/health":
            self._send(200, {"ok": True})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        m = re.match(r"^/tasks/([^/]+)/(complete|postpone)$", self.path)
        if not m:
            self._send(404, {"error": "not found"})
            return
        task_id, action = m.group(1), m.group(2)
        t = find(task_id)
        if t is None:
            self._send(404, {"error": "no such task"})
            return
        if action == "complete":
            t["done"] = True
            self._send(200, {"ok": True})
        else:  # postpone
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length else b"{}"
            try:
                due = json.loads(body or b"{}").get("due", "")
            except json.JSONDecodeError:
                due = ""
            t["due"] = due
            self._send(200, {"ok": True})

    def log_message(self, fmt, *args):
        print("yapplocal:", fmt % args)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = ap.parse_args()
    srv = ThreadingHTTPServer(("0.0.0.0", args.port), Handler)
    print(f"yapplocal serving the device contract on http://0.0.0.0:{args.port}")
    print("  GET /tasks  GET /health  POST /tasks/{id}/complete  POST /tasks/{id}/postpone")
    srv.serve_forever()


if __name__ == "__main__":
    main()
