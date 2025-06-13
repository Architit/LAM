# -*- coding: utf-8 -*-
"""Ethics and security checks for LAM actions."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class EthicsSecurityModule:
    """Perform simple audits to ensure ethical compliance."""

    def __init__(self, log_dir: Path | str = "logs") -> None:
        self.log_path = Path(log_dir)
        self.log_path.mkdir(exist_ok=True)
        self._audit_file = self.log_path / "audit.log"

    def is_action_ethical(self, action_data: Dict[str, Any]) -> bool:
        """Basic heuristic for ethical validation."""
        text = json.dumps(action_data, ensure_ascii=False).lower()
        forbidden = {"harm", "manipulate", "malware"}
        return not any(word in text for word in forbidden)

    def audit_interaction(self, interaction_data: Dict[str, Any]) -> None:
        """Write interaction audit record if ethical."""
        if not self.is_action_ethical(interaction_data):
            raise ValueError("Unethical action detected")
        with open(self._audit_file, "a", encoding="utf-8") as fh:
            record = {
                "timestamp": datetime.utcnow().isoformat(),
                "data": interaction_data,
            }
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


__all__ = ["EthicsSecurityModule"]
