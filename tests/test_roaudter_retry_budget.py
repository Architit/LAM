# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
from roaudter_agent.router import RouterAgent
from roaudter_agent.contracts import TaskEnvelope
from roaudter_agent.policy import RouterPolicy
from roaudter_agent.providers.base import ProviderAdapter, ProviderError, ProviderState


class Flaky429Adapter(ProviderAdapter):
    name = "flaky429"

    def __init__(self) -> None:
        self.calls = 0

    def generate(self, task: TaskEnvelope):
        self.calls += 1
        if self.calls < 3:
            raise ProviderError(
                code="quota",
                http_status=429,
                retryable=True,
                message="rate limit",
                meta={"calls": self.calls},
            )
        return {"text": "ok", "usage": {"total_tokens": 1}}


def test_retry_budget_retries_retryable_errors_then_succeeds():
    adapter = Flaky429Adapter()
    router = RouterAgent(
        policy=RouterPolicy(default_chain=[]),
        providers=[ProviderState(adapter=adapter, healthy=True)],
    )
    router.health.is_healthy = lambda _p: True  # type: ignore[attr-defined]

    task = TaskEnvelope(task_id="t1", agent="t", intent="chat", payload={"msg": "hi"})
    res = router.route(task)

    assert res.status == "ok"
    assert res.provider_used == "flaky429"
    assert adapter.calls == 3


class Always429Adapter(ProviderAdapter):
    name = "always429"
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, task: TaskEnvelope):
        self.calls += 1
        raise ProviderError(
            "rate limit",
            code="quota",
            http_status=429,
            retryable=True,
            meta={"calls": self.calls},
        )


class OkAdapter(ProviderAdapter):
    name = "ok"
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, task: TaskEnvelope):
        self.calls += 1
        return {"text": "ok", "usage": {"total_tokens": 1}}


def test_retry_budget_exhausts_then_falls_back_to_next_provider():
    a = Always429Adapter()
    b = OkAdapter()

    router = RouterAgent(
        policy=RouterPolicy(default_chain=[]),
        providers=[
            ProviderState(adapter=a, healthy=True),
            ProviderState(adapter=b, healthy=True),
        ],
        retry_max_attempts=3,
        retry_budget_ms=200,          # маленький бюджет для быстрого теста
        retry_base_backoff_ms=1,
        retry_max_backoff_ms=2,
    )
    router.health.is_healthy = lambda _p: True  # type: ignore[attr-defined]

    res = router.route(TaskEnvelope(task_id="t1", agent="t", intent="chat", payload={"msg": "hi"}))

    assert res.status == "ok"
    assert res.provider_used == "ok"
    assert a.calls == 3              # исчерпали попытки на первом
    assert b.calls == 1              # затем один вызов второго


class Always401Adapter(ProviderAdapter):
    name = "always401"
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, task: TaskEnvelope):
        self.calls += 1
        raise ProviderError(
            "unauthorized",
            code="auth",
            http_status=401,
            retryable=True,  # даже если кто-то пометил retryable — мы НЕ должны ретраить 401
        )


def test_retry_does_not_retry_401_even_if_marked_retryable():
    a = Always401Adapter()
    b = OkAdapter()

    router = RouterAgent(
        policy=RouterPolicy(default_chain=[]),
        providers=[ProviderState(adapter=a, healthy=True), ProviderState(adapter=b, healthy=True)],
        retry_max_attempts=5,
        retry_budget_ms=500,
        retry_base_backoff_ms=1,
        retry_max_backoff_ms=2,
    )
    router.health.is_healthy = lambda _p: True  # type: ignore[attr-defined]

    res = router.route(TaskEnvelope(task_id="t1", agent="t", intent="chat", payload={"msg": "hi"}))

    assert res.status == "ok"
    assert res.provider_used == "ok"
    assert a.calls == 1  # ключевое: НЕ 5
    assert b.calls == 1
