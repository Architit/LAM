# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
import json

from src.lam_logging import clear_context, log, set_context


def test_lam_logging_auto_injects_trace_and_task(capsys, monkeypatch) -> None:
    # Разрешаем info-логи (по умолчанию LAM_LOG_LEVEL=warn и info не печатается)
    monkeypatch.setenv("LAM_LOG_LEVEL", "info")

    clear_context()
    set_context(trace_id="trace_123", task_id="task_456", parent_task_id="parent_1", span_id="span_9")

    # Не передаём trace_id/task_id явно — должны появиться автоматически
    log("info", "test", "hello", foo="bar")

    out = capsys.readouterr().out.strip()
    assert out, "expected one JSON log line"

    payload = json.loads(out)
    assert payload["trace_id"] == "trace_123"
    assert payload["task_id"] == "task_456"
    assert payload["parent_task_id"] == "parent_1"
    assert payload["span_id"] == "span_9"
    assert payload["foo"] == "bar"
