# Agent Dev Guide (LAM)

## Envelope Standard (v1)
- input: intent + (msg|payload) + context + task_id + reply_to
- output: status + result + error + metrics + context (preserve trace/task)

## Trace/Task context
- trace_id, task_id, parent_task_id, span_id(optional)
- never drop context across comm → taskarid → roaudter

## Observability (JSONL)
- LAM_LOG_LEVEL, LAM_LOG_EVENTS
- events: comm.*, roaudter.*, mem.*, evt.*

## Runtime smoke
TMPDIR=/tmp TEMP=/tmp TMP=/tmp bash scripts/lam_env.sh .venv/bin/python scripts/obs_smoke_roundtrip.py
