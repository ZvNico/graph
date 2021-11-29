from dataclasses import dataclass

from .Node import Node


@dataclass
class Arc:
    start: Node
    end: Node
    dist: int
