from __future__ import annotations

import re


def upsert_active_next_target(text: str, target: str, updated_utc: str) -> str:
    block = (
        "## Active Pointer\n"
        f"- active_next_target: {target}\n"
        f"- updated_utc: {updated_utc}\n"
    )
    pattern = re.compile(
        r"## Active Pointer\n- active_next_target: .*\n- updated_utc: .*\n?",
        re.MULTILINE,
    )
    if pattern.search(text):
        return pattern.sub(block, text, count=1)
    if not text.endswith("\n"):
        text += "\n"
    return text + "\n" + block
