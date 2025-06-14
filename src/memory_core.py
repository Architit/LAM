# -*- coding: utf-8 -*-
"""Core memory management for LAM.

This module defines the ``MemoryCore`` class which maintains a structured
memory database for the artificial consciousness project. Memory entries
are persisted as JSON and include a variety of metadata. The class offers
basic retrieval, importance update and forgetting mechanics.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid

# Path where memory data is stored
MEMORY_PATH = Path("memory")
MEMORY_FILE = MEMORY_PATH / "memories.json"
CATEGORY_FILE = MEMORY_PATH / "categories.json"


@dataclass
class MemoryEntry:
    """Represents a single memory item."""

    id: str
    name: str
    timestamp: str
    content: str
    importance: float
    associations: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    last_access: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
    access_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MemoryEntry":
        return MemoryEntry(**data)


class MemoryCore:
    """Memory management core."""

    def __init__(self) -> None:
        MEMORY_PATH.mkdir(exist_ok=True)
        if MEMORY_FILE.exists():
            with open(MEMORY_FILE, "r", encoding="utf-8") as fh:
                self._memories: List[MemoryEntry] = [
                    MemoryEntry.from_dict(m) for m in json.load(fh)
                ]
        else:
            self._memories = []

        self.categories: Dict[str, List[str]] = {}
        if CATEGORY_FILE.exists():
            with open(CATEGORY_FILE, "r", encoding="utf-8") as fh:
                self.categories = json.load(fh)
        else:
            for mem in self._memories:
                self.categorize(mem)

    def get_memories(self) -> List[MemoryEntry]:
        """Return list of all stored memories."""
        return list(self._memories)

    # --------------------------- persistence ----------------------------
    def _save(self) -> None:
        with open(MEMORY_FILE, "w", encoding="utf-8") as fh:
            json.dump(
                [m.to_dict() for m in self._memories],
                fh,
                ensure_ascii=False,
                indent=2,
            )
        with open(CATEGORY_FILE, "w", encoding="utf-8") as fh:
            json.dump(self.categories, fh, ensure_ascii=False, indent=2)

    # --------------------------- utilities ----------------------------
    def _generate_id(self) -> str:
        return str(uuid.uuid4())

    def generate_tags(self, content: str) -> List[str]:
        """Generate simple tags from content words."""
        words = [w.strip(".,!?;:") for w in content.split()]
        unique = {w.lower() for w in words if len(w) > 3}
        return list(unique)

    def categorize(self, memory_entry: MemoryEntry) -> None:
        """Assign categories to memory and update the mapping."""
        for tag in memory_entry.tags:
            if tag not in self.categories:
                self.categories[tag] = []
            self.categories[tag].append(memory_entry.id)

    # --------------------------- main API ----------------------------
    def add_memory(self, memory_entry: Dict[str, Any]) -> None:
        """Add a new memory to storage."""
        memory_entry.setdefault("id", self._generate_id())
        memory_entry.setdefault(
            "tags",
            self.generate_tags(memory_entry.get("content", "")),
        )
        memory_entry.setdefault("importance", 0.5)
        mem = MemoryEntry.from_dict(memory_entry)
        self.categorize(mem)
        self._memories.append(mem)
        self._save()

    def retrieve_memory(
        self, criteria: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Retrieve memories matching provided criteria."""
        results: List[MemoryEntry] = []
        for mem in self._memories:
            match = True
            if "time_range" in criteria:
                time_range = criteria["time_range"]
                if not mem.timestamp.startswith(time_range):
                    match = False
            if "tags" in criteria:
                if not set(criteria["tags"]).intersection(mem.tags):
                    match = False
            if "associations" in criteria:
                if not set(criteria["associations"]).intersection(
                    mem.associations
                ):
                    match = False
            if match:
                mem.access_count += 1
                mem.last_access = datetime.utcnow().isoformat()
                results.append(mem)
        self._save()
        return [m.to_dict() for m in results]

    def update_importance(self) -> None:
        """Update memory importance based on age and accesses."""
        now = datetime.utcnow()
        for mem in self._memories:
            try:
                ts = datetime.fromisoformat(mem.timestamp.replace("≈", ""))
            except ValueError:
                continue
            age_days = (now - ts).days
            decay = age_days / 365
            access_factor = min(mem.access_count / 10, 1)
            mem.importance = max(
                0.0,
                min(
                    1.0,
                    mem.importance * (1 - decay) + access_factor * 0.1,
                ),
            )
        self._save()

    def forget(
        self, min_importance: float = 0.2, max_age: Optional[str] = None
    ) -> None:
        """Forget memories with low importance or exceeding max age."""
        now = datetime.utcnow()
        keep: List[MemoryEntry] = []
        for mem in self._memories:
            if mem.importance < min_importance:
                continue
            if max_age:
                try:
                    ts = datetime.fromisoformat(mem.timestamp.replace("≈", ""))
                    age_days = (now - ts).days
                    if age_days > int(max_age):
                        continue
                except ValueError:
                    pass
            keep.append(mem)
        self._memories = keep
        self._save()

    # --------------------------- ethics ----------------------------
    def integrity_check(self) -> bool:
        """Perform a basic ethics audit."""
        for mem in self._memories:
            if not 0.0 <= mem.importance <= 1.0:
                return False
        return True


__all__ = ["MemoryCore", "MemoryEntry"]
