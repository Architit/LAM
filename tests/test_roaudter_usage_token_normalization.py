from roaudter_agent.router import RouterAgent
from roaudter_agent.contracts import TaskEnvelope
from roaudter_agent.policy import RouterPolicy
from roaudter_agent.providers.base import ProviderAdapter, ProviderState


class FakeAdapter(ProviderAdapter):
    name = "fake"

    def generate(self, task: TaskEnvelope):
        return {
            "text": "ok",
            "usage": {
                "prompt_tokens": 7,
                "completion_tokens": 5,
            },
        }


def test_tokens_are_sum_of_prompt_and_completion_when_total_missing():
    router = RouterAgent(
        policy=RouterPolicy(default_chain=[]),
        providers=[ProviderState(adapter=FakeAdapter(), healthy=True)],
    )

    # unit-test: ignore health filtering; we test only usage/tokens normalization
    router.health.is_healthy = lambda _p: True  # type: ignore[attr-defined]

    res = router.route(TaskEnvelope(task_id="t1", agent="t", intent="chat", payload={"msg": "hi"}))

    assert res.status == "ok"
    assert res.usage == {"prompt_tokens": 7, "completion_tokens": 5}
    assert res.tokens == 12
