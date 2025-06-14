# -*- coding: utf-8 -*-
"""Filesystem utilities for LAM.

This module implements breadth-first directory traversal for collecting
directory names. Traversal is performed in alphabetical order to produce
deterministic results suitable for testing.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Deque, List


def bfs_directory_names(root: Path) -> List[str]:
    """Return directory names starting from ``root`` using BFS.

    Parameters
    ----------
    root:
        Root directory to traverse.
    """
    dirs: List[str] = []
    queue: Deque[Path] = deque([root])

    while queue:
        current = queue.popleft()
        if current != root:
            dirs.append(str(current.relative_to(root)))
        for item in sorted(current.iterdir()):
            if item.is_dir():
                queue.append(item)
    return dirs


__all__ = ["bfs_directory_names"]
