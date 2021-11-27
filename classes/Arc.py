from .Node import Node

from dataclasses import dataclass


@dataclass
class Arc:
    start: Node
    end: Node
    dist: int
