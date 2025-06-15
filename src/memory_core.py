# -*- coding: utf-8 -*-
"""Core memory management for LAM.

This module defines the ``MemoryCore`` class which maintains a structured
memory database for the artificial consciousness project. Memory entries
and their category mapping are persisted as JSON and include a variety of
metadata. The class offers basic retrieval, importance update and
forgetting mechanics.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid
import os
import tomllib
from math import sqrt

from opentelemetry import trace
from .logging_utils import get_json_logger

# Repository root resolved from this file's location
REPO_ROOT = Path(__file__).resolve().parent.parent

logger = get_json_logger(__name__)
tracer = trace.get_tracer(__name__)  # type: ignore[attr-defined]

try:
    import faiss  # type: ignore
    import numpy as np

    FAISS_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    FAISS_AVAILABLE = False

# Default path where memory data is stored relative to the repository root
DEFAULT_MEMORY_PATH = REPO_ROOT / "memory"


def _update_paths(base: Path) -> Dict[str, Path]:
    """Return file paths for the given base path."""

    base = base.expanduser()
    return {
        "base_path": base,
        "log_dir": base / "logs",
        "metadata_dir": base / "metadata",
        "data_dir": base / "data",
        "memory_file": base / "data" / "memory_items.json",
        "category_file": base / "metadata" / "categories.json",
        "anchor_file": base / "metadata" / "anchor_memory_phase.json",
    }


def _load_memory_path() -> Path:
    """Return memory path from config or default."""
    base: Optional[str] = None

    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if "=" not in line or line.strip().startswith("#"):
                continue
            key, value = line.split("=", 1)
            if key.strip() == "LAM_MEMORY_PATH":
                base = value.strip()
                break

    base = os.getenv("LAM_MEMORY_PATH", base)

    if not base:
        pyproject = REPO_ROOT / "pyproject.toml"
        if pyproject.exists():
            with open(pyproject, "rb") as fh:
                data = tomllib.load(fh)
            base = data.get("tool", {}).get("lam", {}).get("memory_path")

    if base:
        path = Path(base).expanduser()
        if not path.is_absolute():
            path = (REPO_ROOT / path).resolve()
        else:
            path = path.resolve()
        return path

    return DEFAULT_MEMORY_PATH


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
    embedding: List[float] = field(default_factory=list)
    last_access: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    access_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Return dictionary representation."""
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MemoryEntry":
        """Create ``MemoryEntry`` from dictionary."""
        return MemoryEntry(**data)


class MemoryCore:
    """Memory management core."""

    def __init__(self, memory_path: Optional[Path] | None = None) -> None:
        if memory_path is None:
            memory_path = _load_memory_path()

        paths = _update_paths(Path(memory_path))

        self.base_path: Path = paths["base_path"].resolve()
        self.log_dir: Path = paths["log_dir"]
        self.metadata_dir: Path = paths["metadata_dir"]
        self.data_dir: Path = paths["data_dir"]
        self.memory_file: Path = paths["memory_file"]
        self.category_file: Path = paths["category_file"]
        self.anchor_file: Path = paths["anchor_file"]

        self.base_path.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)
        self.metadata_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        if self.memory_file.exists():
            with open(self.memory_file, "r", encoding="utf-8") as fh:
                self._memories: List[MemoryEntry] = [
                    MemoryEntry.from_dict(m) for m in json.load(fh)
                ]
        else:
            self._memories = []

        self.categories: Dict[str, List[str]] = {}
        if self.category_file.exists():
            with open(self.category_file, "r", encoding="utf-8") as fh:
                self.categories = json.load(fh)
        else:
            for mem in self._memories:
                self.categorize(mem)
            self._save()

        self._index = None
        self._index_map: List[str] = []
        self._build_index()

    def get_memories(self) -> List[MemoryEntry]:
        """Return list of all stored memories."""
        return list(self._memories)

    # --------------------------- persistence ----------------------------
    def _save(self) -> None:
        with open(self.memory_file, "w", encoding="utf-8") as fh:
            json.dump(
                [m.to_dict() for m in self._memories],
                fh,
                ensure_ascii=False,
                indent=2,
            )
        with open(self.category_file, "w", encoding="utf-8") as fh:
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

    def _build_index(self) -> None:
        """(Re)build FAISS index from stored embeddings."""
        if not FAISS_AVAILABLE:
            self._index = None
            self._index_map = []
            return

        embeddings = [m.embedding for m in self._memories if m.embedding]
        if not embeddings:
            self._index = None
            self._index_map = []
            return

        dim = len(embeddings[0])
        self._index = faiss.IndexFlatIP(dim)
        xb = np.array(embeddings, dtype="float32")
        faiss.normalize_L2(xb)
        if self._index is not None:
            self._index.add(xb)
        self._index_map = [m.id for m in self._memories if m.embedding]

    # --------------------------- main API ----------------------------
    def add_memory(self, memory_entry: Dict[str, Any]) -> None:
        """Add a new memory to storage."""
        memory_entry.setdefault("id", self._generate_id())
        with tracer.start_as_current_span("add_memory"):
            logger.info("add_memory", extra={"entry": memory_entry["id"]})
        memory_entry.setdefault(
            "tags",
            self.generate_tags(memory_entry.get("content", "")),
        )
        memory_entry.setdefault("importance", 0.5)
        mem = MemoryEntry.from_dict(memory_entry)
        self.categorize(mem)
        self._memories.append(mem)
        self._save()
        self._build_index()

    def retrieve_memory(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retrieve memories matching provided criteria."""
        results: List[MemoryEntry] = []
        with tracer.start_as_current_span("retrieve_memory"):
            logger.info("retrieve_memory", extra={"criteria": criteria})
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
                if not set(criteria["associations"]).intersection(mem.associations):
                    match = False
            if match:
                mem.access_count += 1
                mem.last_access = datetime.utcnow().isoformat()
                results.append(mem)
        self._save()
        return [m.to_dict() for m in results]

    def retrieve_by_embedding(
        self, embedding: List[float], k: int = 1
    ) -> List[Dict[str, Any]]:
        """Return ``k`` memories with closest embeddings using cosine similarity."""
        with tracer.start_as_current_span("retrieve_by_embedding"):
            logger.info("retrieve_by_embedding", extra={"k": k})
        if not FAISS_AVAILABLE or self._index is None:
            # Fallback to manual cosine similarity
            scored: List[tuple[float, MemoryEntry]] = []
            norm_q = sqrt(sum(v * v for v in embedding)) or 1.0
            for mem in self._memories:
                if not mem.embedding:
                    continue
                dot = sum(a * b for a, b in zip(embedding, mem.embedding))
                norm_m = sqrt(sum(v * v for v in mem.embedding)) or 1.0
                score = dot / (norm_q * norm_m)
                scored.append((score, mem))
            scored.sort(key=lambda x: x[0], reverse=True)
            top = [m for _, m in scored[:k] if _ >= 0]
        else:
            xq = np.array([embedding], dtype="float32")
            faiss.normalize_L2(xq)
            distances, indices = self._index.search(xq, k)
            top = []
            for idx in indices[0]:
                if idx == -1:
                    continue
                mem_id = self._index_map[idx]
                mem = next((m for m in self._memories if m.id == mem_id), None)
                if mem:
                    top.append(mem)

        results: List[MemoryEntry] = []
        for mem in top:
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
        self._build_index()

    # --------------------------- ethics ----------------------------
    def integrity_check(self) -> bool:
        """Perform a basic ethics audit."""
        for mem in self._memories:
            if not 0.0 <= mem.importance <= 1.0:
                return False
        return True


__all__ = ["MemoryCore", "MemoryEntry"]
