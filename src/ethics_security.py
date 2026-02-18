# -*- coding: utf-8 -*-
"""Ethics and security checks for LAM actions."""

from __future__ import annotations

import json
import hashlib
import os
import unicodedata
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


FORBIDDEN_TERMS = {
    "harm",
    "manipulate",
    "malware",
    "abuse",
    "attack",
    "exploit",
    "phish",
    "scam",
    "virus",
    "violence",
}

_CYRILLIC_MAP = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


class EthicsSecurityModule:
    """Perform simple audits to ensure ethical compliance."""

    def __init__(self, log_dir: Path | str = "logs") -> None:
        self.log_path = Path(log_dir)
        self.log_path.mkdir(exist_ok=True)
        self._audit_file = self.log_path / "audit.log"
        self._openai = self._load_openai()
        self._last_hash = self._init_hash()

    def _load_openai(self):
        """Attempt to load OpenAI for moderation."""
        try:
            import openai  # type: ignore
        except Exception:
            return None
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            return None
        openai.api_key = key
        return openai

    def _init_hash(self) -> str:
        """Initialize hash chain from existing log."""
        self._audit_file.touch(exist_ok=True)
        last_hash = "0" * 64
        try:
            line = ""
            with open(self._audit_file, "r", encoding="utf-8") as fh:
                for line in fh:
                    pass
            if line:
                last_hash = json.loads(line).get("hash", last_hash)
        except Exception:
            pass
        return last_hash

    def _normalize_text(self, text: str) -> str:
        """Return a lowercase, transliterated version of ``text``."""
        text = text.lower()
        normalized = []
        for ch in text:
            if ch in _CYRILLIC_MAP:
                normalized.append(_CYRILLIC_MAP[ch])
                continue
            decomposed = unicodedata.normalize("NFD", ch)
            ascii_char = decomposed.encode("ascii", "ignore").decode("ascii")
            normalized.append(ascii_char)
        return "".join(normalized)

    def _heuristic(self, text: str) -> bool:
        """Fallback keyword check when classifier is unavailable."""
        text = self._normalize_text(text)
        return not any(term in text for term in FORBIDDEN_TERMS)

    def is_action_ethical(self, action_data: Dict[str, Any]) -> bool:
        """Determine ethicality using OpenAI moderation with heuristic fallback."""
        text = json.dumps(action_data, ensure_ascii=False)
        if self._openai:
            try:
                resp = self._openai.Moderation.create(input=text)
                return not resp["results"][0]["flagged"]
            except Exception as exc:
                logging.getLogger(__name__).warning(
                    "moderation_unavailable_fallback_heuristic",
                    extra={"error": str(exc)},
                )
        return self._heuristic(text)

    def audit_interaction(self, interaction_data: Dict[str, Any]) -> None:
        """Write interaction audit record if ethical."""
        if not self.is_action_ethical(interaction_data):
            raise ValueError("Unethical action detected")
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": interaction_data,
            "prev_hash": self._last_hash,
        }
        record_bytes = json.dumps(record, sort_keys=True, ensure_ascii=False).encode()
        record_hash = hashlib.sha256(record_bytes).hexdigest()
        record["hash"] = record_hash
        with open(self._audit_file, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        self._last_hash = record_hash


__all__ = ["EthicsSecurityModule"]
