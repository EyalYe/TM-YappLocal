# yapplocal — a TaskMaster-C3 "Local" source

A self-contained **task source** for [TaskMaster-C3](https://github.com/EyalYe/TaskMaster):
a platform-agnostic LAN server implementing the device REST contract over an
in-memory store (no Todoist, no cloud). The device's "Local" Task Manager app
talks to it; swap the store for a DB/file/whatever — the contract is the only spec.

This repo is one half of a **source product**: the host server (here) plus the
device app component (added under `app/` once the TaskMaster Task Manager lands).
Keeping it in its own repo means core and app development stay independent — the
device's stable app API + REST contract are the only coupling.

## The contract

```
GET  /tasks                      -> { "etag", "tasks":[ {id, parent_id, title,
                                      due, priority(1..4, 4=highest), done}, ... ] }
POST /tasks/{id}/complete        -> mark complete (drops it from /tasks)
POST /tasks/{id}/postpone {due}  -> reschedule
GET  /health                     -> { "ok": true }
```

## Run

```bash
python3 server.py --port 8080      # Python stdlib only, no dependencies
```

Then point the device's "Local" source URL at `http://<this-machine-ip>:8080`.

## Verify

```bash
curl localhost:8080/tasks
curl -X POST localhost:8080/tasks/1/complete
```
