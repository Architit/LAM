import pytest

from src.epi_evolution import create_app


@pytest.mark.asyncio
async def test_meiosis_mutates_intents(http_client):
    app = create_app()
    session, base = await http_client(app)
    async with session.post(
        f"{base}/meiosis", json={"intents": ["seek", "grow"]}
    ) as resp:
        assert resp.status == 200
        data = await resp.json()
        assert data["intents"] == ["seek_mutated", "grow_mutated"]
