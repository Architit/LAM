import pytest

from src.result_envelope import EnvelopeContext, ResultEnvelope


def test_ok_envelope_minimal():
    ctx = EnvelopeContext(trace_id="t1", task_id="k1")
    env = ResultEnvelope.ok(context=ctx)
    d = env.to_dict()
    assert d["status"] == "ok"
    assert d["context"]["trace_id"] == "t1"
    assert d["context"]["task_id"] == "k1"
    assert d["result"] is None
    assert d["error"] is None
    assert "metrics" in d and isinstance(d["metrics"], dict)


def test_error_requires_error_dict():
    ctx = EnvelopeContext(trace_id="t1", task_id="k1")
    with pytest.raises(ValueError):
        ResultEnvelope(status="error", context=ctx, error=None)

    env = ResultEnvelope.err(context=ctx, error={"code": "E", "message": "boom"})
    d = env.to_dict()
    assert d["status"] == "error"
    assert d["error"]["code"] == "E"


def test_ok_rejects_error():
    ctx = EnvelopeContext(trace_id="t1", task_id="k1")
    with pytest.raises(ValueError):
        ResultEnvelope(status="ok", context=ctx, error={"message": "nope"})
